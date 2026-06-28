# 🗂️ Index — Asso UNAPEI92
> GitHub Pages + Google Sheets | 15 formulaires HTML | **v2.0 — Onglets par établissement**

## Fichiers

| Fichier | Rôle |
|---------|------|
| `context.md` | Profil client, mission, historique |
| `active.md` | Tâches en cours et focus |
| `README.md` | Instructions de déploiement |
| `APPS_SCRIPT_DOC.md` | Documentation complète du script Apps Script |
| `google-apps-script.js` | Script serveur Google (**v2.0** — onglets par établissement) |
| `index.html` | Page d'accueil avec liens vers les formulaires |

## Formulaires (16)

| Formulaire | Type | Fichier |
|------------|------|---------|
| IME | Institut Médico-Éducatif | `formulaires/ime.html` |
| SAVS | Service d'Accompagnement à la Vie Sociale | `formulaires/savs.html` |
| SESSAD | Service d'Éducation Spéciale et de Soins à Domicile | `formulaires/sessad.html` |
| ESAT | Établissement et Service d'Aide par le Travail | `formulaires/esat.html` |
| EAM | Établissement d'Accueil Médicalisé | `formulaires/eam.html` |
| EANM | Établissement d'Accueil Non Médicalisé | `formulaires/eanm.html` |
| CMPP | Centre Médico-Psycho-Pédagogique | `formulaires/cmpp.html` |
| EMMA-H | Équipe Mobile Maintien à Domicile (+45 ans) | `formulaires/emma-h.html` |
| SI-IT | Service Informatique & IT | `formulaires/si-it.html` |
| Direction | Direction générale | `formulaires/direction.html` |
| Qualité | Service Qualité | `formulaires/qualite.html` |
| Donateurs-Adhérents | Gestion des donateurs et adhérents | `formulaires/donateurs.html` |
| DAF | Direction Administrative et Financière | `formulaires/daf.html` |
| RH | Ressources Humaines | `formulaires/rh.html` |
| Paie | Service Paie | `formulaires/paie.html` |
| Communication | Service Communication | `formulaires/communication.html` |

## Structure

```
Asso UNAPEI92/
├── context.md
├── active.md
├── index.md
├── README.md
├── google-apps-script.js        (v1.1 PROD — seul script à déployer)
├── index.html
└── formulaires/
    ├── ime.html (type: IME_RGPD)
    ├── savs.html (type: SAVS_RGPD)
    ├── sessad.html (type: SESSAD_RGPD)
    ├── esat.html (type: ESAT_RGPD)
    ├── eam.html (type: EAM_RGPD)
    ├── eanm.html (type: EANM_RGPD)
    ├── cmpp.html (type: CMPP_RGPD)
    ├── emma-h.html (type: EMMAH_RGPD)
    ├── si-it.html (type: SIIT_RGPD)
    ├── direction.html (type: Direction_RGPD)
    ├── qualite.html (type: Qualite_RGPD)
    ├── donateurs.html (type: Donateurs_RGPD)
    ├── daf.html (type: DAF_RGPD)
    ├── rh.html (type: RH_RGPD)
    ├── paie.html (type: Paie_RGPD)
    └── communication.html (type: Communication_RGPD)
```

## Notes v2.0

- **Format d'envoi** : Array `[{id, question, answer}]` pour tous les formulaires
- **Création d'onglets** : Automatique, un onglet par valeur de `nom_etablissement`
- **Colonnes** : `Date soumission | Type formulaire | Établissement | [questions...]`
- **Gestion dynamique** : Nouvelles colonnes ajoutées automatiquement si nouvelles questions
- Tous les formulaires utilisent le suffixe `_RGPD` pour le type
- Le script Apps Script accepte à la fois les types `XXX` et `XXX_RGPD`
- `formulaire-simple.html` supprimé (template de développement)
- Scripts obsolètes supprimés : `google-apps-script-reception.js`, `google-script-simple.js`
- Docs obsolètes supprimées : `README-SIMPLE.md`, `README-MISE-EN-PLACE.md`

## Fonctionnalités des formulaires

- ✅ Navigation par blocs nommés (sans numérotation visible)
- ✅ Design responsive avec charte UNAPEI (bleu #0055A4)
- ✅ Champs texte, email, date, nombre, textarea
- ✅ Listes déroulantes, boutons radio, cases à cocher
- ✅ Envoi des données vers Google Sheets via Apps Script
- ✅ Messages de confirmation/erreur
- ✅ Date par défaut = aujourd'hui

## Déploiement

Voir `README.md` pour les instructions complètes de :

1. Configuration Google Apps Script
2. Déploiement GitHub Pages
3. Personnalisation des formulaires

## Propositions

| Document | Description |
|---|---|
| `UNAPEI92_RGPD_3approches.md` | Trois approches pour former le personnel RGPD |
| `formation_RGPD.html` | Kit de formation interne (HTML slider) |
| `journal_incidents_rgpd.html` | Journal d'incidents RGPD |
| `Fiche_Reflexe_RGPD_UNAPEI92.docx` | Fiche réflexe RGPD (Word) |
