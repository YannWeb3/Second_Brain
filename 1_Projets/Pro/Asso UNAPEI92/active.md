# Active — Asso UNAPEI92
> Mise à jour : 2026-04-27 (PROD live)

## ✅ Fait
- [x] 15 formulaires HTML complets avec questions RGPD
- [x] Script Google Apps **v2.0** — Onglets créés automatiquement par établissement
- [x] Tous les formulaires utilisent le format array `{id, question, answer}`
- [x] Champ `nom_etablissement` dans tous les formulaires (nomme l'onglet)
- [x] SPREADSHEET_ID configuré
- [x] GOOGLE_SCRIPT_URL dans tous les formulaires
- [x] Page d'accueil index.html avec navigation
- [x] Nettoyage des fichiers obsolètes
- [x] GitHub Pages déployé — formulaires en ligne
- [x] Liens vérifiés et fonctionnels
- [x] Envoi mail aux destinataires effectué

## 🎯 Fonctionnement v2.0
```
Formulaire envoyé
    ↓
nom_etablissement = "IME Les Lilas"
    ↓
Onglet "IME Les Lilas" créé automatiquement (ou réutilisé)
    ↓
Données enregistrées avec colonnes dynamiques
```

**Avantages** :
- Chaque établissement a son propre onglet
- Pas de mélange entre différents IME/SAVS/etc.
- Colonnes créées dynamiquement selon les questions répondues

## 📋 Informations techniques

| Élément | Valeur |
|---------|--------|
| SPREADSHEET_ID | `1yMJI_Nrt6k1EGnkHAbdfj0mc1PFNBsOLUdbu0TpH6b4` |
| Web App URL | `https://script.google.com/macros/s/AKfycbwQBhjBdwuEBtj5Ef63L_5ej3eyXB15DLmpnDBxqM5u0EdVRgoLK6NR1Hkn682obuvN7Q/exec` |
| GitHub Pages | **LIVE** — formulaires en ligne |
| Version | 2.0 (onglets par établissement) — **PROD** |
| Types | 15 formulaires `_RGPD` |
| Mailing destinataires | ✅ Envoyé |

## ⏭️ Prochaines actions
- [ ] **Collecte des réponses** (Avancement actuel : 14/54) — Relancer les établissements en attente
- [ ] **Analyse des résultats** : Extraire les premières tendances des 14 réponses reçues
- [ ] **Entretiens individuels** : Accélérer le rythme (seulement 2 réalisés à ce jour)
- [ ] **Fonctions Support** : Présenter et diffuser le formulaire aux services supports (RH, DAF, Paie, etc.)
- [ ] **Formation** : Préparer les supports de formation basés sur les analyses de l'audit
- [ ] Dashboard GitHub : Mettre à jour et diffuser le fichier `avancement_UNAPEI92.html`

## 📁 Structure finale
```
formulaires/
├── ime.html (61 questions)
├── savs.html
├── sessad.html
├── esat.html
├── eam.html
├── eanm.html
├── cmpp.html
├── si-it.html
├── direction.html
├── qualite.html
├── donateurs.html
├── daf.html
├── rh.html (58 questions - recréé)
├── paie.html
└── communication.html
```
