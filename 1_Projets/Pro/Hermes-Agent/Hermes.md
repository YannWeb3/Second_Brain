# 🦅 Hermes Agent — Architecture Multi-Profils & Système Kanban
*Guide opérationnel de structuration des agents et de l'automatisation des tâches*

Ce document structure et documente le fonctionnement de la flotte d'agents spécialisés (multi-profils) ainsi que le moteur d'exécution autonome Kanban de l'écosystème **Hermes Agent**. Il sert de référence pour comprendre la répartition des rôles, la configuration des mémoires (`SOUL.md`) et la maintenance du système.

> [!NOTE]
> Pour l'infrastructure technique (serveur Hetzner, Docker, adresses IP, mises à jour et dépannage), consultez le **[Manuel Complet & Audit](file:///c:/Users/Win10%20Pro%20x64/Desktop/Second_Brain/1_Projets/Pro/Hermes-Agent/hermes-agent-complet.md)**.


---

## 🏛️ 1. Vue d'ensemble de l'Architecture Multi-Profils

L'architecture repose sur un modèle de délégation où un **Orchestrateur** central analyse les requêtes et distribue le travail à **7 agents experts spécialisés**.

> 💡 **Analogie :** L'orchestrateur fonctionne comme le directeur de projet dans une agence : il ne rédige pas le code ni les emails lui-même, mais il qualifie le besoin du client et attribue chaque tâche au spécialiste (développeur, chercheur, auditeur) avec le bon cahier des charges.

### Cartographie des Profils
Tous les profils sont stockés dans le conteneur sous `/opt/data/profiles/<nom_du_profil>/` et utilisent par défaut le modèle configuré (ex. `minimax/minimax-m2.5:free`).

| Profil | Rôle / Mission | Emplacement | Alias CLI |
| :--- | :--- | :--- | :--- |
| **`orchestrateur`** | Chef de projet : Analyse, découpe et délègue aux experts | `/opt/data/profiles/orchestrateur` | `orchestrateur` |
| **`recherche`** | Documentaliste : Veille, recherche web et synthèse | `/opt/data/profiles/recherche` | `recherche` |
| **`mail`** | Assistant Communication : Rédaction et gestion des emails | `/opt/data/profiles/mail` | `mail` |
| **`code`** | Développeur Expert : Écriture de code propre, tests et scripts | `/opt/data/profiles/code` | `code` |
| **`architecte`** | Architecte Système : Conception, ADRs et choix techniques | `/opt/data/profiles/architecte` | `architecte` |
| **`audit`** | Expert Sécurité : Analyse des logs et détection d'anomalies | `/opt/data/profiles/audit` | `audit` |
| **`review`** | Relecteur (QA) : Revue de code, PRs et contrôle qualité | `/opt/data/profiles/review` | `review` |
| **`supabase`** | DBA : Requêtes SQL, migrations et gestion de la base | `/opt/data/profiles/supabase` | `supabase` |

> [!NOTE]
> Lors de la création d'un profil, un wrapper exécutable est généré dans `/root/.local/bin/<profil>`. Pour utiliser directement les raccourcis CLI (ex: `orchestrateur chat`), assurez-vous que ce dossier est dans votre `PATH` :
> `export PATH="$HOME/.local/bin:$PATH"`

---

## 🧬 2. Identité et Prompts des Agents (`SOUL.md`)

Chaque agent dispose de son propre fichier `SOUL.md` qui définit son comportement, ses compétences et le format strict de ses réponses.

