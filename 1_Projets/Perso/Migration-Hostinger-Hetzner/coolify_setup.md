# Coolify — Récap Installation & Debug

## Infos serveur
| Élément | Valeur |
|---------|--------|
| Hébergeur | Hetzner |
| OS | Ubuntu 24 |
| User | `hermes` |
| SSH | port **2222** |
| IP publique | `204.168.232.97` |
| IP WireGuard serveur | `10.10.0.1` |
| IP bridge Docker | `10.0.0.1` |
| Accès Coolify | `https://coolify.iapourasso.com` |

---

## Services qui tournent sur ce serveur

| Service | Container | Accès |
|---------|-----------|-------|
| Coolify | `coolify` | `https://coolify.iapourasso.com` |
| n8n | `n8n-*` | `https://n8nV3.iapourasso.com` |
| OpenClaw | `openclaw-*` | `https://openclaw.iapourasso.com` |
| Hermes workspace | `hermes-workspace-*` | `http://10.10.0.1:3001` (WireGuard) |
| Hermes agent | `hermes-agent-*` | interne (8642) |
| WAHA | `waha-*` | `http://10.10.0.1:3000` (WireGuard) |

---

## Installation Coolify

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | sudo bash
```

Coolify s'installe dans `/data/coolify/`.

### Vérifier que tout tourne
```bash
docker ps | grep coolify
curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:8000
# Attendu : 302
```

### Accès dashboard
Via WireGuard : `http://10.10.0.1:8000`

---

## Problèmes rencontrés & solutions

### 1. Erreur 500 — Password authentication failed (PostgreSQL)

**Cause :** Volume PostgreSQL stale d'une ancienne installation avec des credentials différents.

**Fix :**
```bash
docker stop coolify coolify-db coolify-redis coolify-realtime
docker rm coolify coolify-db coolify-redis coolify-realtime
docker volume rm coolify-db coolify-redis
sudo bash /data/coolify/source/upgrade.sh
```

---

### 2. Validate Server échoue — `No query results for PrivateKey 0`

**Cause :** La clé SSH n'est pas enregistrée dans la base de données Coolify.

**Fix :**
```bash
# Récupérer la clé privée générée par Coolify
sudo cat /data/coolify/ssh/keys/ssh_key@<id>
# (trouver le nom exact avec : sudo find /data/coolify/ssh -type f)
```
Puis dans Coolify UI → **SSH Keys** → **Add SSH Key** → coller le contenu.

---

### 3. Validate Server échoue — `Permission denied (publickey)`

**Cause :** La clé publique Coolify n'est pas dans les authorized_keys du serveur.

**Fix :**
```bash
sudo ssh-keygen -y -f /data/coolify/ssh/keys/ssh_key@<id> >> ~/.ssh/authorized_keys
```

---

### 4. `PermitRootLogin no` — connexion root refusée

**Cause :** SSH root désactivé sur le serveur (config par défaut sécurisée).

**Fix :** Utiliser l'user `hermes` (qui est dans le groupe `docker`) au lieu de `root` dans la config serveur Coolify.

---

### 5. `host.docker.internal` ne résout pas

**Cause :** Sur Linux, `host.docker.internal` n'est pas résolu hors des containers Docker.

**Fix :** Utiliser l'IP du bridge Docker à la place :
```bash
docker network inspect bridge | grep Gateway
# → 10.0.0.1
```
Dans Coolify : **IP Address** → `10.0.0.1`

---

## Configuration serveur dans Coolify

| Champ | Valeur |
|-------|--------|
| IP Address | `10.0.0.1` |
| User | `hermes` |
| Port | `2222` |
| Private Key | clé importée via SSH Keys |

### Tester la connexion SSH manuellement
```bash
sudo ssh -i /data/coolify/ssh/keys/ssh_key@<id> \
  -p 2222 -o StrictHostKeyChecking=no \
  hermes@10.0.0.1 echo "OK"
# Attendu : OK
```

