# 🦅 Hermes Agent — Manuel Complet & Audit
*Dernière mise à jour consolidée : 18/05/2026*

Ce document regroupe l'architecture, les accès quotidiens, la configuration technique, l'audit du système, les mises à jour et le guide de dépannage complet. **Source unique de vérité au quotidien.**

> [!NOTE]
> - Pour l'architecture IA (les 8 profils d'agents, leurs prompts `SOUL.md` et le moteur Kanban), consultez **[Hermes.md](file:///c:/Users/Win10%20Pro%20x64/Desktop/Second_Brain/Hermes.md)**.
> - Pour l'installation initiale du serveur ou le déploiement pas-à-pas de nouveaux services, référez-vous au **[README Global](file:///c:/Users/Win10%20Pro%20x64/Desktop/Second_Brain/1_Projets/Pro/Hermes-Agent/readme.md)**.
> - Pour le profil de l'utilisateur (Yann) et la stratégie métier, référez-vous à **[User.md](file:///c:/Users/Win10%20Pro%20x64/Desktop/Second_Brain/User.md)**.

---

## 🎯 1. Stratégie & Objectifs
Stack agentique légère, stable et optimisée pour un coût maîtrisé.
- **Budget cible :** < 20€/mois (Réel estimé : 5-8€/mois).
- **Interface :** Telegram.
- **Optimisation :** Réduction drastique des tokens (Passage de 20k+ à ~9k de baseline).

### Décisions Modèles (OpenRouter)
| Rôle | Modèle Principal | Fallback / Secondaire |
| :--- | :--- | :--- |
| **Orchestrateur (Limu)** | `tencent/hy3-preview` | `deepseek/deepseek-v4-flash` |
| **Architecte / Review** | `google/gemma-4-26b-a4b-it` | `nvidia/nemotron-3-super-120b:free` |
| **Code / Supabase** | `deepseek/deepseek-v4-flash` | `qwen/qwen3-coder:free` |
| **Audit / Mail** | `inclusionai/ling-2.6-flash` | `google/gemma-4-31b-it:free` |
| **Recherche** | `google/gemma-4-31b-it:free` | `gemini-2.5-flash-lite` |

---

## 🌐 2. Accès & Infrastructure
Le serveur est hébergé chez **Hetzner** sous **Ubuntu 24** (8GB RAM).
- **Utilisateur principal :** `hermes` (droits sudo et groupe docker).
- **IP Publique du serveur :** `204.168.232.97`
- **Réseau interne WireGuard :** `10.10.0.1` (serveur) / `10.10.0.2` (client)
- **Pont réseau Docker :** `10.0.0.1`

### Connexions au serveur
```bash
# 1. SSH via WireGuard (Méthode recommandée)
ssh -p 2222 hermes@204.168.232.97

# 2. Accès de secours via tunnel SSH (si accès interne bloqué)
# Pour Hermes Workspace interne (port 3001) :
ssh -p 2222 -L 3001:127.0.0.1:3001 hermes@204.168.232.97
# Puis ouvrir http://localhost:3001 sur la machine locale

# Pour le dashboard interne Coolify (port 8000) :
ssh -p 2222 -L 8000:127.0.0.1:8000 hermes@204.168.232.97
# Puis ouvrir http://localhost:8000
```

### Cartographie des Services
| Service | URL / Accès | Note |
| :--- | :--- | :--- |
| **Coolify** | [coolify.iapourasso.com](https://coolify.iapourasso.com) | Dashboard de gestion (HTTPS public) |
| **n8n** | [n8nV3.iapourasso.com](https://n8nV3.iapourasso.com) | Automatisations (HTTPS public) |
| **OpenClaw** | [openclaw.iapourasso.com](https://openclaw.iapourasso.com) | Interface IA (HTTPS public) |
| **Hermes Workspace** | `http://10.10.0.1:3001` | Accès réservé WireGuard |
| **Hermes Agent** | `http://10.10.0.1:8642` | Accès réservé WireGuard |
| **WAHA (WhatsApp)** | `http://10.10.0.1:3000` | Accès réservé WireGuard (Session `default`) |

### DNS — Enregistrements Hostinger (A)
Tous configurés vers l'IP publique `204.168.232.97` (TTL 300) :
- `coolify`
- `n8n` (et/ou `n8nV3`)
- `openclaw`

```bash
# Vérification de la propagation DNS
dig coolify.iapourasso.com +short
```

---

## 🧠 3. Architecture Mémoire & IA
Configuration optimisée pour réduire la consommation de tokens.

### Limites de Context (Config Globale)
- `memory_char_limit`: **800** (était 2200)
- `user_char_limit`: **400** (était 1375)
- `max_turns`: **20** (était 120)
- `protect_last_n`: **6**
- `reasoning_effort`: **low** (sauf orchestrateur explicite)

### Structure des fichiers mémoire
1. **`MEMORY.md`** : Faits de session et crons actifs (géré automatiquement).
2. **`SOUL.md`** : Identité d'Alex et règles d'or (ne jamais faire de `ls` récursif, < 5 lignes de réponse).
3. **`active.md`** : Focus de la semaine (lu 1 seule fois par session).
4. **`ROUTING.md`** : Cartographie des modèles par agent.

---

## 🛠️ 4. Commandes de Survie (Cheatsheet)

### Administration Docker & Services
```bash
# Statut clair et rapide des conteneurs
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Voir les ports occupés sur le serveur
sudo ss -tlnp | grep -E ':80|:443|:3000|:3001|:8000|:5678|:8082'

# Voir les logs d'Hermes Agent en temps réel
docker compose -f ~/hermes-workspace/docker-compose.yml logs hermes-agent --tail 30

# Voir les logs de Coolify
docker logs coolify --tail 50

# Redémarrer entièrement Hermes Workspace et Agent
cd ~/hermes-workspace && docker compose down && docker compose up -d

# Relancer ou mettre à jour Coolify en ligne de commande
sudo bash /data/coolify/source/upgrade.sh

# Tester la réponse locale de Coolify (attendu : HTTP 302)
curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:8000
```

### Configuration & Maintenance IA
```bash
# Vérifier la configuration LLM active d'Hermes Agent
docker exec -it hermes-workspace-hermes-agent-1 cat /opt/data/config.yaml

# Relancer le wizard de setup LLM d'Hermes
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes setup

# Mettre à jour le Token GitHub dans le conteneur agent
docker exec -it hermes-workspace-hermes-agent-1 bash -c \
  "git config --global credential.helper store && \
   echo 'https://TON_USER:ghp_TON_TOKEN@github.com' > ~/.git-credentials"

# Créer / cloner les profils agents par défaut
docker exec -it hermes-workspace-hermes-agent-1 bash -c "
  /opt/hermes/.venv/bin/hermes profile create orchestrateur --clone &&
  /opt/hermes/.venv/bin/hermes profile create code --clone &&
  /opt/hermes/.venv/bin/hermes profile create audit --clone
"

# Trouver la clé SSH générée par Coolify
sudo find /data/coolify/ssh/keys -type f ! -name "*.lock"

# Retrouver le Gateway Token d'OpenClaw
docker exec CONTAINER_OPENCLAW env | grep OPENCLAW_GATEWAY_TOKEN
```

### Script de changement rapide du modèle de Fallback
```bash
MOUNTPOINT=$(docker volume inspect hermes-workspace_claude-data | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['Mountpoint'])")
sudo python3 -c "
import re
with open('$MOUNTPOINT/config.yaml', 'r') as f:
    content = f.read()
content = re.sub(r'(fallback_model:\n  provider: )\S+(\n  model: )\S+', r'\1openrouter\2ID_DU_MODELE', content)
with open('$MOUNTPOINT/config.yaml', 'w') as f:
    f.write(content)
"
```

---

## 🚑 5. Maintenance & Troubleshooting

### Hermes Agent ne démarre pas ou tourne en boucle
| Symptôme / Erreur | Cause | Solution |
| :--- | :--- | :--- |
| `port 3000 already allocated` | Conflit avec le port 3000 de WAHA | Modifier `docker-compose.yml` pour utiliser le port `3001` (`10.10.0.1:3001:3000`) |
| `Exited (1)` au lancement | Mot de passe manquant | Ajouter `HERMES_PASSWORD=mot_de_passe_fort` dans `~/hermes-workspace/.env` |
| `HTTP 401 Unauthorized` | Mauvaise écoute de l'API | Définir `API_SERVER_HOST=0.0.0.0` et vérifier l'exactitude de `API_SERVER_KEY` |
| Boucle infinie à la connexion | Problème de cookie sécurisé sans HTTPS | Ajouter `COOKIE_SECURE=0` dans le fichier `.env` |
| Commande `hermes: not found` | Exécutable hors du $PATH | Appeler directement `/opt/hermes/.venv/bin/hermes` |

### Problèmes Coolify courants
- **Erreur 500 / Postgres stale (mot de passe échoué) :** Supprimer les volumes résiduels (`coolify-db` et `coolify-redis`) et relancer l'installation :
  ```bash
  docker stop coolify coolify-db coolify-redis coolify-realtime
  docker rm coolify coolify-db coolify-redis coolify-realtime
  docker volume rm coolify-db coolify-redis
  sudo bash /data/coolify/source/upgrade.sh
  ```
- **Permission Denied sur Proxy / Services :** Réparer les droits d'accès sur le système hôte :
  ```bash
  sudo chmod -R 755 /data/coolify/proxy/
  sudo chmod -R 755 /data/coolify/services/
  ```
- **Erreur `No query results for PrivateKey 0` (Validation serveur) :** La clé SSH n'est pas dans la base de Coolify. Copier le contenu avec `sudo cat /data/coolify/ssh/keys/ssh_key@XXXX` et l'ajouter manuellement dans Coolify UI → **SSH Keys**.
- **Mot de passe administrateur Coolify perdu :** Réinitialiser directement dans la base de données :
  ```bash
  docker exec -it coolify-db psql -U coolify -d coolify -c \
    "UPDATE users SET password = '\$2y\$10\$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi' WHERE id = 1;"
  ```
  Le mot de passe redevient alors temporairement `password`.

### Connectivité & Services Web
- **Erreur 503 (No available server) sur n8n / OpenClaw :** Les conteneurs utilisent des labels spécifiques à Caddy. Vérifier dans Coolify que le proxy du serveur localhost est bien configuré sur **Caddy** (et non Traefik ou Nginx).
- **Problème de résolution `host.docker.internal` sous Linux :** Utiliser l'adresse IP de la passerelle Docker (`10.0.0.1`) pour les communications inter-conteneurs.
  ```bash
  docker network inspect bridge | grep Gateway
  ```

### Connexions API Tiers (Telegram & Supabase)
- **Telegram "not authorized" :** Autoriser tous les utilisateurs sur la gateway :
  ```bash
  docker exec -it hermes-workspace-hermes-agent-1 bash -c "echo 'GATEWAY_ALLOW_ALL_USERS=true' >> /opt/data/.env"
  cd ~/hermes-workspace && docker compose down && docker compose up -d
  ```
- **Supabase Invalid API Key :** S'assurer que la clé renseignée dans `~/hermes-workspace/.env` et `/opt/data/.env` est la **service_role key** complète (environ 219 caractères).
  ```bash
  # Tester la connexion Supabase en ligne de commande depuis le conteneur
  docker exec -it hermes-workspace-hermes-agent-1 bash -c \
    'KEY=$(grep SUPABASE_KEY /opt/data/.env | cut -d= -f2) && \
     URL=$(grep SUPABASE_URL /opt/data/.env | cut -d= -f2) && \
     curl -s "$URL/rest/v1/" -H "apikey: $KEY" | head -c 50'
  # Réponse attendue : {"swagger":"2.0"...
  ```

---

## 🔄 6. Mises à jour & Cycle de Vie

### Mettre à jour Hermes Workspace (Interface & API)
```bash
cd ~/hermes-workspace
docker compose pull
docker compose down && docker compose up -d
```

### Mettre à jour l'image Hermes Agent
```bash
docker pull nousresearch/hermes-agent:latest
cd ~/hermes-workspace && docker compose down && docker compose up -d
```

### Vérifications post-mise à jour
```bash
# 1. Vérifier que tout tourne correctement
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. Vérifier que les permissions sur /opt/data sont toujours correctes
docker exec hermes-workspace-hermes-agent-1 ls -la /opt/data/

# 3. Vérifier que la configuration LLM et allowed_chats sont intacts
docker exec -u root hermes-workspace-hermes-agent-1 sh -c \
  "grep -o '^[^=]*' /opt/data/config.yaml | head -5"
```

---

## 🔐 7. Permissions & Credentials Externes

### Architecture des permissions dans le conteneur agent
| Fichier / Dossier | Propriétaire | Modifiable depuis Telegram | Note |
| :--- | :--- | :--- | :--- |
| `/opt/data/.env` | `root` | ❌ Non | Variables sensibles d'exécution |
| `/opt/data/config.yaml` | `root` | ❌ Non | Configuration LLM et accès chats |
| `/opt/data/memory/` | `hermes` | ✅ Oui | Mémoire asynchrone des sessions |
| `/opt/data/skills/` | `hermes` | ✅ Oui | Compétences dynamiques chargées |

```bash
# Réparer ou appliquer les permissions de production sur les dossiers dynamiques
docker exec -u root hermes-workspace-hermes-agent-1 bash -c \
  "mkdir -p /opt/data/memory /opt/data/skills && \
   chown -R hermes:hermes /opt/data/memory /opt/data/skills"
```

### Gestion du fichier `.env` interne (sans éditeur nano)
```bash
# Ajouter une variable d'environnement ou token tiers
docker exec -u root hermes-workspace-hermes-agent-1 sh -c "echo 'NOUVELLE_CLE=valeur' >> /opt/data/.env"

# Vérifier les noms des clés existantes (sans afficher les valeurs secrètes)
docker exec -u root hermes-workspace-hermes-agent-1 sh -c "grep -o '^[^=]*' /opt/data/.env"

# Si besoin d'éditer manuellement le .env depuis l'hôte via le volume monté :
sudo nano $(docker volume inspect hermes-workspace_claude-data | grep Mountpoint | cut -d'"' -f4)/.env
```

### Identifiants et Mots de passe d'application
- **Yannstory** : `vxsz sgzb rszp widp`

---
**💡 Astuce de production :** Pour forcer Hermes à ne pas boucler inutilement sur des tâches de fond automatisées, configurer les tâches planifiées avec le paramètre `mode: no-agent`.
