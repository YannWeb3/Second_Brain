# Documentation Apps Script - UNAPEI92

## Version 1.1 PROD

---

## Architecture

```
┌─────────────────┐     HTTP POST      ┌──────────────────┐
│  Formulaire     │ ─────────────────► │  Apps Script     │
│  HTML (GitHub)  │   JSON {type,      │  Web App         │
│                 │        responses}  │                  │
└─────────────────┘                    └────────┬─────────┘
                                                │
                                                ▼
                                       ┌──────────────────┐
                                       │  Google Sheets   │
                                       │  - 16+ onglets   │
                                       │  - 1 ligne =     │
                                       │    1 réponse     │
                                       └──────────────────┘
```

---

## Points d'entrée

### `doPost(e)` - Réception des formulaires

**Méthode** : POST  
**Content-Type** : application/json

**Payload attendu** :
```json
{
  "type": "IME_RGPD",
  "responses": {
    "q0_1_nom_etablissement": "IME Les Lilas",
    "q0_2_nom_prenom_repondant": "Marie Dupont",
    "q0_3_fonction": "directeur",
    ...
  }
}
```

**Réponse succès** :
```json
{
  "status": "success",
  "message": "Réponse enregistrée avec succès"
}
```

**Réponse erreur** :
```json
{
  "status": "error",
  "message": "Type de formulaire non reconnu..."
}
```

---

### `doGet(e)` - Health Check

**Méthode** : GET  
**URL** : URL_DE_LA_WEB_APP (sans paramètres)

**Réponse** :
```json
{
  "status": "ok",
  "message": "Service UNAPEI92 actif",
  "timestamp": "2026-04-24T10:30:00.000Z",
  "version": "1.1.0"
}
```

**Utilisation** : Vérifier que le service est en ligne avant déploiement.

---

### `doOptions(e)` - CORS Preflight

Gère automatiquement les requêtes OPTIONS pour le CORS.  
Pas d'appel manuel nécessaire.

---

## Configuration

### Types de formulaires acceptés

Dans `CONFIG.TYPES` :
- `IME_RGPD` - Questionnaire RGPD détaillé IME
- `IME`, `SAVS`, `SESSAD`, `ESAT`, `EANM`, `EAM`, `CMPP`
- `SI-IT`, `Direction`, `Qualite`, `Donateurs`, `DAF`, `RH`, `Paie`, `Communication`

**Sécurité** : Les requêtes avec un type non listé sont rejetées.

---

## Fonctionnement interne

### Gestion dynamique des colonnes

Le script gère automatiquement l'évolution des formulaires :

1. **Première soumission** : Crée les colonnes fixes + toutes les questions reçues
2. **Soumissions suivantes** : 
   - Si nouvelle question détectée → ajoute une colonne à droite
   - Si question existante → remplit la colonne correspondante
   - Si question absente → laisse vide

**Avantage** : Plusieurs versions d'un même formulaire peuvent coexister sans décaler les données.

### Structure d'une feuille

| Horodatage | Type formulaire | q0_1_nom_etablissement | q0_2_nom_prenom | ... |
|------------|-----------------|------------------------|-----------------|-----|
| 24/04/2026 10:30 | IME_RGPD | IME Les Lilas | Marie Dupont | ... |
| 24/04/2026 11:15 | IME_RGPD | IME du Centre | Jean Martin | ... |

---

## Fonctions de maintenance

### `initialiserFeuilles()`

**Usage** : À exécuter une fois après installation  
**Action** : Crée toutes les feuilles pour les types configurés

```javascript
// Dans l'éditeur Apps Script :
initialiserFeuilles()
```

---

### `testerConfiguration()`

**Usage** : Vérifier que tout est configuré correctement  
**Vérifie** :
- Accès au spreadsheet
- Liste des types
- Création de feuille test

```javascript
// Dans l'éditeur Apps Script :
testerConfiguration()
```

**Output attendu** :
```
✓ Spreadsheet accessible : UNAPEI92_Reponses
✓ URL : https://docs.google.com/spreadsheets/d/...
✓ Types configurés : IME_RGPD, IME, SAVS, ...
✓ Test de création de feuille réussi
✓ Nettoyage test OK
=== Configuration validée ===
```

---

### `getStatistiques()`

**Usage** : Obtenir un rapport d'utilisation  
**Affiche** : Nombre de réponses par type de formulaire

```javascript
// Dans l'éditeur Apps Script :
getStatistiques()
```

**Output exemple** :
```
=== STATISTIQUES ===
Date : 24/04/2026 10:45:00

IME_RGPD : 15 réponse(s) (65 colonnes)
IME : 0 réponse(s) (2 colonnes)
SAVS : 3 réponse(s) (45 colonnes)
...
```

---

## Dépannage

### "Type de formulaire non reconnu"

**Cause** : Le type envoyé n'est pas dans `CONFIG.TYPES`  
**Solution** : Ajouter le type dans la configuration ou corriger le `type` dans le HTML

### "Données de réponses invalides"

**Cause** : Le champ `responses` est manquant ou n'est pas un objet  
**Solution** : Vérifier le format JSON envoyé par le formulaire

### Erreur CORS

**Cause** : Mauvaise configuration du déploiement  
**Solution** : Vérifier que le déploiement est configuré avec :
- Exécuter en tant que : Moi
- Qui y a accès : Tout le monde

### Colonnes désordonnées

**Cause** : Normal avec l'ancien script  
**Solution** : Le nouveau script gère ça automatiquement. Pour nettoyer une feuille existante : exporter les données, supprimer la feuille, laisser le script la recréer.

---

## Limites et bonnes pratiques

| Limite | Valeur | Recommandation |
|--------|--------|----------------|
| Caractères par cellule | 50 000 | Textes longs tronqués automatiquement |
| Colonnes par feuille | 18 278 | Pas de risque avec les formulaires |
| Lignes par feuille | 10 millions | Archiver les anciennes données si besoin |
| Temps d'exécution | 6 min/script | Pas de risque avec ce script |
| Requêtes par jour | 20 000 (compte gratuit) | Suffisant pour ce usage |

---

## Sécurité

- ✅ Validation des types de formulaires
- ✅ Validation du format des données
- ✅ CORS configuré pour accepter toutes les origines
- ✅ Pas de données sensibles dans les logs
- ✅ ID du spreadsheet à configurer manuellement

---

## Mise à jour du script

Pour mettre à jour vers une nouvelle version :

1. Sauvegarder l'ancien script (Ctrl+A, Ctrl+C)
2. Coller le nouveau script
3. Vérifier que `SPREADSHEET_ID` est correct
4. Cliquer sur **Déployer** > **Gérer les déploiements**
5. Modifier le déploiement actif
6. Sélectionner la nouvelle version du code
7. Cliquer sur **Déployer**

**Les données existantes sont conservées.**
