# ============================================
#  Plateforme de gestion SSIAP - Intégrale Academy
#  Version complète et professionnelle
# ============================================

from flask import (
    Flask, render_template, request, redirect, url_for,
    send_from_directory, session, jsonify, flash
)
from werkzeug.utils import secure_filename
import os, json, datetime, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --------------------------------------------
# CONFIGURATION
# --------------------------------------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXT = {"pdf", "jpg", "jpeg", "png"}

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "ecole@integraleacademy.com")
ADMIN_PASS = os.getenv("ADMIN_PASS", "")
ADMIN_LOGIN = os.getenv("ADMIN_LOGIN", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "ssiap2025")


# --------------------------------------------
# JSON DATA HANDLING
# --------------------------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "candidats": [],
            "conformite": {
                "prefecture_avis": "a_venir",
                "test_francais": "a_venir",
                "certificats_medicaux": "a_venir",
                "identites": "a_venir",
                "locaux": "a_venir",
                "formateurs": "a_venir",
                "planning": "a_venir"
            }
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# --------------------------------------------
# EMAIL SENDER
# --------------------------------------------
def send_email(to, subject, html):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = ADMIN_EMAIL
        msg["To"] = to
        msg["Subject"] = subject

        msg.attach(MIMEText(html, "html"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(ADMIN_EMAIL, ADMIN_PASS)
        server.sendmail(ADMIN_EMAIL, to, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email error:", e)


# --------------------------------------------
# AUTH ROUTES
# --------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("user")
        p = request.form.get("password")

        if u == ADMIN_LOGIN and p == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        else:
            flash("Identifiants incorrects")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# --------------------------------------------
# CANDIDATE FORM
# --------------------------------------------
def allowed(f):
    return "." in f and f.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = load_data()

    nom = request.form.get("nom")
    prenom = request.form.get("prenom")
    naissance = request.form.get("naissance")
    telephone = request.form.get("telephone")
    email = request.form.get("email")

    fichiers = {}

    for champ in ["identite", "certificat", "test_francais", "photo"]:
        f = request.files.get(champ)
        if f and allowed(f.filename):
            filename = secure_filename(f"{datetime.datetime.now().timestamp()}_{f.filename}")
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            fichiers[champ] = filename
        else:
            fichiers[champ] = None

    candidat = {
        "id": str(datetime.datetime.now().timestamp()),
        "nom": nom,
        "prenom": prenom,
        "naissance": naissance,
        "telephone": telephone,
        "email": email,
        "fichiers": fichiers,
        "statut": "en_attente",
        "commentaire": "",
        "date_inscription": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    data["candidats"].append(candidat)
    save_data(data)

    # Email au candidat
    send_email(
        email,
        "Votre inscription SSIAP - Intégrale Academy",
        f"""
        <h2>Bonjour {prenom},</h2>
        <p>Votre inscription à la formation SSIAP a bien été reçue.</p>
        <p>Nous reviendrons vers vous rapidement.</p>
        """
    )

    # Email à toi
    send_email(
        ADMIN_EMAIL,
        "📩 Nouveau candidat SSIAP",
        f"""
        <h3>Nouveau candidat :</h3>
        <p><b>{nom} {prenom}</b></p>
        <p>Email : {email}</p>
        <p>Téléphone : {telephone}</p>
        """
    )

    return redirect("/confirmation")


@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")


# --------------------------------------------
# ADMIN
# --------------------------------------------
@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/login")

    data = load_data()
    return render_template("admin.html", data=data)


@app.route("/admin/update-field", methods=["POST"])
def update_field():
    if "admin" not in session:
        return jsonify(error=True)

    req = request.get_json()
    id = req.get("id")
    champ = req.get("champ")
    valeur = req.get("valeur")

    data = load_data()
    for c in data["candidats"]:
        if c["id"] == id:
            c[champ] = valeur

    save_data(data)
    return jsonify(ok=True)


@app.route("/admin/update-conformite", methods=["POST"])
def update_conformite():
    if "admin" not in session:
        return jsonify(error=True)

    req = request.get_json()
    cle = req.get("champ")
    valeur = req.get("valeur")

    data = load_data()
    data["conformite"][cle] = valeur

    save_data(data)
    return jsonify(ok=True)


@app.route("/admin/delete/<id>")
def delete(id):
    if "admin" not in session:
        return redirect("/login")

    data = load_data()
    data["candidats"] = [c for c in data["candidats"] if c["id"] != id]
    save_data(data)

    return redirect("/admin")


# --------------------------------------------
# FILE DOWNLOAD
# --------------------------------------------
@app.route("/uploads/<path:filename>")
def files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# --------------------------------------------
# RUN
# --------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
