# Skill : /meeting
## Déclencheur
Commande `/meeting` + coller le transcript

## Étapes
1. Lire le transcript fourni
2. Identifier : participants, date, contexte
3. Extraire :
   - Décisions prises (liste numérotée)
   - Actions à faire (avec responsable + deadline si mentionné)
   - Points en suspens / à revoir
   - Insights clés
4. Générer le résumé structuré
5. Demander : dans quel dossier sauvegarder ?
6. Sauvegarder + mettre à jour l'index du dossier

## Format output
```
# Résumé réunion — [Date] — [Sujet]

## Participants
## Décisions
## Actions
## En suspens
## Insights
```
