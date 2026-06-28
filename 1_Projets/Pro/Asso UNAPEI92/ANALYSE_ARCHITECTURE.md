# Analyse Comparative — Approche Prod-Ready UNAPEI92

## Résumé Exécutif

| Critère | Template Generator | UNAPEI92 Actuel | Recommandation |
|---------|-------------------|-----------------|----------------|
| **Maintenabilité** | ⭐⭐⭐ Génération automatique | ⭐⭐ 15 fichiers manuels | **Adopter le générateur** |
| **Compatibilité backend** | ⭐⭐ Payload array (breaking change) | ⭐⭐⭐ Compatible Apps Script | **Conserver format key-value** |
| **UX / Navigation** | ⭐⭐⭐ Wizard progressif | ⭐⭐ Scroll libre | **Adopter wizard + progress bar** |
| **Questions conditionnelles** | ⭐⭐⭐ Natif | ❌ Non supporté | **Ajouter au système actuel** |
| **Déploiement** | ⭐⭐ Nécessite Python | ⭐⭐⭐ HTML statique pur | **Générer une fois, déployer statique** |

---

## 1. Différences Techniques Majeures

### 1.1 Structure des Données

**Template Generator** (Array ordonné) :
```json
{
  "type": "IME_RGPD",
  "timestamp": "2026-04-24T10:00:00Z",
  "responses": [
    {"question_id": "q1", "question": "Avez-vous un DPO ?", "answer": "Oui", "visible": true},
    {"question_id": "q2", "question": "Nom du DPO", "answer": "", "visible": false}
  ]
}
```

**UNAPEI92 Actuel** (Object key-value) :
```json
{
  "type": "IME",
  "responses": {
    "Avez-vous un DPO ?": "Oui",
    "Nom du DPO": "Jean Dupont"
  }
}
```

**Impact** : Le script Apps Script actuel utilise `Object.keys(responses)` et ne gère pas les arrays. Changer le format = modifier le backend.

### 1.2 Navigation Utilisateur

| Template Generator | UNAPEI92 Actuel |
|-------------------|-----------------|
| Wizard par blocs (précédent/suivant) | Navigation libre avec ancres |
| Progress bar animée | Pas de progression visuelle |
| Validation bloc par bloc | Validation à la soumission |
| Animation fade entre blocs | Scroll standard |

### 1.3 Questions Conditionnelles

**Template Generator** — Support natif :
```javascript
// Définition
{
  id: 'q2',
  label: 'Nom du DPO',
  condition: {q: 'q1', is: 'Oui'}  // S'affiche si q1 == 'Oui'
}

// Implémentation JS
function applyConditions() {
  Object.entries(conditions).forEach(([qid, cond]) => {
    const val = getFieldValue(cond.q);
    const show = cond.is ? val === cond.is : val !== cond.not;
    qEl.classList.toggle('hidden', !show);
  });
}
```

**UNAPEI92 Actuel** — Non supporté (toutes les questions sont affichées).

---

## 2. Analyse des Forces/Faiblesses

### Template Generator ✅

