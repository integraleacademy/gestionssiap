// ==========================================
//  JS ADMIN – SSIAP
//  - Edition inline
//  - Statuts dossiers
//  - Conformité arrêté 2 mai 2005
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    // ==========================================================
    //    1. MISE À JOUR INLINE (commentaires)
    // ==========================================================
    document.querySelectorAll("td[contenteditable='true']").forEach(cell => {
        cell.addEventListener("blur", () => {
            const tr = cell.closest("tr");
            const id = tr.dataset.id;
            const field = cell.dataset.field;
            const value = cell.textContent.trim();

            cell.style.background = "#fff3cd"; // jaune pendant la sauvegarde

            fetch("/admin/update-field", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id, champ: field, valeur: value })
            })
            .then(r => r.json())
            .then(res => {
                if (res.ok) {
                    cell.style.background = "#d4edda"; // vert après save
                    setTimeout(() => cell.style.background = "transparent", 600);
                } else {
                    cell.style.background = "#f8d7da"; // rouge erreur
                }
            });
        });
    });



    // ==========================================================
    //    2. MISE À JOUR DES STATUTS DES CANDIDATS
    // ==========================================================
    document.querySelectorAll(".select-statut").forEach(select => {
        select.addEventListener("change", () => {
            const tr = select.closest("tr");
            const id = tr.dataset.id;
            const value = select.value;

            select.style.background = "#fff3cd"; // jaune

            fetch("/admin/update-field", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id, champ: "statut", valeur: value })
            })
            .then(r => r.json())
            .then(res => {
                if (res.ok) {
                    select.style.background = value === "complet" ? "#d4edda"
                                      : value === "incomplet" ? "#fce4d6"
                                      : "#f8f9fa";
                    setTimeout(() => select.style.background = "transparent", 600);
                } else {
                    select.style.background = "#f8d7da";
                }
            });
        });
    });



    // ==========================================================
    //    3. GESTION CONFORMITÉ – ARRÊTÉ 2 MAI 2005
    // ==========================================================
    document.querySelectorAll(".conf-btns").forEach(block => {

        const champ = block.dataset.champ;

        block.querySelectorAll(".conf-btn").forEach(btn => {
            btn.addEventListener("click", () => {

                const value = btn.dataset.value;

                // Reset couleurs
                block.querySelectorAll(".conf-btn").forEach(b => {
                    b.classList.remove("green", "orange", "red");
                });

                // Appliquer la classe au bouton cliqué
                if (value === "conforme") btn.classList.add("green");
                if (value === "a_venir") btn.classList.add("orange");
                if (value === "non_conforme") btn.classList.add("red");

                // Envoi serveur
                fetch("/admin/update-conformite", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ champ, valeur: value })
                })
                .then(r => r.json())
                .then(res => {
                    if (!res.ok) {
                        alert("Erreur de sauvegarde");
                    }
                });

            });
        });

    });

});
