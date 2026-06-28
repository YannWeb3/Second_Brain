# AUDIT UX/UI – ESPACE MONTEUR EWA STUDIO

## Version : Audit V1

## Date : Août 2025

---

# Résumé exécutif

L'espace monteur est déjà visuellement propre, moderne et cohérent avec l'identité EWA Studio.

L'architecture générale est pertinente :

* Dashboard
* Gestion des projets
* Facturation
* Assets
* Retours
* Formation

Cependant, plusieurs points de friction risquent de ralentir les monteurs lorsqu'ils commenceront à utiliser la plateforme quotidiennement avec des projets réels.

L'objectif principal doit être :

> Permettre à un monteur de comprendre instantanément ce qu'il doit faire aujourd'hui, ce qui est urgent et où il en est dans son workflow.

---

# PRIORITÉ CRITIQUE (P1)

## 1. Vérifier la cohérence des données de facturation

### Constat

Des informations financières sont actuellement visibles dans le profil du monteur.

La section "Facturation" existe également dans le menu.

### Risque

* Duplication des données
* Incohérence d'affichage
* Risque de confusion utilisateur
* Difficulté de maintenance

### Action demandée

✅ Vérifier que toutes les données affichées dans :

* Mon Profil
* Facturation

proviennent bien de la même source de données.

### Validation attendue

* Revenus mensuels identiques
* Revenus cumulés identiques
* Factures identiques
* Aucun écart entre les écrans

---

## 2. Ajouter un indicateur d'urgence sur les projets

### Constat

Le workflow est clair mais ne permet pas de distinguer rapidement les priorités.

### Recommandation

Ajouter des badges :

🔴 Urgent

🟠 Cette semaine

🟢 En avance

### Bénéfice

Le monteur identifie immédiatement la tâche prioritaire.

---

## 3. Ajouter un compteur dans chaque colonne Kanban

### Exemple

En montage (5)

Check interne (2)

Retouche (1)

Livré (24)

### Bénéfice

Vision instantanée de la charge de travail.

---

# PRIORITÉ ÉLEVÉE (P2)

## 4. Ajouter une colonne "Bloqué"

### Cas d'usage

* Rushs manquants
* Feedback client incomplet
* Validation en attente

### Bénéfice

Évite que les projets restent bloqués dans "En montage".

---

## 5. Ajouter un filtre "Mes urgences"

### Nouveaux filtres

* Tout
* Mes projets
* Urgents
* En retard
* En attente client

### Bénéfice

Navigation plus rapide lorsque le volume de projets augmente.

---

## 6. Ajouter des actions rapides sur les cartes projet

### Boutons recommandés

▶ Ouvrir

⬆ Livrer

💬 Commentaires

⚠ Signaler un problème

### Bénéfice

Réduction du nombre de clics.

---

# PRIORITÉ MOYENNE (P3)

## 7. Réorganiser le menu latéral

### Structure actuelle

* Dashboard
* Mes projets
* Check interne
* Facturation
* Mon profil
* Assets
* Retours
* Académie
* Playbooks

### Proposition

### Production

* Dashboard
* Mes projets
* Assets
* Retours

### Gestion

* Facturation
* Mon profil

### Ressources

* Académie
* Playbooks

### Bénéfice

Navigation plus intuitive.

---

## 8. Ajouter un centre de notifications

### Types de notifications

* Nouveau projet
* Retour client
* Projet validé
* Facture validée

### Bénéfice

Le monteur n'a plus besoin de vérifier manuellement plusieurs écrans.

---

## 9. Ajouter des statistiques de performance

### Exemple

⭐ Satisfaction : 4,8 / 5

⚡ Temps moyen de rendu : 1,7 jours

🎯 Livraisons à l'heure : 97 %

### Bénéfice

Motivation et suivi de performance.

---

# PRIORITÉ STRATÉGIQUE (P4)

## 10. Assistant IA Projet

### Fonction

Afficher automatiquement :

* Résumé client
* Objectifs
* Style de montage
* Derniers retours
* Deadline
* Priorité

### Exemple

Client : Fitness Pro

Objectif :
Générer des leads

Style :
Alex Hormozi

Dernier retour :
Hook plus agressif

Deadline :
Demain 18h

### Bénéfice

Réduction massive du temps passé à chercher l'information.

---

# Tests utilisateurs recommandés

## Test 1

Trouver le prochain projet à traiter

Objectif :
< 10 secondes

---

## Test 2

Déposer une vidéo terminée

Objectif :
< 30 secondes

---

## Test 3

Trouver le dernier retour client

Objectif :
< 15 secondes

---

## Test 4

Consulter ses revenus du mois

Objectif :
< 10 secondes

---

# Validation demandée avant prochaine itération

Merci de confirmer les points suivants :

□ Les données de facturation remontent correctement.

□ Les données affichées dans "Mon Profil" et "Facturation" sont synchronisées.

□ Les statuts du Kanban correspondent au workflow réel des monteurs.

□ Les notifications sont prévues dans la roadmap.

□ Les cartes projet pourront accueillir des indicateurs d'urgence.

---

# Conclusion

La plateforme possède déjà une base solide et professionnelle.

Les prochains gains de valeur se situent principalement sur :

1. La gestion des priorités.
2. La réduction du nombre de clics.
3. La visibilité sur les projets urgents.
4. La centralisation de l'information.
5. L'assistance IA aux monteurs.

Ces améliorations permettront d'accompagner efficacement la montée en charge de la production tout en préparant les fondations du futur SaaS EWA.