**Forces :**
- Génération automatique de 15 formulaires à partir d'une définition JSON
- Payload stable (toutes les questions dans l'ordre → colonnes Sheets fixes)
- Questions conditionnelles robustes
- UX moderne (DM Sans/Serif Display, animations, progress bar)
- Navigation guidée réduit l'erreur utilisateur

**Faiblesses :**
- Format de payload incompatible avec le backend existant
- Nécessite Python pour régénérer (dépendance build)
- Débogage plus complexe (code généré)

### UNAPEI92 Actuel ✅

**Forces :**
- 100% compatible avec le backend Apps Script
- Déploiement ultra-simple (HTML statique pur)
- Débogage facile (code lisible, pas de génération)
- Navigation flexible (l'utilisateur va où il veut)

**Faiblesses :**
- Maintenance manuelle de 16 fichiers
- Pas de questions conditionnelles
- Pas de progress bar
- Risque de désynchronisation entre formulaires

---

## 3. Recommandation : Architecture Hybride V2

### 3.1 Principe

```
┌─────────────────────────────────────────────────────────────┐
│                    FORM_BUILDER.PY                          │
│  (Générateur Python — combine les deux approches)           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              FICHIERS JSON DE CONFIGURATION                 │
│  questions_ime.json, questions_savs.json, etc.              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              16 FORMULAIRES HTML GÉNÉRÉS                    │
│  • Format payload key-value (compatibilité Apps Script)    │
│  • Navigation wizard avec progress bar                     │
│  • Questions conditionnelles                               │
│  • Design UNAPEI (#0055A4)                                 │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Spécifications de la V2

**Format de sortie compatible :**
```javascript
// Au lieu de responses[] array
const payload = {
  type: 'IME',
  timestamp: new Date().toISOString(),
  responses: {}  // Object key-value pour compatibilité
};

// Mapping : question_id → answer
ALL_QUESTION_IDS.forEach(qid => {
  const qEl = document.getElementById('q-' + qid);
  const isHidden = qEl?.classList.contains('hidden');
  const answer = isHidden ? '' : getFieldValue(qid);
  // Clé = label de la question (comme actuellement)
  responses[ALL_QUESTION_LABELS[qid]] = answer;
});
```

**Fonctionnalités à conserver du Template Generator :**
1. ✅ Navigation wizard par blocs
2. ✅ Progress bar animée
3. ✅ Questions conditionnelles (show/hide)
4. ✅ Validation bloc par bloc
5. ✅ Design moderne (fonts, ombres, radius)

**Fonctionnalités à conserver d'UNAPEI92 :**
1. ✅ Format de payload key-value
2. ✅ Charte graphique UNAPEI (#0055A4, #E60028)
3. ✅ Structure FORM_CONFIG (pour maintenance facile)
4. ✅ Navigation sticky par blocs nommés

---

## 4. Implementation Plan

### Étape 1 : Créer form_builder.py (fork de template_generator.py)

```python
# Modifications majeures :
# 1. Payload key-value au lieu d'array
# 2. Couleurs UNAPEI (#0055A4, #E60028)
# 3. Nav sticky + wizard (hybride)
# 4. Génération des 15 formulaires en une commande
```

### Étape 2 : Structurer les données

```
Asso UNAPEI92/
├── data/
│   ├── questions_ime.json      # 61 questions RGPD
│   ├── questions_savs.json
│   ├── questions_sessad.json
│   └── ... (15 fichiers)
├── generator/
│   └── form_builder.py         # Générateur
├── output/                     # Formulaires générés
│   ├── formulaires/
│   │   ├── ime.html
│   │   ├── savs.html
│   │   └── ...
│   └── index.html
└── google-apps-script.js       # Backend (inchangé)
```

### Étape 3 : Format JSON des questions

```json
{
  "form_type": "IME",
  "title": "Institut Médico-Éducatif",
  "sections": [
    {
      "name": "Gouvernance RGPD",
      "questions": [
        {
          "id": "dpo_nom",
          "label": "Nom du DPO désigné",
          "type": "text",
          "required": true
        },
        {
          "id": "dpo_externe",
          "label": "Le DPO est-il externe ?",
          "type": "radio",
          "choices": ["Oui", "Non"],
          "required": true
        },
        {
          "id": "dpo_societe",
          "label": "Nom de la société externe",
          "type": "text",
          "condition": {"q": "dpo_externe", "is": "Oui"}
        }
      ]
    }
  ]
}
```

---

## 5. Conclusion

| Aspect | Décision |
|--------|----------|
| **Générateur** | ✅ Oui — maintenance automatisée des 15 formulaires |
| **Payload** | Key-value (compatibilité backend) |
| **Navigation** | Wizard + nav sticky hybride |
| **Conditionnelles** | ✅ Ajouter — essentiel pour RGPD |
| **Design** | Charte UNAPEI + améliorations UX |

**Livrable recommandé** : Un générateur Python (`form_builder.py`) qui produit des formulaires HTML statiques avec :
- Format de données compatible Apps Script
- Toutes les fonctionnalités UX du template generator
- Génération batch des 15 formulaires

Cette approche combine la **maintenabilité** du générateur avec la **simplicité de déploiement** de l'approche actuelle.
