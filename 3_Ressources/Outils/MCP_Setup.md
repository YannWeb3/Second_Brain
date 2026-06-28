# MCP_SETUP.md — Connecter Airtable, Supabase et n8n
# Source officielle Airtable MCP : https://support.airtable.com/docs/using-the-airtable-mcp-server
# Source officielle Supabase MCP : https://supabase.com/docs/guides/getting-started/mcp
# Source n8n-MCP : https://github.com/czlonkowski/n8n-mcp
# Source Claude Code MCP : https://code.claude.com/docs/en/mcp

---

## PRÉ-REQUIS

```bash
# Vérifier que Node.js est installé (v18 minimum)
node --version

# Vérifier que Claude Code est installé
claude --version

# Vérifier que npm est disponible
npm --version
```

Si Claude Code n'est pas installé :
```bash
curl -fsSL https://claude.ai/install.sh | bash
source ~/.zshrc  # ou ~/.bashrc selon ton shell
```

---

## ÉTAPE 0 — PRÉPARER LE .env

Copier `.env.example` en `.env` et remplir toutes les valeurs :

```bash
cp .env.example .env
# Ouvrir .env et remplir les clés — NE PAS laisser de XXXX
```

Créer `.gitignore` à la racine si tu utilises Git :
```bash
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
```

---

## ÉTAPE 1 — AIRTABLE MCP (officiel)

> Source : https://support.airtable.com/docs/using-the-airtable-mcp-server
> Le MCP Airtable est officiel et utilise le transport HTTP — le plus simple et le plus stable.

### 1a — Créer un Personal Access Token Airtable

1. Aller sur https://airtable.com/create/tokens
2. Cliquer "Create new token"
3. Nom : `claude-mcp`
4. Scopes à cocher :
   - `schema.bases:read`
   - `data.records:read`
   - `data.records:write`
   - `schema.bases:write` (optionnel — si tu veux que Claude crée des tables)
5. Access : sélectionner les bases que Claude peut voir
6. Copier le token → le coller dans `.env` sous `AIRTABLE_PERSONAL_ACCESS_TOKEN`

### 1b — Connecter dans Claude Code

```bash
# Commande officielle Claude Code pour Airtable (transport HTTP)
claude mcp add --transport http airtable https://mcp.airtable.com/mcp \
  --header "Authorization: Bearer $(grep AIRTABLE_PERSONAL_ACCESS_TOKEN .env | cut -d '=' -f2)"
```

Ou si tu préfères passer la clé manuellement :
```bash
claude mcp add --transport http airtable https://mcp.airtable.com/mcp \
  --header "Authorization: Bearer patXXXXXXXXXXXXXX.XXXX"
```

### 1c — Vérifier la connexion

```bash
# Lister les MCP connectés
claude mcp list

# Tu dois voir : airtable — https://mcp.airtable.com/mcp
```

### 1d — Tester dans Antigravity

Dans une session Antigravity, demande :
```
Liste les bases disponibles dans mon Airtable.
```
Claude doit répondre avec tes bases sans que tu lui donnes la clé.

### 1e — Contrôler l'accès (important)

Après connexion, tu peux gérer quelles bases sont accessibles :
- Airtable > Profil > Integrations > Third-party Integrations
- Trouver "MCP Integration"
- Ajouter ou retirer des bases

> ⚠️ **Sécurité** : ne jamais donner accès à des bases contenant des données sensibles
> clients si tu n'en as pas besoin dans Claude.

---

## ÉTAPE 2 — SUPABASE MCP

> Source : https://supabase.com/docs/guides/getting-started/mcp
> ⚠️ Supabase MCP est conçu pour le développement. Ne pas connecter en production.

### 2a — Créer un token d'accès Supabase

1. Aller sur https://supabase.com/dashboard/account/tokens
2. Cliquer "Generate new token"
3. Nom : `claude-mcp`
4. Copier → coller dans `.env` sous `SUPABASE_ACCESS_TOKEN`

### 2b — Récupérer la référence projet

Dans l'URL de ton projet Supabase :
`https://supabase.com/dashboard/project/XXXXXXXXXXXX`
→ `XXXXXXXXXXXX` est ton `SUPABASE_PROJECT_REF`

### 2c — Connecter dans Claude Code

```bash
# Lire les variables depuis .env
source .env

# Ajouter le MCP Supabase
claude mcp add --transport http supabase \
  "https://mcp.supabase.com/v1/projects/${SUPABASE_PROJECT_REF}" \
  --header "Authorization: Bearer ${SUPABASE_ACCESS_TOKEN}"
```

### 2d — Vérifier

```bash
claude mcp list
# Tu dois voir : supabase — https://mcp.supabase.com/v1/projects/XXXX
```

### 2e — Tester

```
Décris la structure de ma base de données Supabase.
```

> ⚠️ **Règle absolue Supabase** : Ne jamais utiliser le MCP sur une base de production
> avec des données clients réelles. Utiliser un projet de staging/développement dédié.