---

### 6. Proxy Traefik — Permission denied

**Cause :** Permissions incorrectes sur `/data/coolify/proxy/` et `/data/coolify/services/`.

**Fix :**
```bash
sudo chmod -R 755 /data/coolify/proxy/
sudo chmod -R 755 /data/coolify/services/
```
Puis relancer **Start Proxy** dans Coolify → Servers → localhost → Proxy.

---

### 7. OpenClaw / n8n — 503 No available server

**Cause :** Les services Coolify utilisent des labels **Caddy** mais le proxy par défaut est **Traefik**. Traefik ne peut pas router vers ces containers.

**Fix :** Switcher le proxy de Traefik vers Caddy :
1. Coolify → **Servers** → **localhost** → onglet **Proxy**
2. **Stop Proxy**
3. Changer le type → **Caddy**
4. **Start Proxy**

---

### 8. Mot de passe Coolify oublié

**Cause :** Permissions incorrectes sur `/data/coolify/proxy/` et `/data/coolify/services/`.

**Fix :**
```bash
sudo chmod -R 755 /data/coolify/proxy/
sudo chmod -R 755 /data/coolify/services/
```
Puis relancer **Start Proxy** dans Coolify → Servers → localhost → Proxy.

---

### 7. Mot de passe Coolify oublié

**Fix :**
```bash
docker exec -it coolify-db psql -U coolify -d coolify -c \
  "UPDATE users SET password = '\$2y\$10\$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi' WHERE id = 1;"
```
Mot de passe temporaire : `password` — à changer immédiatement dans Profile.

---

## Déployer n8n

1. **Projects** → **New Project** → nommer `n8n`
2. **New Resource** → **Service** → choisir **n8n with PostgreSQL**
3. Assigner le domaine `n8n.iapourasso.com`
4. Si erreur `Permission denied` sur le dossier services :
```bash
sudo chmod -R 755 /data/coolify/services/
```

---

## DNS — Enregistrements A à créer chez Hostinger

| Nom | IP |
|-----|----|
| `coolify` | `204.168.232.97` |
| `n8n` | `204.168.232.97` |

Vérifier propagation : `dig <sous-domaine>.iapourasso.com +short`

---

## Réinstallation propre (si tout casse)

```bash
# 1. Stopper et supprimer les containers Coolify
docker stop coolify coolify-db coolify-redis coolify-realtime
docker rm coolify coolify-db coolify-redis coolify-realtime

# 2. Supprimer les volumes
docker volume rm coolify-db coolify-redis

# 3. Réinstaller
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | sudo bash

# 4. Vérifier
docker ps | grep coolify
curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:8000

# 5. Ajouter la clé SSH à hermes
sudo ssh-keygen -y -f $(sudo find /data/coolify/ssh/keys -type f ! -name "*.lock" | head -1) \
  >> ~/.ssh/authorized_keys
```

---

## Commandes utiles

```bash
# Voir tous les containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Voir les ports occupés
sudo ss -tlnp | grep -E ':80|:443|:3000|:3001|:8000|:5678|:9000'

# Logs Coolify
docker logs coolify --tail 50

# Relancer Coolify
sudo bash /data/coolify/source/upgrade.sh

# Trouver la clé SSH Coolify
sudo find /data/coolify/ssh -type f ! -name "*.lock"

# Vérifier la clé publique générée
sudo ssh-keygen -y -f /data/coolify/ssh/keys/ssh_key@<id>
```

---

## Fichiers importants

| Fichier | Rôle |
|---------|------|
| `/data/coolify/source/docker-compose.prod.yml` | Config Docker Coolify |
| `/data/coolify/source/upgrade.sh` | Script de (re)lancement |
| `/data/coolify/ssh/keys/` | Clés SSH générées par Coolify |
| `~/.ssh/authorized_keys` | Clés autorisées sur hermes |