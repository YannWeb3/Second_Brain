# 🖥️ Récap Installation VPS EWA-prod

## Informations Serveur

| Champ | Valeur |
|---|---|
| Fournisseur | Hetzner Cloud |
| Serveur | CCX33 |
| IP | 167.233.131.89 |
| OS | Ubuntu 24 |
| Nom | EWA-prod |
| Domaine | editingwizardagency.com |
| DNS | OVH |

---

## 1. Connexion SSH

```bash
ssh root@167.233.131.89
```

La clé SSH est sur ton PC dans `~/.ssh/id_ed25519`.

---

## 2. Installation Coolify

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

- Interface Coolify : `http://167.233.131.89:8000`
- Coolify installe automatiquement Docker, Traefik, Redis, PostgreSQL

---

## 3. DNS OVH

Enregistrements de type **A** pointant vers `167.233.131.89` :

| Sous-domaine | Type | Cible |
|---|---|---|
| `coolify` | A | `167.233.131.89` |
| `n8n` | A | `167.233.131.89` |
| `waha` | A | `167.233.131.89` |
| `waha2` | A | `167.233.131.89` |

---

## 4. Firewall Hetzner

Règles **Inbound** :

| Port | Protocole | Usage |
|---|---|---|
| 22 | TCP | SSH |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |

Outbound : tout autoriser.

---

## 5. n8n (with PostgreSQL and Worker)

**Déployé via** : Coolify → New Resource → Service → n8n with PostgreSQL and Worker

**Domaine** : `https://n8n.editingwizardagency.com`

**Credentials PostgreSQL** (générés par Coolify, à retrouver dans Coolify → Service → Environment) :
- User : voir Coolify
- Database : `n8n`
- Password : voir Coolify

**Stack** :
- n8n
- n8n Worker
- Task Runners
- PostgreSQL 16
- Redis 6

**Notes** :
- Le champ Domains se configure au niveau du service N8N principal
- Pas besoin de spécifier le port 5678 dans l'URL, Traefik route automatiquement
- Certificat SSL généré automatiquement par Let's Encrypt via Traefik

---

## 6. Waha #1

**Déployé via** : Coolify → New Resource → Docker Compose

**Docker Compose** :
```yaml
services:
  waha:
    image: devlikeapro/waha
    restart: always
    volumes:
      - 'waha_data:/app/.sessions'
volumes:
  waha_data: null
```

**Domaine** : `https://waha.editingwizardagency.com`

**Variables d'environnement** :
```
WAHA_API_KEY=EWAWaha1Prod2026SecureKey
WAHA_API_KEY_PLAIN=EWAWaha1Prod2026SecureKey
WAHA_DASHBOARD_USERNAME=ewa_admin
WAHA_DASHBOARD_PASSWORD=EWAWaha1Prod2026Pass
WHATSAPP_SWAGGER_USERNAME=ewa_admin
WHATSAPP_SWAGGER_PASSWORD=EWAWaha1Prod2026Pass
WAHA_BASE_URL=https://waha.editingwizardagency.com
WAHA_PUBLIC_URL=https://waha.editingwizardagency.com
```

> ⚠️ **Important** : Toujours mettre `WAHA_API_KEY` ET `WAHA_API_KEY_PLAIN` avec la même valeur, sinon l'authentification échoue.

**Test API** :
```bash
curl -H "X-Api-Key: EWAWaha1Prod2026SecureKey" https://waha.editingwizardagency.com/api/server/status
```

---

## 7. Waha #2

**Déployé via** : Coolify → New Resource → Docker Compose

**Docker Compose** :
```yaml
services:
  waha2:
    image: devlikeapro/waha
    restart: always
    volumes:
      - 'waha2_data:/app/.sessions'
volumes:
  waha2_data: null
```

**Domaine** : `https://waha2.editingwizardagency.com`

**Variables d'environnement** :
```
WAHA_API_KEY=EWAWaha2Prod2026SecureKey
WAHA_API_KEY_PLAIN=EWAWaha2Prod2026SecureKey
WAHA_DASHBOARD_USERNAME=ewa_admin
WAHA_DASHBOARD_PASSWORD=EWAWaha2Prod2026Pass
WHATSAPP_SWAGGER_USERNAME=ewa_admin
WHATSAPP_SWAGGER_PASSWORD=EWAWaha2Prod2026Pass
WAHA_BASE_URL=https://waha2.editingwizardagency.com
WAHA_PUBLIC_URL=https://waha2.editingwizardagency.com
```

**Test API** :
```bash
curl -H "X-Api-Key: EWAWaha2Prod2026SecureKey" https://waha2.editingwizardagency.com/api/server/status
```

---

## 8. Vérification générale

```bash
# Vérifier tous les conteneurs
docker ps

# Vérifier les logs Traefik
docker logs coolify-proxy 2>&1 | tail -50

# Tester n8n
curl https://n8n.editingwizardagency.com

# Tester Waha #1
curl -H "X-Api-Key: EWAWaha1Prod2026SecureKey" https://waha.editingwizardagency.com/api/server/status

# Tester Waha #2
curl -H "X-Api-Key: EWAWaha2Prod2026SecureKey" https://waha2.editingwizardagency.com/api/server/status
```

---

## 9. Services en production

| Service | URL | Stack |
|---|---|---|
| Coolify | `http://167.233.131.89:8000` | ✅ |
| n8n | `https://n8n.editingwizardagency.com` | ✅ |
| Waha #1 | `https://waha.editingwizardagency.com/dashboard` | ✅ |
| Waha #2 | `https://waha2.editingwizardagency.com/dashboard` | ✅ |

---

## 10. À faire (prochaines étapes)

- [ ] Wireguard (accès sécurisé VPN)
- [ ] Claude Code (connexion au VPS)
- [ ] Backup Hetzner (activé, vérifier la config)
- [ ] Changer les mots de passe par défaut après installation
- [ ] Configurer les webhooks n8n avec les URLs Waha

---

*Généré le 17 juin 2026*