---

## ÉTAPE 3 — N8N MCP

> Source : https://github.com/czlonkowski/n8n-mcp
> Deux options selon ton usage. Lire attentivement.

### Option A — Accès à la doc n8n uniquement (sans instance)
Utile pour : laisser Claude construire des workflows en connaissant les nodes n8n.
Ne nécessite pas d'instance n8n connectée.

```bash
claude mcp add --transport stdio n8n-docs \
  -- npx n8n-mcp
```

Configuration minimale dans `~/.claude/mcp.json` :
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true"
      }
    }
  }
}
```

### Option B — Connexion à ton instance n8n (lecture + écriture)
Utile pour : Claude peut lire, créer et modifier tes workflows directement.

```bash
source .env

claude mcp add --transport stdio n8n \
  --env MCP_MODE=stdio \
  --env LOG_LEVEL=error \
  --env DISABLE_CONSOLE_OUTPUT=true \
  --env N8N_API_URL="${N8N_API_URL}" \
  --env N8N_API_KEY="${N8N_API_KEY}" \
  -- npx n8n-mcp
```

Ou directement dans `~/.claude/mcp.json` :
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://ton-instance.n8n.cloud",
        "N8N_API_KEY": "n8n_api_XXXXXXXXXX"
      }
    }
  }
}
```

### 3b — Récupérer la clé API n8n

- n8n Cloud : Settings > API > Create new API key
- Self-hosted : Settings > n8n API > Create API key

### 3c — Vérifier

```bash
claude mcp list
# Tu dois voir : n8n-mcp
```

### 3d — Tester

```
Liste mes workflows n8n actifs.
```
ou
```
Crée un workflow n8n qui envoie un email quand un nouveau record est ajouté dans Airtable.
```

> ⚠️ **Best practice n8n** : Ne jamais modifier directement un workflow de production.
> Toujours travailler sur une copie. Source : n8n-MCP documentation.

---

## ÉTAPE 4 — VÉRIFICATION GLOBALE

```bash
# Lister tous les MCP connectés
claude mcp list

# Résultat attendu :
# airtable    — https://mcp.airtable.com/mcp
# supabase    — https://mcp.supabase.com/v1/projects/XXXX
# n8n-mcp     — npx n8n-mcp (stdio)
```

Test d'intégration complet dans Antigravity :
```
Vérifie que tu as accès à :
1. Airtable — liste mes bases
2. Supabase — décris la structure de ma DB
3. n8n — liste mes workflows actifs
Résume ce que tu vois pour chaque outil.
```

---

## ÉTAPE 5 — AJOUTER LES MCP AU SECOND BRAIN

### Mettre à jour `_Brain/CLAUDE.md`

Ajouter cette section dans le fichier :

```markdown
## Outils connectés (MCP)

| Outil | Usage | Commande |
|-------|-------|---------|
| Airtable | CRM, leads, contacts, deals | Accès direct — demander explicitement |
| Supabase | Base de données dev | Accès direct — NE PAS utiliser en prod |
| n8n | Workflows automatisation | Lire / créer des workflows |

Règle : charger un outil MCP uniquement si la session en a besoin.
Ne jamais interroger les 3 en même temps sans raison.
```

### Créer le skill `/sync-airtable`

Fichier : `_Brain/Skills/sync-airtable.md`

```markdown
# Skill : /sync-airtable
## Déclencheur
Commande /sync-airtable + nom de la base ou du client

## Étapes
1. Lire 1_Projets/Pro/[Client]/context.md
2. Interroger Airtable — récupérer les records du client
3. Comparer avec context.md — identifier les écarts
4. Proposer les mises à jour à faire
5. Attendre validation avant toute écriture dans Airtable

## Règle
Ne jamais écrire dans Airtable sans confirmation explicite.
```

---

## GESTION DES ERREURS COURANTES

| Erreur | Cause probable | Solution |
|--------|---------------|---------|
| `MCP server not found` | npx pas installé | `npm install -g npx` |
| `Unauthorized` Airtable | Token expiré ou mauvais scope | Régénérer le token |
| `Connection refused` n8n | Instance n8n arrêtée | Vérifier que n8n tourne |
| `Project not found` Supabase | Mauvais PROJECT_REF | Vérifier l'URL du projet |
| Timeout n8n | Workflow dépasse 5 min | Découper en sous-workflows |

---

## SÉCURITÉ — RÈGLES NON NÉGOCIABLES

1. **Jamais de clés dans les fichiers .md** — uniquement dans `.env`
2. **Jamais de .env dans Git** — vérifier `.gitignore` avant tout commit
3. **Supabase MCP = développement uniquement** — pas de données clients réelles
4. **Rotation des tokens** — tous les 90 jours minimum
5. **Accès minimal** — ne donner à Claude que les scopes dont il a besoin
6. **Backup des clés** — stocker dans un gestionnaire de mots de passe (pas dans Drive)