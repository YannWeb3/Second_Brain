# Migrer T460s Windows 10 → Ubuntu
> Dernière mise à jour : 2026-06-29

## Contexte
ThinkPad T460s — impossible de passer à Windows 11 (CPU non supporté). Décision de migrer vers Ubuntu en clean install.

## Statut
- [x] Audit espace disque initial (210,5 Go / 250 Go utilisés)
- [x] Nettoyage : PlariumPlay (17 Go), Temp (7 Go), Chrome cache (17 Go), npm/pip cache
- [x] Suppression vidéos antérieures à 2026 (17 Go récupérés)
- [x] Suppression caches apps inutilisables sous Ubuntu (Discord, Zoom, Dropbox, Firefox, WisprFlow, etc.)
- [ ] Backup données essentielles sur disque externe
- [ ] Création clé USB Ubuntu bootable
- [ ] Installation Ubuntu (clean install)
- [ ] Restauration fichiers et configs

## Progression disque
| Étape | Utilisé | Libre | Gain |
|-------|---------|-------|------|
| Initial | 210,5 Go | 26,8 Go | — |
| Après nettoyage | 158,6 Go | 78,7 Go | ~52 Go récupérés |

## Fichiers à sauvegarder
- Desktop : projets actifs (EWA, Pilotage_Coach, n8n back up, Coach_Setter, etc.)
- Documents\Ianne (9,5 Go — à vérifier)
- Second Brain complet (ce dépôt Git)
- Profils Chrome/Firefox ? (historique/mots de passe)

## Notes
- Le SSD 250 Go du T460s suffit amplement pour Ubuntu propre
- Backup obligatoire avant clean install
- Vérifier compatibilité Ubuntu 24.04 LTS avec T460s (tout OK : Intel 6e gen, carte Intel WiFi)

## Références
- Ubuntu 24.04 LTS : https://ubuntu.com/download
- T460s specs : Intel i5-6300U, 12 Go RAM, SSD 250 Go
