# Context — Asso UNAPEI92
> Créé le : 2026-04-23

## Profil client
- **Secteur** : Association — Accompagnement personnes handicapées
- **Taille** : Multi-établissements (IME, SAVS, SESSAD, ESAT, etc.)
- **Contact principal** : Association UNAPEI 92
- **Canal de communication** : Email

## Mission
- **Objectif** : Créer 15 formulaires HTML dédiés (un par type d'établissement/service) pour collecter des données internes
- **Périmètre** :
  - 15 formulaires HTML responsive et professionnels
  - Navigation par blocs nommés (sans numérotation visible)
  - Stockage des réponses dans Google Sheets centralisé
  - Hébergement via GitHub Pages (gratuit)
- **Budget** : Gratuit (GitHub Pages + Google Sheets)
- **Deadline** : Livraison immédiate

## Types d'établissements/services (16 formulaires)

| Type | Description |
|------|-------------|
| IME | Institut Médico-Éducatif |
| SAVS | Service d'Accompagnement à la Vie Sociale |
| SESSAD | Service d'Éducation Spéciale et de Soins à Domicile |
| ESAT | Établissement et Service d'Aide par le Travail |
| EAM | Établissement d'Accueil Médicalisé |
| EANM | Établissement d'Accueil Non Médicalisé |
| CMPP | Centre Médico-Psycho-Pédagogique |
| EMMA-H | Équipe Mobile de Maintien à Domicile (+45 ans) |
| SI-IT | Service Informatique & IT |
| Direction | Direction générale |
| Qualité | Service Qualité |
| Donateurs-Adhérents | Gestion des donateurs et adhérents |
| DAF | Direction Administrative et Financière |
| RH | Ressources Humaines |
| Paie | Service Paie |
| Communication | Service Communication |

## Stack technique

- **Frontend** : HTML5 + CSS3 vanilla (responsive)
- **Backend** : Google Apps Script (Web App) v1.1 PROD
- **Stockage** : Google Sheets (1 fichier, 16+ onglets)
- **Hébergement** : GitHub Pages (gratuit, HTTPS)

### Fonctionnalités du script Apps Script

| Fonctionnalité | Description |
|----------------|-------------|
| Gestion dynamique des colonnes | Ajoute automatiquement les nouvelles questions sans décaler les données |
| Validation des types | Sécurité : accepte uniquement les types de formulaires configurés |
| Health check | Endpoint `/` (GET) pour vérifier l'état du service |
| CORS complet | Support des requêtes cross-origin (POST, GET, OPTIONS) |
| Formatage auto | Dates formatées, textes tronqués si > 50000 caractères |
| En-têtes stylisés | Ligne d'en-tête en bleu UNAPEI avec texte blanc |

## Structure du livrable

```
Asso UNAPEI92/
├── README.md                    → Instructions déploiement
├── google-apps-script.js        → Script serveur
├── index.html                   → Page d'accueil avec liens
└── formulaires/
    ├── ime.html
    ├── savs.html
    ├── sessad.html
    ├── esat.html
    ├── eanm.html
    ├── eam.html
    ├── cmpp.html
    ├── emma-h.html
    ├── si-it.html
    ├── direction.html
    ├── qualite.html
    ├── donateurs.html
    ├── daf.html
    ├── rh.html
    ├── paie.html
    └── communication.html
```

## Historique
- **2026-04-23** : Création du dossier client + livraison formulaires complets
- **2026-04-24** : Mise à jour script Apps Script v1.1 PROD (gestion dynamique des colonnes, health check, CORS amélioré)
- **2026-04-24** : Formulaire IME enrichi avec 61 questions RGPD détaillées
- **2026-04-28** : Ajout formulaire EMMA-H (Équipe Mobile Maintien à Domicile +45 ans) avec 40+ questions RGPD

## Notes importantes
- Les formulaires utilisent une navigation par blocs nommés (pas de numéros visibles)
- Design professionnel avec la charte UNAPEI (bleu #0055A4)
- Les réponses sont envoyées vers Google Sheets via requête POST
- Chaque type a son propre onglet dans le Google Sheet central
