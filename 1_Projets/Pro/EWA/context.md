# Context — EWA
> Créé le : 2026-04-23

## Profil client
- **Secteur** : Production vidéo / Content creation
- **Taille** : Cabinet (~200-250 clients historiques à importer)
- **Contact principal** : Alex (Agent IA de qualification - Claude 4.5)
- **Canal de communication** : WhatsApp (via Waha VPS) + Email pour notifications

## Mission
- **Objectif** : Système d'automatisation complète pour la gestion de cabinet via WhatsApp + Airtable + n8n
- **Périmètre** :
  - Qualification automatique des prospects (Agent IA)
  - Création dynamique de groupes WhatsApp clients
  - Gestion de projet (onboarding, checklist, validation livrables)
  - Facturation automatique (Tiime) + Rapprochement bancaire (Qonto)
  - Monitoring & continuité de service (backup, alertes)
- **Budget** : ~30€/mois infrastructure (n8n Cloud Pro + Waha VPS + GDrive)
- **Deadline** : Phase 1 TERMINÉE - Dashboard à venir

## Historique
- **2026-04-23** : Création du dossier client
- **2026-03-23** : Point Mission - Validation V1 et packs vidéo (300-450€)
- **2026-03-19** : Début Phase 1 - Architecture WhatsApp + n8n + Airtable

## Notes importantes
- **Stack technique** : Airtable / n8n v2.1.5 (Coolify/Hostinger) / Waha VPS (Hetzner) / Claude 4.5 / RGPD
- **18 workflows n8n** opérationnels répartis sur 5 modules (Qualification, Pilotage Projets, Finance, Ops, Error Handling)
- **Table CONFIG** : Source unique pour prompts, profils WhatsApp (Principal/Backup), et paramètres système
- **Communication** : Transparence IA requise ("Je suis l'assistant EWA...")
- **RGPD** : Consentement clients à vérifier, données historiques à importer sécurisément
