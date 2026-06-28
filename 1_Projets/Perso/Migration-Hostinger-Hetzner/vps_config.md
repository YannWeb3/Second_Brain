# Hermes Workspace — Récap Installation (5 min)

## Infos serveur
| Élément | Valeur |
|---------|--------|
| Hébergeur | Hetzner |
| OS | Ubuntu 24 |
| User | `hermes` |
| SSH | port **2222** |
| IP publique | `204.168.232.97` |
| IP WireGuard serveur | `10.10.0.1` |
| IP WireGuard client | `10.10.0.2` |
| Accès UI | `http://10.10.0.1:3001` |

---

## Installation en 5 min

```bash
cd ~
git clone https://github.com/outsourc-e/hermes-workspace.git
cd hermes-workspace
cp .env.example .env
# Configurer le .env avec les clés API
```

### Contenu `.env` critique

```env
OPENROUTER_API_KEY=sk-or-v1-...
OPENAI_API_KEY=sk-...
API_SERVER_KEY=hermes_sec...
API_SERVER_HOST=0.0.0.0
HERMES_PASSWORD=ton_mot_de_passe_fort
COOKIE_SECURE=0
```

### Correction du Port (Conflit WAHA)

```bash
sed -i "s/'127.0.0.1:3000:3000'/'10.10.0.1:3001:3000'/" docker-compose.yml
```

### Lancement

```bash
docker compose up -d
```

### Setup LLM provider dans l'agent

```bash
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes setup
# Choisir OpenRouter, entrer la clé, répondre n au lancement immédiat
```

```bash
docker compose down && docker compose up -d
```

---

## Points d'attention (Troubleshooting)

| Problème | Cause | Solution |
|----------|-------|----------|
| `port 3000 already allocated` | WAHA occupe le 3000 | `sed` sur docker-compose.yml → port 3001 |
| `Exited (1)` au démarrage | `HERMES_PASSWORD` absent | Ajouter dans `.env` |
| `HTTP 401` sur le backend | `API_SERVER_HOST=127.0.0.1` par défaut | Mettre `API_SERVER_HOST=0.0.0.0` + `API_SERVER_KEY` |
| Login en boucle | Cookie Secure sur HTTP | Ajouter `COOKIE_SECURE=0` dans `.env` |
| `hermes: not found` | Pas dans $PATH | Utiliser `/opt/hermes/.venv/bin/hermes` |

---

## Commandes utiles

```bash
# Logs
docker compose logs hermes-workspace
docker compose logs hermes-agent | tail -30

# Redémarrer
docker compose down && docker compose up -d

# Vérifier ports
sudo ss -tlnp | grep :3001
```

---

## Accès

- **Via WireGuard** : `http://10.10.0.1:3001`
- **Via Tunnel SSH** : `ssh -p 2222 -L 3001:127.0.0.1:3001 hermes@204.168.232.97` puis `http://localhost:3001`

---

## TODO — Telegram

Ajouter dans `/opt/data/.env` du container :
```bash
docker exec -it hermes-workspace-hermes-agent-1 bash -c \
  "echo 'GATEWAY_ALLOW_ALL_USERS=true' >> /opt/data/.env"
```
Puis redémarrer.

---

## Permissions & Credentials

### Architecture des permissions (Option B — équilibre sécurité/praticité)

| Fichier/Dossier | Propriétaire | Modifiable depuis Telegram |
|-----------------|--------------|---------------------------|
| `/opt/data/.env` | root | ❌ Non |
| `/opt/data/config.yaml` | root | ❌ Non |
| `/opt/data/memory/` | hermes | ✅ Oui |
| `/opt/data/skills/` | hermes | ✅ Oui |

### Mots de passe d'application (Credentials externes)

- **Yannstory** : `vxsz sgzb rszp widp`

### Appliquer les permissions (après chaque réinstall)

```bash
docker exec -u root hermes-workspace-hermes-agent-1 bash -c \
  "mkdir -p /opt/data/memory /opt/data/skills && \
   chown -R hermes:hermes /opt/data/memory /opt/data/skills"
```

### Ajouter un token/API key dans /opt/data/.env

```bash
docker exec -u root hermes-workspace-hermes-agent-1 sh -c \
  "echo 'MA_VARIABLE=ma_valeur' >> /opt/data/.env"
```

### Vérifier les clés présentes (sans afficher les valeurs)

```bash
docker exec -u root hermes-workspace-hermes-agent-1 sh -c \
  "grep -o '^[^=]*' /opt/data/.env"
```

### Éditeur non disponible dans le container

`nano` absent — utiliser soit la commande echo ci-dessus, soit :
```bash
sudo nano $(docker volume inspect hermes-workspace_claude-data \
  | grep Mountpoint | cut -d'"' -f4)/.env
```

---

## Mises à jour

### Mettre à jour Hermes Workspace

```bash
cd ~/hermes-workspace
docker compose pull
docker compose down && docker compose up -d
```

### Mettre à jour l'image Hermes Agent

```bash
docker pull nousresearch/hermes-agent:latest
docker compose down && docker compose up -d
```

### Après chaque mise à jour — vérifier

```bash
# Permissions toujours OK ?
docker exec hermes-workspace-hermes-agent-1 ls -la /opt/data/

# Config LLM toujours là ?
docker exec -u root hermes-workspace-hermes-agent-1 sh -c \
  "grep -o '^[^=]*' /opt/data/config.yaml | head -5"

# Tout tourne ?
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### ⚠️ Points d'attention après mise à jour

- Vérifier que `allowed_chats` est toujours dans `config.yaml`
- Vérifier les permissions sur `memory/` et `skills/`
- Si login en boucle → vérifier `COOKIE_SECURE=0` dans `.env`
- Si HTTP 401 → vérifier `API_SERVER_HOST=0.0.0.0` dans `.env`