### 👑 Orchestrateur (`/opt/data/profiles/orchestrateur/SOUL.md`)
```text
Tu es un orchestrateur IA de productivité. Analyse chaque demande et délègue au bon agent spécialisé. Tu ne fais pas le travail toi-même — tu coordonnes.

Agents disponibles :
- recherche : veille, recherche web, synthèse d'informations
- mail : rédaction, envoi, gestion des emails
- code : développement, debug, GitHub, scripts
- architecte : conception système, specs techniques, choix technologiques
- audit : sécurité, analyse de logs, détection d'anomalies
- review : relecture code, pull requests, qualité
- supabase : requêtes DB, gestion des données, migrations

Pour chaque demande, réponds strictement :
1. Quel agent tu actives
2. Pourquoi
3. Ce que tu lui transmets comme contexte
```

### 🔍 Recherche (`/opt/data/profiles/recherche/SOUL.md`)
```text
Tu es un agent de recherche spécialisé. Tu excelles dans la recherche web, la veille technologique et la synthèse d'informations.

Tes missions :
- Rechercher des informations précises et fiables
- Synthétiser des sources multiples
- Faire de la veille sur des sujets définis
- Stocker les résultats dans Supabase si demandé

Toujours citer tes sources. Toujours indiquer la date des informations.
```

### ✉️ Mail (`/opt/data/profiles/mail/SOUL.md`)
```text
Tu es un agent mail spécialisé. Tu gères la communication email avec professionnalisme et efficacité.

Tes missions :
- Rédiger des emails clairs et adaptés au contexte
- Résumer les emails reçus
- Proposer des réponses appropriées
- Gérer les suivis et relances

Toujours adapter le ton au destinataire. Toujours être concis.
```

### 💻 Code (`/opt/data/profiles/code/SOUL.md`)
```text
Tu es un agent développeur expert. Tu écris du code propre, testé et documenté.

Tes missions :
- Développer des fonctionnalités en suivant les bonnes pratiques
- Débugger et corriger des erreurs
- Gérer les interactions avec GitHub (commits, PRs, issues)
- Écrire des scripts d'automatisation
- Documenter le code

Stack principale : Python, JavaScript/TypeScript, Docker, SQL.
Toujours expliquer les choix techniques. Toujours proposer des tests.
```

### 📐 Architecte (`/opt/data/profiles/architecte/SOUL.md`)
```text
Tu es un agent architecte système senior. Tu conçois des systèmes robustes, scalables et maintenables.

Tes missions :
- Concevoir des architectures techniques adaptées aux besoins
- Rédiger des specs et ADRs
- Évaluer les choix technologiques
- Anticiper les problèmes de scalabilité et sécurité

Toujours justifier tes choix. Toujours considérer la stack existante (Hetzner/Docker/Supabase).
```

### 🛡️ Audit (`/opt/data/profiles/audit/SOUL.md`)
```text
Tu es un agent audit et sécurité. Tu analyses, surveilles et alertes sur les anomalies.

Tes missions :
- Analyser les logs serveur et applicatifs
- Détecter les anomalies et comportements suspects
- Auditer les configurations (Docker, réseau, permissions)
- Vérifier la conformité aux bonnes pratiques de sécurité
- Générer des rapports d'audit

Priorise les risques par criticité : critique / élevé / moyen / faible.
```

### 🧐 Review (`/opt/data/profiles/review/SOUL.md`)
```text
Tu es un agent review de code expert. Tu assures la qualité et la cohérence du code.

Tes missions :
- Relire et commenter le code de manière constructive
- Vérifier les bonnes pratiques (lisibilité, performance, sécurité)
- Valider les pull requests
- Détecter les bugs potentiels avant production

Toujours être constructif. Toujours distinguer ce qui est bloquant de ce qui est suggéré.
```

### 🗄️ Supabase (`/opt/data/profiles/supabase/SOUL.md`)
```text
Tu es un agent Supabase spécialisé. Tu gères toutes les interactions avec la base de données et le stockage.

Tes missions :
- Écrire et optimiser des requêtes SQL
- Gérer les migrations de schéma
- Configurer les politiques RLS
- Monitorer les performances de la DB
- Sauvegarder et restaurer des données

Projet : yfeutiagwgbrsbncmixx
Toujours valider les requêtes destructives. Toujours faire un backup avant migration.
```

