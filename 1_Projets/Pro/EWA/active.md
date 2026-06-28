# Active — EWA
> Mise à jour : 2026-05-11

## Focus actuel
- [x] Phase 1 - Création des 18 workflows n8n
- [x] Table TARIFS créée et configurée
- [x] Accès aux liens Airtable testé et opérationnel
- [ ] Dashboard EWA - Interface de gestion

## Résumé de ce qui a été fait

### Module 1 - Qualification & CRM (5 WFs)
- WF1-Trigger : Trigger & Déduplication messages entrants (Waha Webhook)
- WF2-Qualification : Agent IA Claude 4.5 + LangChain Tools
- WF3-Création-Groupe : Création groupe WhatsApp dynamique
- WF4-Sauvegarde : Sauvegarde conversation Airtable CRM
- WF5-Suivi-Groupe : Suivi automatique des groupes WA

### Module 2 - Pilotage Projets (4 WFs)
- WF-Detection-Validation : Détecte 15 phrases validation
- WF-Alertes-Slack : Alertes projets incomplets (Cron 9h/17h)
- WF-Onboarding : Drive + Demandes rushs quand client Actif
- WF-Checklist : Rappel automatique clients (Cron 1x/heure)

### Module 3 - Finance (3 WFs)
- WF-Facturation : Livrable Approuvé → Facture Pennylane
- WF-Relances : Relances factures impayées (J-3, J+0, J+7, J+14, J+21)
- WF-Banque : Rapprochement bancaire automatique (Webhook Qonto)

### Module 4 - Ops & Resilience (3 WFs)
- WF6-Monitoring : Health check + alertes WhatsApp admin (Cron 5min)
- WF7-Basculement : Basculement Profil WAHA Principal → Backup
- WF8-Communication-Crise : Communication d'urgence aux clients

### Module 5 - Error Handling (1 WF)
- WF-Err-Global : Gestion centralisée des erreurs n8n

### Table TARIFS (Créée le 2026-04-12)
- 6 tarifs configurés : Reel (30€), Ads (30€/15€), VSL (25€/min), Interview (150€), Clipping (15€/10€)
- Intégration LIVRABLES pour calcul auto des prix
- Relation critique : LIVRABLES.Statut "Approuvé" → Facturation Pennylane

## Prochaines actions (Suite au point avec Pacome)
- [x] **Résoudre Auth Google Drive** : Vidéo tuto envoyée à Pacome pour la mise à jour des credentials Google Drive et Gmail dans n8n.
- [x] **Ajuster WF Bot WhatsApp (Scraping prioritaire)** : Le bot ne répond plus automatiquement. Il se contente "d'écouter", d'extraire les infos des messages et de remplir Airtable en arrière-plan. (Voir `Etapes/docs/plans/2026-05-12-n8n-workflow-updates-m1-m2.md`)
- [x] **Modifier Déclencheur Onboarding** : La création du groupe WA et l'onboarding se déclenchent uniquement via un changement de statut ("Actif") sur Airtable OU un message spécifique (texte/vocal) de Pacome ("client validé").
- [ ] **Automatiser Import CSV Qonto** : Créer un workflow n8n qui lit le fichier CSV de Qonto (déposé sur Drive), utilise l'API Claude pour nettoyer les données (dédoublonnage) et mappe les paiements dans Airtable.
- [ ] **Dossier de Test Drive** : Créer un Drive temporaire avec des documents factices (un lien .ssg, un .doc) pour valider l'envoi de documents par mail/WhatsApp.
- [ ] Dashboard EWA - Vue d'ensemble des projets
- [ ] Dashboard EWA - Statistiques en temps réel
- [ ] Dashboard EWA - Gestion des workflows n8n
- [ ] Dashboard EWA - Configuration des profils WAHA

## En attente
- Import des ~200-250 clients historiques
- Migration données existantes vers nouvelle structure
- Tests de charge sur les workflows de qualification
- Validation RGPD pour le traitement des données clients
