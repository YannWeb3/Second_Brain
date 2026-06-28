# Projet : Serveur IA Local - Stratégie et Achat
**Date :** 13 Juin 2026

## 🎯 Objectif
Mettre en place un serveur d'Intelligence Artificielle local pour **670 €**, afin de réduire les coûts d'API (OpenAI, Anthropic) pour les tâches courantes, tout en s'intégrant au système existant.

**Ressources actuelles :**
- Un VPS Cloud (Hetzner à 8€/mois) qui héberge n8n, Coolify et Supabase.
- Un abonnement Cloud (Llama Pro à 20€/mois) pour les modèles très avancés.
- Un orchestrateur IA ("Hermes Agent").

---

## 🏗️ L'Architecture Hybride (Local + Cloud)

La stratégie repose sur la complémentarité : on ne fait pas tout en local, ni tout dans le cloud.

1. **Le "Travailleur" (Local)** : Le futur mini-PC s'occupe des tâches ingrates et répétitives envoyées par n8n (extraire des données de PDF, faire des résumés massifs de réunions ou de données SESSAD/RGPD). Ces tâches consomment beaucoup de tokens, donc les faire en local coûte **0 €**.
2. **Le "Cerveau" (Cloud)** : L'orchestrateur Hermes Agent utilise les modèles Cloud haut de gamme (via l'abonnement Llama Pro) pour des décisions complexes, l'architecture globale ou la programmation.

---

## 💻 Le Matériel Choisi

**Configuration idéale : Mini-PC Barebone (Minisforum, Beelink ou AOOSTAR)**
- **Processeur :** AMD Ryzen 7 8845HS (Rapide, excellent pour la bureautique et les jeux).
- **Carte Graphique :** Radeon 780M intégrée (La meilleure pour faire tourner l'IA locale via Ollama).
- **Mémoire RAM :** 64 Go de DDR5 (Achetée séparément).
- **Stockage :** 1 To SSD NVMe (Acheté séparément).
- **Système d'exploitation :** Windows 11 Pro (via une clé pas chère) ou Linux (Ubuntu Server).

**Budget Estimé : ~670 €**
- Boitier Barebone : ~430 €
- 64 Go RAM : ~170 €
- 1 To SSD : ~70 €

---

## 🧠 Pourquoi 64 Go de RAM ? (La vraie astuce)

Avoir 64 Go de mémoire transforme ce petit PC en véritable station de travail professionnelle :
- **Taille des Modèles IA :** Les gros modèles très intelligents comme Qwen 3.6 (27B) ou Command R (35B) pèsent environ 16 à 20 Go. Ils rentrent parfaitement dans les 64 Go, avec énormément de marge pour le système.
- **Multitâche :** On peut télécharger de nombreux modèles sur le SSD, et basculer instantanément d'un modèle à l'autre selon la tâche n8n.
- **Le Gaming :** La carte graphique peut utiliser jusqu'à 16 Go de cette RAM. Résultat : d'excellentes performances (1080p) sur des jeux comme *Stellaris*, *Civilization 7*, *CS2*, *Kaiserpunk* ou *Beyond Astra*.

---

## 💻 Entretien du Matériel Existant (Lenovo ThinkPad T460s)

Afin de ne pas jeter le matériel robuste existant et de le conserver pour la bureautique et la gestion du VPS Hetzner :
- **Diagnostic :** Le PC est un ThinkPad T460s (très solide), mais son processeur Intel de 6ème génération est incapable de faire tourner l'IA locale de manière fluide.
- **Action :** Ajouter une barrette de **16 Go RAM DDR4 SO-DIMM** (2133/2400 MHz) dans le slot disponible pour atteindre 20/24 Go au total.
- **Coût :** ~30 €.
- **Bénéfice :** Permet de prolonger la durée de vie de ce PC portable de plusieurs années pour un coût dérisoire.

---

## 🚀 Prochaines Étapes
1. Acheter les composants (Vérifier les promos Amazon).
2. Assembler la RAM et le SSD (Très simple).
3. Installer l'OS (Windows Pro ou Linux).
4. Installer Ollama pour télécharger les LLMs (Qwen 27B, Gemma 12B/27B).
5. Créer un tunnel sécurisé (Cloudflare Tunnel ou Tailscale) pour connecter le mini-PC à n8n sur Hetzner.
