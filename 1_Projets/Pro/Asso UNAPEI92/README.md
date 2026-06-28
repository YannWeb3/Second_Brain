# UNAPEI92 - Formulaires en ligne

> 15 formulaires HTML pour la collecte de données interne — Hébergement GitHub Pages + Google Sheets

---

## 📋 Table des matières

1. [État du projet](#État-du-projet)
2. [Prérequis](#prérequis)
3. [Installation Google Sheets](#installation-google-sheets)
4. [Déploiement GitHub Pages](#déploiement-github-pages)
5. [Personnalisation](#personnalisation)
6. [Liste des formulaires](#liste-des-formulaires)

---

## ✅ État du projet

| Élément | Status | Détails |
|---------|--------|---------|
| 15 formulaires HTML | ✅ Complétés | `formulaires/*.html` — format array v2.0 |
| Script Apps Script **v2.0** | ✅ Prêt | Onglets créés **par établissement** |
| SPREADSHEET_ID | ✅ Configuré | `1yMJI_Nrt6k1EGnkHAbdfj0mc1PFNBsOLUdbu0TpH6b4` |
| Web App déployée | ✅ Fait | URL configurée dans tous les formulaires |
| Champ `nom_etablissement` | ✅ Fait | Dans les 15 formulaires |
| Page d'accueil index.html | ✅ Prête | Navigation vers les 15 formulaires |
| Test d'envoi | ⏳ À faire | Vérifier la création d'onglet par établissement |
| GitHub Pages | ⏳ À faire | Créer repo, uploader, activer Pages |

---

## ✅ Fichiers à déployer sur GitHub Pages

Seuls les fichiers suivants sont nécessaires (pour GitHub Pages, tous les fichiers HTML à la racine) :

```
rgpd-2026/  (votre repo GitHub)
├── index.html                    # Page d'accueil
├── ime.html                      # Formulaires à la racine
├── savs.html                     #  (pas de sous-dossier formulaires/)
├── sessad.html                   #  sur GitHub Pages)
├── esat.html
├── eam.html
├── eanm.html
├── cmpp.html
├── si-it.html
├── direction.html
├── qualite.html
├── donateurs.html
├── daf.html
├── rh.html
├── paie.html
├── communication.html
├── google-apps-script.js         # Script Apps Script v2.0
├── README.md                     # Instructions
├── APPS_SCRIPT_DOC.md            # Documentation technique
├── context.md                    # Contexte client
├── active.md                     # Tâches en cours
└── ANALYSE_ARCHITECTURE.md       # Notes architecture
```

> **Note** : Sur GitHub Pages, il est plus simple de mettre tous les fichiers HTML à la racine plutot que dans un sous-dossier `formulaires/`.

**Fichiers obsolètes** (à ne pas déployer) :
- `formulaire-simple.html` — template de départ, doublon des versions finales
- `google-apps-script-reception.js` — ancienne version du script
- `google-script-simple.js` — version simplifiée non utilisée
- `README-SIMPLE.md` — documentation pour version simple (obsolète)
- `README-MISE-EN-PLACE.md` — documentation pour version réception (obsolète)

---

## 🎯 Fonctionnement v2.0 — Onglets par établissement

Cette version crée **automatiquement un onglet par établissement** dans Google Sheets :

```
Google Sheets
├── IME Les Lilas          ← Créé quand le 1er IME remplit
├── IME du Centre          ← Créé quand le 2ème IME remplit
├── SAVS 92                ← Créé quand le 1er SAVS remplit
├── SAVS Sud               ← Créé quand le 2ème SAVS remplit
└── ...
```

**Colonnes fixes** : Date soumission | Type formulaire | Établissement | [questions...]

**Avantages** :
- Chaque établissement isolé dans son propre onglet
- Pas de mélange entre différents établissements du même type
- Colonnes dynamiques : s'adaptent aux questions répondues

---

## ✅ Prérequis

- Un compte **Google** (pour Google Sheets)
- Un compte **GitHub** (gratuit)
- Navigateur web moderne

---

## 🔧 Installation Google Sheets

### Étape 1 : Créer le Google Sheet

1. Allez sur [Google Sheets](https://sheets.google.com)
2. Créez une **nouvelle feuille de calcul vide**
3. Nommez-la : **UNAPEI92_Reponses**

> **Note** : L'ID du spreadsheet est déjà configuré dans les scripts :
> ```
> SPREADSHEET_ID = 1yMJI_Nrt6k1EGnkHAbdfj0mc1PFNBsOLUdbu0TpH6b4
> ```

### Étape 2 : Configurer le script Apps Script

1. Dans votre Google Sheet, cliquez sur **Extensions** > **Apps Script**
2. Supprimez le code par défaut (`function myFunction() {}`)
3. Copiez-collez tout le contenu du fichier `google-apps-script.js` (version **v2.0** — onglets par établissement)
4. **Le SPREADSHEET_ID est déjà configuré** dans le fichier (ligne 37) — aucune modification nécessaire
5. Enregistrez le projet (Ctrl+S) — nommez-le **UNAPEI92_Formulaires**

### Étape 3 : (Optionnel) Tester la configuration

1. Dans l'éditeur Apps Script, vous pouvez exécuter `testerConfiguration()` pour vérifier que tout est correct
2. Autorisez les permissions demandées par Google (première utilisation)

> **Note v2.0** : Les onglets se créent **automatiquement** au premier envoi de chaque établissement. Pas besoin d'initialisation manuelle.

### Étape 4 : Déployer la Web App

1. Cliquez sur **Déployer** > **Nouveau déploiement**
2. Cliquez sur l'icône engrenage (⚙️) et sélectionnez **Application web**
3. Remplissez :
   - **Description** : UNAPEI92 API v2.0
   - **Exécuter en tant que** : Moi
   - **Qui y a accès** : **Tout le monde** (obligatoire pour CORS)
4. Cliquez sur **Déployer**
5. Copiez l'**URL de l'application Web** (elle ressemble à : `https://script.google.com/macros/s/AKfycbw.../exec`)

### Étape 5 : Tester le script (optionnel mais recommandé)

Avant de déployer, vérifiez que tout fonctionne :

1. Dans l'éditeur Apps Script, sélectionnez `testerConfiguration`
2. Cliquez sur **Exécuter** (▶️)
3. Consultez les logs (**Afficher** > **Journaux** ou Ctrl+Entrée)
4. Vous devriez voir : `✓ Configuration validée`

**Test du health check** :
- Ouvrez l'URL de la Web App dans un navigateur
- Vous devriez voir : `{"status":"ok","message":"Service UNAPEI92 actif"...}`

### Étape 6 : Mettre à jour les formulaires HTML

**⚠️ CETTE ÉTAPE EST DÉJÀ FAITE** — Tous les formulaires HTML dans le dossier `formulaires/` ont déjà été configurés avec l'URL de la Web App (lors du déploiement).

Si vous avez besoin de vérifier ou modifier l'URL, ouvrez chaque fichier HTML et cherchez :

```javascript
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwQBhjBdwuEBtj5Ef63L_5ej3eyXB15DLmpnDBxqM5u0EdVRgoLK6NR1Hkn682obuvN7Q/exec';
```

**Note** : Le script supporte automatiquement les formulaires avec des questions différentes. Les nouvelles questions s'ajoutent en colonnes sans décaler les données existantes.

---

## 🚀 Déploiement GitHub Pages

### Étape 1 : Créer un repository GitHub

1. Connectez-vous à [GitHub](https://github.com)
2. Cliquez sur **New** (Nouveau repository)
3. Nommez-le : `unapei92-formulaires`
4. Sélectionnez **Public**
5. Cochez **Add a README file**
6. Cliquez sur **Create repository**

### Étape 2 : Uploader les fichiers

#### Option A — Interface web (simple)

1. Dans votre repository, cliquez sur **Add file** > **Upload files**
2. Glissez-déposez tous les fichiers et dossiers :
   - `index.html`
   - `formulaires/` (dossier complet avec les 16 fichiers HTML)
3. Cliquez sur **Commit changes**

#### Option B — Git (avancé)

```bash
git clone https://github.com/VOTRE_USER/unapei92-formulaires.git
cd unapei92-formulaires
# Copiez vos fichiers ici
git add .
git commit -m "Initial commit - 15 formulaires"
git push origin main
```

### Étape 3 : Activer GitHub Pages

1. Dans votre repository, allez dans **Settings** (⚙️)
2. Dans le menu de gauche, cliquez sur **Pages**
3. Section **Source** :
   - Branch : `main` (ou `master`)
   - Folder : `/ (root)`
4. Cliquez sur **Save**
5. Attendez 1-2 minutes
6. Votre site est accessible à : `https://VOTRE_USER.github.io/unapei92-formulaires/`

---

## 🎨 Personnalisation

### Modifier les champs d'un formulaire

Chaque fichier HTML contient une constante `FORM_CONFIG` :

```javascript
const FORM_CONFIG = {
  type: 'IME',
  title: 'Institut Médico-Éducatif',
  sections: [
    {
      name: 'Identité',
      fields: [
        { name: 'nom', label: 'Nom', type: 'text', required: true },
        { name: 'email', label: 'Email', type: 'email', required: true }
      ]
    }
  ]
};
```

Types de champs disponibles :
- `text` — Texte simple
- `email` — Email (avec validation)
- `tel` — Téléphone
- `number` — Nombre
- `date` — Date
- `textarea` — Zone de texte multiligne
- `select` — Liste déroulante
- `radio` — Boutons radio
- `checkbox` — Cases à cocher

### Modifier les couleurs

Dans la section `<style>` de chaque fichier :

```css
:root {
  --primary: #0055A4;      /* Bleu UNAPEI */
  --primary-dark: #003d7a; /* Bleu foncé */
  --secondary: #E60028;    /* Rouge UNAPEI */
  --bg: #f5f7fa;           /* Fond */
  --text: #333;            /* Texte */
}
```

---

## 📁 Liste des formulaires

| Fichier | Type | Type payload |
|---------|------|--------------|
| `formulaires/ime.html` | IME | `IME_RGPD` |
| `formulaires/savs.html` | SAVS | `SAVS_RGPD` |
| `formulaires/sessad.html` | SESSAD | `SESSAD_RGPD` |
| `formulaires/esat.html` | ESAT | `ESAT_RGPD` |
| `formulaires/eam.html` | EAM | `EAM_RGPD` |
| `formulaires/eanm.html` | EANM | `EANM_RGPD` |
| `formulaires/cmpp.html` | CMPP | `CMPP_RGPD` |
| `formulaires/si-it.html` | SI-IT | `SIIT_RGPD` |
| `formulaires/direction.html` | Direction | `Direction_RGPD` |
| `formulaires/qualite.html` | Qualité | `Qualite_RGPD` |
| `formulaires/donateurs.html` | Donateurs | `Donateurs_RGPD` |
| `formulaires/daf.html` | DAF | `DAF_RGPD` |
| `formulaires/rh.html` | RH | `RH_RGPD` |
| `formulaires/paie.html` | Paie | `Paie_RGPD` |
| `formulaires/communication.html` | Communication | `Communication_RGPD` |

**Total : 15 formulaires**. Tous configurés avec `GOOGLE_SCRIPT_URL` et types `*_RGPD`.

---

## 🔒 Sécurité & Confidentialité

- Les données transitent via HTTPS (GitHub Pages + Google)
- Le Google Sheet doit être configuré avec les bonnes permissions de partage
- Pensez à activer l'authentification à deux facteurs sur votre compte Google

---

## 📞 Support

En cas de problème :
1. Vérifiez l'URL du script Google dans chaque fichier HTML
2. Assurez-vous que la Web App est déployée avec l'accès "Tout le monde"
3. Consultez les logs dans Apps Script (Extensions > Apps Script > Exécutions)

---

**UNAPEI92 — Formulaires v2.0**  
*Dernière mise à jour : 27/04/2026*
