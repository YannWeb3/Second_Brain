# CLAUDE.md — Hermes Agent

> [!IMPORTANT]
> Référence opérationnelle : **[hermes-agent-complet.md](file:///c:/Users/Win10%20Pro%20x64/Desktop/Second_Brain/1_Projets/Pro/Hermes-Agent/hermes-agent-complet.md)**.

## Commandes Docker (Serveur)
- Logs : `docker compose logs -f`
- Restart : `docker compose down && docker compose up -d`
- Setup LLM : `docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes setup`

## Configuration
- Workspace UI : `http://10.10.0.1:3001`
- Variables critiques : `API_SERVER_HOST=0.0.0.0`, `COOKIE_SECURE=0`

## Maintenance & Sécurité
- **Permissions** : `docker exec -u root hermes-workspace-hermes-agent-1 bash -c "mkdir -p /opt/data/memory /opt/data/skills && chown -R hermes:hermes /opt/data/memory /opt/data/skills"`
- **Update Workspace** : `cd ~/hermes-workspace && docker compose pull && docker compose down && docker compose up -d`
- **Update Agent** : `docker pull nousresearch/hermes-agent:latest && docker compose down && docker compose up -d`
- **Vérifier Config** : `docker exec -u root hermes-workspace-hermes-agent-1 sh -c "grep -o '^[^=]*' /opt/data/config.yaml | head -5"`

## Règles du projet
- Toujours vérifier le port 3001 pour l'UI (conflit WAHA sur 3000).
- Les modifications de config agent se font dans `/opt/data/.env` (container).
- Permissions sur `memory/` et `skills/` à vérifier après chaque update.
