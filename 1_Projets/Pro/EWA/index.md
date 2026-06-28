# 🗂️ Index — EWA
> Production vidéo | ~200-250 clients | WhatsApp + n8n + Airtable

## Fichiers

| Fichier | Rôle |
|---------|------|
| `context.md` | Profil client, mission, historique |
| `active.md` | Tâches en cours et focus |

## Stack technique

- **Airtable** — Base de données clients & projets
- **n8n v2.1.5** — 18 workflows opérationnels (Coolify/Hostinger)
- **Waha VPS** — WhatsApp API (Hetzner)
- **Claude 4.5** — Agent IA de qualification (Alex)

## Modules n8n (5)

1. **Qualification** — Agent IA Alex, scoring prospects
2. **Pilotage Projets** — Onboarding, checklists, validation livrables
3. **Finance** — Facturation Tiime, rapprochement Qonto
4. **Ops** — Gestion groupes WhatsApp, backups
5. **Error Handling** — Monitoring, alertes, retry

## Structure

```
EWA/
├── context.md    → Profil client complet
├── active.md     → Focus et tâches en cours
└── index.md      → Ce fichier
```
