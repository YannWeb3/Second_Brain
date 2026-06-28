/**
 * APPS SCRIPT — Récepteur Google Sheets
 * Unapei92 — Audit RGPD 2025
 * Version 3 — onglet nommé par la RÉPONSE au champ id="nom_etablissement"
 *
 * DÉPLOIEMENT : Applications Web > Accès "Tout le monde"
 */

var SPREADSHEET_ID = 'COLLE_ICI_LIDENTIFIANT_DE_TON_GOOGLE_SHEET';

// ─────────────────────────────────────────────
// POINT D'ENTRÉE — reçoit les réponses HTML
// ─────────────────────────────────────────────
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = resolveSheet(data);
    appendResponse(sheet, data);
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Test GET : ouvrir l'URL dans le navigateur doit afficher {"status":"ok"}
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', message: 'Récepteur RGPD Unapei92 actif' }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─────────────────────────────────────────────
// RÉSOLUTION DU NOM D'ONGLET
//
// Logique simple et fiable :
//   1. Chercher dans data.responses la réponse dont l'id === 'nom_etablissement'
//   2. Utiliser sa valeur (answer) comme nom d'onglet
//   3. Fallback sur data.type si le champ est absent ou vide
// ─────────────────────────────────────────────
function resolveSheet(data) {
  var nomEtab = '';

  if (data.responses && data.responses.length > 0) {
    data.responses.forEach(function (r) {
      if (r.id === 'nom_etablissement' && r.answer && r.answer.trim() !== '') {
        nomEtab = r.answer.trim();
      }
    });
  }

  // Fallback : si le champ est absent ou non renseigné, utiliser le type
  var sheetName = nomEtab || data.type || 'Sans nom';

  // Nettoyer les caractères interdits dans les noms d'onglets Google Sheets
  // Interdits : / \ ? * [ ] :  — max 100 caractères
  sheetName = sheetName.replace(/[\/\\?*\[\]:]/g, '-').substring(0, 100);

  return getOrCreateSheet(sheetName);
}

// ─────────────────────────────────────────────
// CRÉATION OU RÉCUPÉRATION D'UN ONGLET
// ─────────────────────────────────────────────
function getOrCreateSheet(name) {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

// ─────────────────────────────────────────────
// ÉCRITURE DE LA RÉPONSE
// Aligne les colonnes sur les en-têtes existants
// Ajoute les nouvelles colonnes en fin si besoin
// ─────────────────────────────────────────────
function appendResponse(sheet, data) {
  var lastRow = sheet.getLastRow();
  var lastCol = sheet.getLastColumn();

  // Lire les en-têtes existants (ligne 1)
  var existingHeaders = [];
  if (lastRow >= 1 && lastCol >= 1) {
    existingHeaders = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  }

  // En-têtes fixes de début + une colonne par question
  var expectedHeaders = ['Date soumission', 'Type formulaire', 'Établissement'];
  data.responses.forEach(function (r) {
    if (r.question && expectedHeaders.indexOf(r.question) === -1) {
      expectedHeaders.push(r.question);
    }
  });

  // Premier enregistrement : écrire + formater les en-têtes
  if (existingHeaders.length === 0) {
    sheet.appendRow(expectedHeaders);
    existingHeaders = expectedHeaders;
    var headerRange = sheet.getRange(1, 1, 1, existingHeaders.length);
    headerRange.setFontWeight('bold');
    headerRange.setBackground('#1B4F8A');
    headerRange.setFontColor('#ffffff');
    sheet.setColumnWidth(1, 160);
    sheet.setColumnWidth(2, 120);
    sheet.setColumnWidth(3, 200);
  }

  // Ajouter les colonnes manquantes à droite si nouvelle question apparaît
  expectedHeaders.forEach(function (h) {
    if (existingHeaders.indexOf(h) === -1) {
      existingHeaders.push(h);
      var newHeaderCell = sheet.getRange(1, existingHeaders.length);
      newHeaderCell.setValue(h);
      newHeaderCell.setFontWeight('bold');
      newHeaderCell.setBackground('#1B4F8A');
      newHeaderCell.setFontColor('#ffffff');
    }
  });

  // Construire la ligne alignée sur les en-têtes
  var row = new Array(existingHeaders.length).fill('');
  row[0] = new Date();
  row[1] = data.type || '';

  // Colonne "Établissement" = réponse au champ id='nom_etablissement'
  data.responses.forEach(function (r) {
    if (r.id === 'nom_etablissement') {
      row[2] = r.answer || '';
    }
  });

  // Placer chaque réponse dans la bonne colonne (par libellé de question)
  data.responses.forEach(function (r) {
    var idx = existingHeaders.indexOf(r.question);
    if (idx >= 0) {
      row[idx] = r.answer || '';
    } else {
      // Nouvelle colonne inconnue : ajouter en fin
      existingHeaders.push(r.question);
      var newHeaderCell = sheet.getRange(1, existingHeaders.length);
      newHeaderCell.setValue(r.question);
      newHeaderCell.setFontWeight('bold');
      newHeaderCell.setBackground('#1B4F8A');
      newHeaderCell.setFontColor('#ffffff');
      row.push(r.answer || '');
    }
  });

  sheet.appendRow(row);

  // Formater la date
  sheet.getRange(sheet.getLastRow(), 1).setNumberFormat('dd/mm/yyyy hh:mm');
}