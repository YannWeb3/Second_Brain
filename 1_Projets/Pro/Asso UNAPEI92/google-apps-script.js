/**
 * GOOGLE APPS SCRIPT - UNAPEI92 (v2.0 — onglets par établissement)
 * Adapté de send_to_sheets.gs — chaque établissement a son propre onglet
 */

const SPREADSHEET_ID = '1yMJI_Nrt6k1EGnkHAbdfj0mc1PFNBsOLUdbu0TpH6b4';

// Types autorisés (avec et sans _RGPD)
const CONFIG = {
  TYPES: [
    'IME_RGPD', 'IME',
    'SAVS_RGPD', 'SAVS',
    'SESSAD_RGPD', 'SESSAD',
    'ESAT_RGPD', 'ESAT',
    'EANM_RGPD', 'EANM',
    'EAM_RGPD', 'EAM',
    'CMPP_RGPD', 'CMPP',
    'SI-IT', 'SIIT_RGPD',
    'Direction_RGPD', 'Direction',
    'Qualite_RGPD', 'Qualite',
    'Donateurs_RGPD', 'Donateurs',
    'DAF_RGPD', 'DAF',
    'RH_RGPD', 'RH',
    'Paie_RGPD', 'Paie',
    'Communication_RGPD', 'Communication'
  ]
};

// ============================================
// POST — réception des réponses
// ============================================
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = resolveSheet(data);
    appendResponse(sheet, data);
    return createResponse({ status: 'success', message: 'Réponse enregistrée' });
  } catch (err) {
    return createResponse({ status: 'error', message: err.toString() });
  }
}

// ============================================
// GET — health check
// ============================================
function doGet(e) {
  return createResponse({
    status: 'ok',
    message: 'Service UNAPEI92 v2.0 actif (onglets par établissement)',
    timestamp: new Date().toISOString(),
    version: '2.0.0'
  });
}

// ============================================
// OPTIONS — CORS
// ============================================
function doOptions(e) {
  return ContentService.createTextOutput('')
    .setHeaders({
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
}

// ============================================
// RÉSOLUTION DE L'ONGLET
// ============================================
function resolveSheet(data) {
  let nomEtab = '';

  if (data.responses && data.responses.length > 0) {
    data.responses.forEach(r => {
      if (r.id === 'nom_etablissement' && r.answer && r.answer.trim() !== '') {
        nomEtab = r.answer.trim();
      }
    });
  }

  const sheetName = nomEtab || data.type || 'Sans nom';
  const cleanName = sheetName.replace(/[\/\\?*\[\]:]/g, '-').substring(0, 100);

  return getOrCreateSheet(cleanName);
}

// ============================================
// CRÉER / RÉCUPÉRER ONGLET
// ============================================
function getOrCreateSheet(name) {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.setFrozenRows(1);
    Logger.log('Onglet créé : ' + name);
  }
  return sheet;
}

// ============================================
// AJOUTER RÉPONSE
// ============================================
function appendResponse(sheet, data) {
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();

  let existingHeaders = [];
  if (lastRow >= 1 && lastCol >= 1) {
    existingHeaders = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  }

   // En-têtes fixes + questions (exclure nom_etablissement car déjà colonne fixe)
   let expectedHeaders = ['Date soumission', 'Type formulaire', 'Établissement'];
   data.responses.forEach(r => {
     if (r.question && expectedHeaders.indexOf(r.question) === -1 && r.id !== 'nom_etablissement') {
       expectedHeaders.push(r.question);
     }
   });

  // Premier enregistrement : écrire + formater
  if (existingHeaders.length === 0) {
    sheet.appendRow(expectedHeaders);
    existingHeaders = expectedHeaders;
    formatHeaderRow(sheet, expectedHeaders.length);
    sheet.setColumnWidth(1, 160);
    sheet.setColumnWidth(2, 120);
    sheet.setColumnWidth(3, 200);
  }

  // Ajouter colonnes manquantes
  let newCols = false;
  expectedHeaders.forEach(h => {
    if (existingHeaders.indexOf(h) === -1) {
      existingHeaders.push(h);
      newCols = true;
    }
  });
  if (newCols) {
    sheet.getRange(1, 1, 1, existingHeaders.length).setValues([existingHeaders]);
    formatHeaderRow(sheet, existingHeaders.length);
  }

  // Construire ligne
  const row = new Array(existingHeaders.length).fill('');
  row[0] = new Date();
  row[1] = data.type || '';

  // Colonne Établissement
  data.responses.forEach(r => {
    if (r.id === 'nom_etablissement') {
      row[2] = r.answer || '';
    }
  });

   // Placer réponses (skip nom_etablissement car déjà dans colonne fixe)
   data.responses.forEach(r => {
     if (r.id === 'nom_etablissement') return;
     const idx = existingHeaders.indexOf(r.question);
     if (idx >= 0) {
       row[idx] = r.answer || '';
     } else {
       existingHeaders.push(r.question);
       row.push(r.answer || '');
     }
   });

  sheet.appendRow(row);
  sheet.getRange(sheet.getLastRow(), 1).setNumberFormat('dd/mm/yyyy hh:mm');
}

// ============================================
// FORMAT EN-TÊTES
// ============================================
function formatHeaderRow(sheet, colCount) {
  sheet.getRange(1, 1, 1, colCount)
    .setFontWeight('bold')
    .setBackground('#0055A4')
    .setFontColor('#FFFFFF');
}

// ============================================
// RÉPONSE HTTP
// ============================================
function createResponse(data, headers) {
  let out = ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
  if (headers) {
    Object.keys(headers).forEach(k => out = out.setHeader(k, headers[k]));
  }
  return out;
}

// ============================================
// MAINTENANCE
// ============================================
function initialiserFeuilles() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  CONFIG.TYPES.forEach(type => {
    if (!ss.getSheetByName(type)) {
      ss.insertSheet(type);
    }
  });
  const def = ss.getSheetByName('Feuille 1');
  if (def && def.getLastRow() === 0) ss.deleteSheet(def);
  Logger.log('Initialisation OK — onglets créés au premier envoi par établissement.');
}

function testerConfiguration() {
  try {
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    Logger.log('✓ Spreadsheet : ' + ss.getName());
    Logger.log('✓ URL : ' + ss.getUrl());
    Logger.log('✓ Types : ' + CONFIG.TYPES.join(', '));
    getOrCreateSheet('TEST_TEMP');
    ss.deleteSheet(ss.getSheetByName('TEST_TEMP'));
    Logger.log('\n=== Configuration validée (v2.0) ===');
  } catch (e) {
    Logger.log('✗ ERREUR : ' + e);
    throw e;
  }
}

function getStatistiques() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  Logger.log('=== STATS ===');
  ss.getSheets().forEach(s => {
    const n = s.getName();
    const r = s.getLastRow();
    const c = s.getLastColumn();
    Logger.log(n + ' : ' + Math.max(0, r-1) + ' réponse(s), ' + c + ' colonnes');
  });
}
