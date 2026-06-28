# ?? Migration Hostinger ? Hetzner
> Infrastructure et services cloud

## ?? Objectif
Migrer l'infrastructure de Hostinger vers Hetzner pour déployer Coolify et n8n,
avec un backup complet des données existantes.

## ?? Statut
- **Phase** : En cours — Serveur provisionné
- **Priorité** : ?? Haute
- **Deadline** : **29/04/2026**
- **Serveur** : Hetzner VPS (204.168.232.97)
- **Coolify** : ? Installé
- **n8n** : ? À installer

## ?? Enjeux
- Downtime à minimiser
- Sauvegarde critique des données
- Continuité des services

## ?? Structure
- [context.md](context.md) — Contexte et plan
- [active.md](active.md) — Tâches en cours
- [coolify_setup.md](coolify_setup.md) — Installation & debug Coolify
- [vps_config.md](vps_config.md) — Installation Hermes Workspace

## ?? Scope
- Migration serveur complet
- Installation Coolify
- Installation n8n
- Configuration applications
- Backup complet

## ?? Planification
- Avant le 27/04 : Backup et préparation
- 27-28/04 : Migration et déploiement
- 29/04 : Validation et tests

## ? Checklist migration
- [ ] Backup complet Hostinger
- [x] Provisionnement Hetzner ? (204.168.232.97)
- [x] Installation Coolify ?
- [ ] Installation n8n
- [ ] Configuration domaine/SSL
- [ ] Tests et validation
