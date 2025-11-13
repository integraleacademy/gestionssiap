// ==========================================
//  JS FRONT – FORMULAIRE SSIAP
//  Navigation étapes + récapitulatif
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    const tabs = document.querySelectorAll(".tab-btn");
    const steps = document.querySelectorAll(".tab-content");
    const nextBtns = document.querySelectorAll(".next-btn");
    const prevBtns = document.querySelectorAll(".prev-btn");

    let currentStep = 1;


    // ================================
    //   FONCTION POUR CHANGER D'ÉTAPE
    // ================================
    function showStep(step) {
        currentStep = step;

        // Onglets
        tabs.forEach(btn => {
            btn.classList.remove("active");
            if (parseInt(btn.dataset.step) === step) {
                btn.classList.add("active");
            }
        });

        // Contenus
        steps.forEach(stepDiv => {
            stepDiv.classList.remove("active");
        });
        document.querySelector(".step-" + step).classList.add("active");

        // Mise à jour du récap
        if (step === 3) {
            updateRecap();
        }
    }


    // ================================
    //   NAVIGATION ENTRE ONGLET (CLICK)
    // ================================
    tabs.forEach(btn => {
        btn.addEventListener("click", () => {
            showStep(parseInt(btn.dataset.step));
        });
    });


    // ================================
    //   BOUTONS SUIVANT
    // ================================
    nextBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep < 3) {
                showStep(currentStep + 1);
            }
        });
    });


    // ================================
    //   BOUTONS RETOUR
    // ================================
    prevBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep > 1) {
                showStep(currentStep - 1);
            }
        });
    });



    // ================================
    //   RÉCAPITULATIF (ÉTAPE 3)
    // ================================
    function updateRecap() {
        const recap = document.getElementById("recap");

        const nom = document.querySelector("input[name='nom']").value;
        const prenom = document.querySelector("input[name='prenom']").value;
        const naissance = document.querySelector("input[name='naissance']").value;
        const telephone = document.querySelector("input[name='telephone']").value;
        const email = document.querySelector("input[name='email']").value;

        recap.innerHTML = `
            <div class="recap-block">
                <h4>Informations personnelles</h4>
                <p><strong>Nom :</strong> ${nom}</p>
                <p><strong>Prénom :</strong> ${prenom}</p>
                <p><strong>Date de naissance :</strong> ${naissance}</p>
                <p><strong>Téléphone :</strong> ${telephone}</p>
                <p><strong>Email :</strong> ${email}</p>
            </div>

            <div class="recap-block">
                <h4>Documents transmis</h4>
                <p><strong>Identité :</strong> ${fileStatus("identite")}</p>
                <p><strong>Certificat médical :</strong> ${fileStatus("certificat")}</p>
                <p><strong>Test de français :</strong> ${fileStatus("test_francais")}</p>
                <p><strong>Photo :</strong> ${fileStatus("photo")}</p>
            </div>
        `;
    }


    // Affichage oui/non selon si un fichier est sélectionné
    function fileStatus(inputName) {
        const input = document.querySelector(`[name='${inputName}']`);
        return input && input.files && input.files.length > 0
            ? "✔️ Fichier ajouté"
            : "❌ Aucun fichier";
    }


    // ================================
    //   DÉMARRAGE
    // ================================
    showStep(1);
});
