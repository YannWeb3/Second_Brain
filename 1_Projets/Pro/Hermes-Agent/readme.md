# 🤖 Hermes Automation Stack — Guide d'installation

> [!IMPORTANT]
> Ce fichier est dédié à l'**installation initiale** de l'infrastructure depuis zéro. 
> Pour la gestion quotidienne, les adresses IP, l'administration et le dépannage, consultez la source unique de vérité : **[Manuel Complet & Audit](file:///c:/Users/Win10%20Pro%20x64/Desktop/Second_Brain/1_Projets/Pro/Hermes-Agent/hermes-agent-complet.md)**.

Stack d'automatisation IA sur VPS Hetzner (Ubuntu 24) avec Hermes Agent, n8n, OpenClaw, WAHA et Coolify.

---

## 📋 Table des matières

- [Prérequis](#prérequis)
- [Installation complète pas-à-pas](#installation-complète-pas-à-pas)
  - [1. Hermes Workspace](#1-hermes-workspace)
  - [2. Coolify](#2-coolify)
  - [3. Hermes Agent (Connexion)](#3-hermes-workspace--connexion-complète-à-lagent)
  - [4. n8n (via Coolify)](#4-n8n-via-coolify)
  - [5. OpenClaw (via Coolify)](#5-openclaw-via-coolify)
- [Fichiers et arborescence](#fichiers-et-arborescence)
- [Sécurité](#sécurité)

---

## Prérequis

- VPS Ubuntu 24 (Hetzner recommandé, min 4GB RAM, idéalement 8GB)
- Domaine avec accès DNS (ex: Hostinger)
- WireGuard installé sur ta machine locale pour l'accès aux services internes
- Docker & Docker Compose installés sur le serveur

### Installer Docker sur le serveur

```bash
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## Installation complète pas-à-pas

### 1. Hermes Workspace

```bash
cd ~
git clone https://github.com/outsourc-e/hermes-workspace.git
cd hermes-workspace
cp .env.example .env
nano .env
```

#### Variables `.env` critiques à configurer

```env
# LLM Provider
OPENROUTER_API_KEY=sk-or-v1-VOTRE_CLE

# Auth workspace ↔ agent (même valeur obligatoire des deux côtés)
API_SERVER_KEY=hermes_secret_2024
API_SERVER_HOST=0.0.0.0

# Interface web
HERMES_PASSWORD=mot_de_passe_fort

# Désactiver Secure cookie (HTTP sans HTTPS en local/WireGuard)
COOKIE_SECURE=0

# Supabase (si utilisé)
SUPABASE_URL=https://VOTRE_PROJECT.supabase.co
SUPABASE_KEY=VOTRE_SERVICE_ROLE_KEY
SUPABASE_DB_PASSWORD=VOTRE_MOT_DE_PASSE
```

#### Corriger le port (conflit avec WAHA sur 3000)

```bash
sed -i "s/'127.0.0.1:3000:3000'/'10.10.0.1:3001:3000'/" docker-compose.yml
```

#### Lancer le service

```bash
docker compose up -d
```

#### Initialiser le fournisseur LLM

```bash
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes setup
# Choisir OpenRouter, entrer la clé API, répondre "n" au lancement immédiat
docker compose down && docker compose up -d
```

---

### 2. Coolify

#### Installation

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | sudo bash
```

#### Corriger les permissions (nécessaire à chaque install)

```bash
sudo chmod -R 755 /data/coolify/proxy/
sudo chmod -R 755 /data/coolify/services/
```

#### Configuration du serveur localhost dans Coolify

1. Récupérer la clé SSH générée par Coolify :
```bash
sudo find /data/coolify/ssh/keys -type f ! -name "*.lock"
sudo ssh-keygen -y -f /data/coolify/ssh/keys/ssh_key@XXXX >> ~/.ssh/authorized_keys
```

2. Dans Coolify UI → **SSH Keys** → **Add SSH Key** :
```bash
sudo cat /data/coolify/ssh/keys/ssh_key@XXXX
```

3. Dans **Servers** → **localhost** :
   - IP : `10.0.0.1`
   - User : `hermes`
   - Port : `2222`
   - Private Key : sélectionner la clé importée ci-dessus.

4. Activer le proxy : **Servers** → **localhost** → **Proxy** → **Start Proxy** → choisir **Caddy**.

> [!WARNING]
> Utiliser **Caddy** comme proxy, pas Traefik — les services (OpenClaw, n8n) utilisent des labels Caddy.

#### Définir le domaine Coolify

Dans Coolify : **Settings** → **Configuration** → **Instance Domain** → `https://coolify.iapourasso.com`

---

### 3. Hermes Workspace — Connexion complète à l'agent

Le conteneur agent doit lancer à la fois le gateway et le dashboard. Modifier `docker-compose.yml` :

```yaml
# Service hermes-agent — commande
command: ["/bin/sh", "-c", "hermes dashboard --port 9119 --host 0.0.0.0 --insecure & hermes gateway run"]
ports:
  - '8642:8642'
  - '9119:9119'
restart: unless-stopped

# Service hermes-workspace — ajouter dans environment
HERMES_DASHBOARD_URL: http://hermes-agent:9119

# Service hermes-workspace — ajouter volumes
volumes:
  - workspace-hermes:/home/workspace/.hermes

# Section volumes globale
volumes:
  workspace-hermes:
  claude-data:
```

Après le premier démarrage, corriger les permissions :
```bash
docker exec -u root -it hermes-workspace-hermes-workspace-1 chown -R workspace:workspace /home/workspace/.hermes
```

Puis sélectionner un modèle :
```bash
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes model
```

---

### 4. n8n (via Coolify)

1. Dans Coolify : **Projects** → **New Project** → `n8n`
2. **New Resource** → **Service** → **n8n with PostgreSQL**
3. Domaine : `https://n8n.iapourasso.com` (ou `n8nV3.iapourasso.com`)
4. **Deploy**

```bash
# Si erreur Permission denied lors du déploiement
sudo chmod -R 755 /data/coolify/services/
```

---

### 5. OpenClaw (via Coolify)

1. Supprimer l'ancien conteneur si présent sur la machine :
```bash
docker stop openclaw-XXXX && docker rm openclaw-XXXX
```

2. Dans Coolify → **New Resource** → **Service** → **OpenClaw**
3. Domaine : `https://openclaw.iapourasso.com`
4. **Deploy**

#### Récupérer le Gateway Token

```bash
docker exec CONTAINER_OPENCLAW env | grep OPENCLAW_GATEWAY_TOKEN
```
Coller ce token dans OpenClaw → **Control UI Settings** → **Gateway Token**.

#### Configurer le LLM dans OpenClaw

- Provider : OpenRouter
- API Key : `sk-or-v1-VOTRE_CLE`
- Model : `z-ai/glm-4.5-air:free` (gratuit) ou autre.

---

## Fichiers et arborescence

| Fichier | Rôle |
|---------|------|
| `~/hermes-workspace/.env` | Variables Docker (clés API, mots de passe) |
| `~/hermes-workspace/docker-compose.yml` | Config Docker Hermes |
| `/opt/data/.env` | Variables runtime de l'agent (dans le conteneur) |
| `/opt/data/config.yaml` | Config LLM provider de l'agent |
| `/data/coolify/source/docker-compose.prod.yml` | Config Docker interne de Coolify |
| `/data/coolify/source/upgrade.sh` | Script de (re)lancement Coolify |
| `/data/coolify/ssh/keys/` | Clés SSH générées par Coolify |
| `~/.ssh/authorized_keys` | Clés SSH autorisées sur le serveur |

---

## Sécurité

- Ne jamais committer les clés API, mots de passe ou tokens dans Git.
- Utiliser un fichier `.env` local (ajouté au `.gitignore`).
- WireGuard est requis pour accéder aux services internes non exposés.
- Le login root SSH est désactivé (`PermitRootLogin no`).
- Connexion SSH autorisée uniquement sur le port 2222 via l'interface WireGuard.