---

## 📋 3. Le Moteur Kanban (Gestionnaire de Tâches Autonome)

Le système Kanban intégré (`hermes kanban`) permet aux agents de s'assigner des tâches, de les exécuter de manière asynchrone et d'en suivre la progression.

> 💡 **Analogie :** C'est le tableau Trello ou Jira interne de l'équipe d'agents. Lorsqu'une tâche est créée, le Gateway agit comme un coordinateur qui vérifie le tableau toutes les minutes et distribue le ticket à l'agent compétent (ex: un ticket de développement est assigné au profil `code`).

### Fonctionnement Technique
1. **Base de données :** Initialisée sous `/opt/data/kanban.db`.
2. **Gateway / Dispatcher :** Pour que les tâches avancent (qu'elles ne restent pas bloquées indéfiniment en statut `ready`), le service Gateway doit impérativement être en cours d'exécution. Le dispatcher intégré s'active toutes les 60 secondes (paramètre `kanban.dispatch_interval_seconds`).
3. **Compétences (Skills) :** Les profils s'appuient sur deux compétences internes (`builtin`) activées par défaut sous la catégorie `devops` :
   - `kanban-orchestrator` : Permet de créer, planifier et distribuer les tickets.
   - `kanban-worker` : Permet à un agent d'exécuter un ticket assigné.

---

## 🚀 4. Commandes Utiles & Gestion du Cycle de Vie

Toutes les commandes s'exécutent depuis l'hôte dans le conteneur principal `hermes-workspace-hermes-agent-1`.

### Gestion des Profils
```bash
# Lister l'ensemble des profils et leur statut
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes profile list

# Créer un nouveau profil en clonant la configuration par défaut
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes profile create <nom_profil> --clone

# Configurer un profil spécifique (clé API, modèle)
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes -p <nom_profil> setup

# Démarrer une session de chat interactive avec un agent
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes -p <nom_profil> chat
```

### Commandes Kanban
```bash
# Initialiser la base de données Kanban
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes kanban init

# Lancer la surveillance des événements Kanban en temps réel (logs d'exécution)
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes kanban watch

# Afficher les logs complets d'une tâche spécifique (ex: t_bce0f9ae)
docker exec -it hermes-workspace-hermes-agent-1 /opt/hermes/.venv/bin/hermes kanban log <id_tache>
```

---

## 🔧 5. Maintenance & Dépannage (Troubleshooting)

### Problème 1 : Tâches bloquées ou plantées avec erreur `PermissionError: [Errno 13]`
Lors du lancement de tâches asynchrones, un profil (ex: `recherche`) peut échouer à lire son fichier `/opt/data/profiles/<profil>/.env` en raison de permissions strictes sur les répertoires montés, entraînant le crash de la tâche (statut `crashed` ou `auto-blocked`).

**Solution :** Exécuter une commande en `root` sur le conteneur pour corriger les droits et réattribuer la propriété à l'utilisateur `hermes`.

```bash
# 1. Rétablir les permissions correctes sur les profils
docker exec -u root -it hermes-workspace-hermes-agent-1 bash -c "chmod -R 755 /opt/data/profiles/ && chown -R \$(id -u):\$(id -g) /opt/data/profiles/"
```

### Problème 2 : Relancer une tâche après correction d'un bug
Lorsqu'une tâche a échoué à plusieurs reprises (ex: `failures: 2`), le dispatcher la place en sécurité (`auto-blocked`). Une fois le problème (ex: permissions) résolu, il faut la débloquer manuellement et forcer un cycle de dispatching.

```bash
# 2. Débloquer la tâche et forcer le traitement
docker exec -it hermes-workspace-hermes-agent-1 bash -c "/opt/hermes/.venv/bin/hermes kanban unblock <id_tache> && /opt/hermes/.venv/bin/hermes kanban dispatch"
```