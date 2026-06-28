<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rapport Red Team — EWA App</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --red: #C0392B;
    --red-light: #FDEDEC;
    --red-mid: #E74C3C;
    --orange: #D35400;
    --orange-light: #FEF5E7;
    --yellow: #B7950B;
    --yellow-light: #FEFDE7;
    --blue: #1A5276;
    --blue-light: #EBF5FB;
    --green: #1E8449;
    --green-light: #EAFAF1;
    --gray-900: #0D1117;
    --gray-800: #161B22;
    --gray-700: #21262D;
    --gray-600: #30363D;
    --gray-400: #6E7681;
    --gray-200: #C9D1D9;
    --gray-100: #F0F2F4;
    --gray-50: #F8F9FA;
    --white: #FFFFFF;
    --font-sans: 'Inter', system-ui, sans-serif;
    --font-mono: 'IBM Plex Mono', 'Courier New', monospace;
  }

  body {
    font-family: var(--font-sans);
    background: var(--gray-50);
    color: var(--gray-900);
    font-size: 14px;
    line-height: 1.6;
  }

  /* COVER */
  .cover {
    background: var(--gray-900);
    color: var(--white);
    padding: 64px 80px 56px;
    position: relative;
    overflow: hidden;
  }
  .cover::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--red-mid);
  }
  .cover-tag {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.12em;
    color: var(--red-mid);
    text-transform: uppercase;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .cover-tag::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 1px;
    background: var(--red-mid);
  }
  .cover h1 {
    font-size: 40px;
    font-weight: 300;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 8px;
  }
  .cover h1 strong { font-weight: 600; }
  .cover-sub {
    font-size: 16px;
    color: var(--gray-400);
    margin-bottom: 48px;
    font-weight: 300;
  }
  .cover-meta {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 32px;
    padding-top: 40px;
    border-top: 1px solid var(--gray-700);
  }
  .cover-meta-item label {
    display: block;
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.1em;
    color: var(--gray-400);
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .cover-meta-item span {
    font-size: 14px;
    font-weight: 500;
    color: var(--white);
  }
  .cover-score {
    position: absolute;
    right: 80px;
    top: 50%;
    transform: translateY(-50%);
    text-align: center;
  }
  .cover-score-num {
    font-family: var(--font-mono);
    font-size: 72px;
    font-weight: 500;
    color: var(--red-mid);
    line-height: 1;
  }
  .cover-score-label {
    font-size: 11px;
    color: var(--gray-400);
    margin-top: 4px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* LAYOUT */
  .container { max-width: 960px; margin: 0 auto; padding: 48px 40px; }

  /* SECTION HEADERS */
  .section-header {
    display: flex;
    align-items: baseline;
    gap: 16px;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--gray-200);
  }
  .section-num {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--gray-400);
    letter-spacing: 0.08em;
  }
  .section-header h2 {
    font-size: 20px;
    font-weight: 600;
    letter-spacing: -0.01em;
  }

  /* SUMMARY CARDS */
  .summary-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 40px;
  }
  .summary-card {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: 8px;
    padding: 20px;
    text-align: center;
  }
  .summary-card .num {
    font-family: var(--font-mono);
    font-size: 36px;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 6px;
  }
  .summary-card .lbl {
    font-size: 11px;
    color: var(--gray-400);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .summary-card.crit { border-top: 3px solid var(--red-mid); }
  .summary-card.crit .num { color: var(--red); }
  .summary-card.high { border-top: 3px solid var(--orange); }
  .summary-card.high .num { color: var(--orange); }
  .summary-card.med { border-top: 3px solid var(--yellow); }
  .summary-card.med .num { color: var(--yellow); }
  .summary-card.ok { border-top: 3px solid var(--green); }
  .summary-card.ok .num { color: var(--green); }

  /* FINDINGS */
  .finding {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: 8px;
    margin-bottom: 16px;
    overflow: hidden;
  }
  .finding-header {
    display: grid;
    grid-template-columns: 4px 1fr auto;
    gap: 0;
    align-items: stretch;
  }
  .finding-stripe { }
  .finding-stripe.crit { background: var(--red-mid); }
  .finding-stripe.high { background: var(--orange); }
  .finding-stripe.med { background: var(--yellow); }
  .finding-stripe.low { background: var(--blue); }
  .finding-stripe.ok { background: var(--green); }

  .finding-head-content {
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .finding-id {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--gray-400);
    min-width: 36px;
  }
  .finding-title-text {
    font-size: 15px;
    font-weight: 600;
    flex: 1;
  }
  .severity-badge {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.08em;
    padding: 3px 10px;
    border-radius: 4px;
    white-space: nowrap;
    margin-right: 20px;
  }
  .severity-badge.crit { background: var(--red-light); color: var(--red); }
  .severity-badge.high { background: var(--orange-light); color: var(--orange); }
  .severity-badge.med { background: var(--yellow-light); color: var(--yellow); }
  .severity-badge.low { background: var(--blue-light); color: var(--blue); }
  .severity-badge.ok { background: var(--green-light); color: var(--green); }

  .finding-body { padding: 0 20px 20px 20px; padding-left: 68px; }
  .finding-body p { color: #444; line-height: 1.7; margin-bottom: 12px; }

  .finding-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
  }
  .meta-pill {
    font-family: var(--font-mono);
    font-size: 11px;
    background: var(--gray-100);
    color: var(--gray-400);
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid var(--gray-200);
  }

  .evidence-block {
    background: var(--gray-900);
    border-radius: 6px;
    padding: 14px 16px;
    margin: 12px 0;
  }
  .evidence-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.1em;
    color: var(--red-mid);
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .evidence-block code {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--gray-200);
    display: block;
    line-height: 1.8;
  }
  .evidence-block code .hl { color: #58A6FF; }
  .evidence-block code .val { color: #7EE787; }
  .evidence-block code .warn { color: #F0883E; }
  .evidence-block code .danger { color: var(--red-mid); }

  .reco-block {
    background: var(--green-light);
    border: 1px solid #A9DFBF;
    border-radius: 6px;
    padding: 12px 16px;
    margin-top: 12px;
  }
  .reco-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.1em;
    color: var(--green);
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .reco-block p { color: #1A5C35; margin-bottom: 0; font-size: 13px; }
  .reco-block code {
    font-family: var(--font-mono);
    font-size: 11px;
    background: rgba(0,0,0,0.08);
    padding: 1px 5px;
    border-radius: 3px;
  }

  /* ATTACK SURFACE */
  .route-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .route-table th {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--gray-400);
    text-align: left;
    padding: 8px 12px;
    border-bottom: 1px solid var(--gray-200);
    background: var(--gray-50);
  }
  .route-table td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--gray-100);
    vertical-align: middle;
  }
  .route-table tr:last-child td { border-bottom: none; }
  .route-table tr:hover td { background: var(--gray-50); }
  .route-table code {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--blue);
  }
  .status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    margin-right: 6px;
  }
  .status-dot.crit { background: var(--red-mid); }
  .status-dot.high { background: var(--orange); }
  .status-dot.med { background: var(--yellow); }
  .status-dot.ok { background: var(--green); }

  /* HEADER TABLE */
  .header-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 24px; }
  .header-table th {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--gray-400);
    text-align: left;
    padding: 8px 12px;
    background: var(--gray-50);
    border-bottom: 1px solid var(--gray-200);
  }
  .header-table td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--gray-100);
    font-family: var(--font-mono);
    font-size: 12px;
    vertical-align: middle;
  }
  .header-table tr:last-child td { border-bottom: none; }
  .tag-ok { color: var(--green); font-weight: 500; }
  .tag-fail { color: var(--red); font-weight: 500; }
  .tag-warn { color: var(--orange); font-weight: 500; }

  /* SCOPE */
  .scope-box {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 24px;
  }
  .scope-box h3 {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 12px;
    color: var(--gray-400);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-family: var(--font-mono);
  }
  .scope-box ul { list-style: none; }
  .scope-box ul li {
    padding: 5px 0;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid var(--gray-100);
  }
  .scope-box ul li:last-child { border-bottom: none; }
  .scope-box ul li::before {
    content: '→';
    font-family: var(--font-mono);
    color: var(--gray-400);
    font-size: 12px;
  }

  /* TIMELINE */
  .timeline { margin-bottom: 32px; }
  .timeline-item {
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: 20px;
    padding: 12px 0;
    border-bottom: 1px solid var(--gray-100);
  }
  .timeline-item:last-child { border-bottom: none; }
  .timeline-time {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--gray-400);
    padding-top: 2px;
  }
  .timeline-desc { font-size: 13px; }
  .timeline-desc strong { font-weight: 600; }

  /* FOOTER */
  .footer {
    background: var(--gray-900);
    color: var(--gray-400);
    padding: 32px 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.06em;
    margin-top: 40px;
  }
  .footer a { color: var(--gray-400); text-decoration: none; }

  .divider {
    height: 1px;
    background: var(--gray-200);
    margin: 40px 0;
  }

  .callout {
    background: var(--red-light);
    border-left: 3px solid var(--red-mid);
    border-radius: 0 6px 6px 0;
    padding: 14px 18px;
    margin: 20px 0;
    font-size: 13px;
    color: #7B241C;
    line-height: 1.6;
  }

  @media print {
    body { background: white; }
    .cover-score { position: static; transform: none; margin-top: 24px; }
    .cover-meta { grid-template-columns: repeat(2, 1fr); }
  }

  @media (max-width: 700px) {
    .cover { padding: 32px 24px; }
    .cover h1 { font-size: 28px; }
    .cover-score { display: none; }
    .cover-meta { grid-template-columns: repeat(2, 1fr); }
    .container { padding: 32px 20px; }
    .summary-grid { grid-template-columns: repeat(2, 1fr); }
  }
</style>
</head>
<body>

<!-- COVER -->
<div class="cover">
  <div class="cover-tag">Rapport Red Team · Confidentiel</div>
  <h1><strong>Audit Sécurité</strong><br>EWA App</h1>
  <p class="cover-sub">Editing Wizard Agency — Application interne de pilotage opérationnel</p>
  <div class="cover-score">
    <div class="cover-score-num">9.1</div>
    <div class="cover-score-label">CVSS max</div>
  </div>
  <div class="cover-meta">
    <div class="cover-meta-item">
      <label>Cible</label>
      <span>ewa-app.vercel.app</span>
    </div>
    <div class="cover-meta-item">
      <label>Date</label>
      <span>19 juin 2026</span>
    </div>
    <div class="cover-meta-item">
      <label>Type</label>
      <span>Boîte grise</span>
    </div>
    <div class="cover-meta-item">
      <label>Statut</label>
      <span style="color:#E74C3C">⬤ Critique</span>
    </div>
  </div>
</div>

<!-- MAIN -->
<div class="container">

  <!-- EXECUTIVE SUMMARY -->
  <div class="section-header" style="margin-top:0">
    <span class="section-num">01</span>
    <h2>Résumé exécutif</h2>
  </div>

  <div class="callout">
    <strong>Constat principal :</strong> Un compte Monteur (rôle EDITOR) accède sans restriction à l'intégralité des données de l'agence — données financières, emails de tous les membres et clients, configuration système. L'absence de contrôle d'accès par rôle côté serveur constitue une violation critique du principe du moindre privilège et expose l'application à des risques RGPD immédiats.
  </div>

  <div class="summary-grid">
    <div class="summary-card crit">
      <div class="num">3</div>
      <div class="lbl">Critiques</div>
    </div>
    <div class="summary-card high">
      <div class="num">2</div>
      <div class="lbl">Élevées</div>
    </div>
    <div class="summary-card med">
      <div class="num">2</div>
      <div class="lbl">Moyennes</div>
    </div>
    <div class="summary-card ok">
      <div class="num">4</div>
      <div class="lbl">OK / conformes</div>
    </div>
  </div>

  <div class="divider"></div>

  <!-- SCOPE -->
  <div class="section-header">
    <span class="section-num">02</span>
    <h2>Périmètre & Méthodologie</h2>
  </div>

  <div class="scope-box">
    <h3>Cibles testées</h3>
    <ul>
      <li>https://ewa-app.vercel.app (frontend Next.js)</li>
      <li>https://ogwqvijwbzzzmswgifvx.supabase.co (backend Supabase)</li>
      <li>Compte test Éditeur : editor@ewa-test.com (rôle EDITOR / Marc Monteur)</li>
      <li>13 routes applicatives + API REST Supabase</li>
    </ul>
  </div>

  <div class="scope-box">
    <h3>Phases de test</h3>
    <div class="timeline">
      <div class="timeline-item">
        <div class="timeline-time">Phase 1</div>
        <div class="timeline-desc"><strong>Reconnaissance passive</strong> — headers HTTP, stack technique, bundle JS, clés exposées, cartographie des routes</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-time">Phase 2</div>
        <div class="timeline-desc"><strong>Tests RLS Supabase</strong> — accès anonyme, accès authentifié, IDOR sur tables publiques, tentatives d'écriture</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-time">Phase 3</div>
        <div class="timeline-desc"><strong>Tests RBAC applicatif</strong> — accès aux routes avec token Éditeur, inspection du contenu rendu, extraction de données sensibles</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-time">Phase 4</div>
        <div class="timeline-desc"><strong>Analyse JWT & session</strong> — décodage du token, localisation du claim de rôle, vecteurs d'élévation de privilèges</div>
      </div>
    </div>
  </div>

  <div class="divider"></div>

  <!-- HEADERS -->
  <div class="section-header">
    <span class="section-num">03</span>
    <h2>Analyse des headers HTTP</h2>
  </div>

  <table class="header-table">
    <thead>
      <tr>
        <th>Header</th>
        <th>Valeur observée</th>
        <th>Statut</th>
        <th>Commentaire</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Strict-Transport-Security</td>
        <td>max-age=31536000</td>
        <td class="tag-ok">✓ OK</td>
        <td>HSTS actif, force HTTPS</td>
      </tr>
      <tr>
        <td>X-Frame-Options</td>
        <td>DENY</td>
        <td class="tag-ok">✓ OK</td>
        <td>Protection clickjacking</td>
      </tr>
      <tr>
        <td>X-Content-Type-Options</td>
        <td>nosniff</td>
        <td class="tag-ok">✓ OK</td>
        <td>Protection MIME sniffing</td>
      </tr>
      <tr>
        <td>Referrer-Policy</td>
        <td>strict-origin-when-cross-origin</td>
        <td class="tag-ok">✓ OK</td>
        <td>Fuite d'URL limitée</td>
      </tr>
      <tr>
        <td>Content-Security-Policy</td>
        <td>script-src 'self' <span class="tag-fail">'unsafe-inline'</span></td>
        <td class="tag-fail">✗ FAIL</td>
        <td>unsafe-inline annule la protection XSS</td>
      </tr>
      <tr>
        <td>Access-Control-Allow-Origin</td>
        <td><span class="tag-fail">*</span></td>
        <td class="tag-fail">✗ FAIL</td>
        <td>Tout domaine peut faire des requêtes cross-origin</td>
      </tr>
    </tbody>
  </table>

  <div class="divider"></div>

  <!-- FINDINGS -->
  <div class="section-header">
    <span class="section-num">04</span>
    <h2>Vulnérabilités identifiées</h2>
  </div>

  <!-- F-01 -->
  <div class="finding">
    <div class="finding-header">
      <div class="finding-stripe crit"></div>
      <div class="finding-head-content">
        <span class="finding-id">F-01</span>
        <span class="finding-title-text">Broken Access Control — /equipe : exposition de l'annuaire interne</span>
      </div>
      <span class="severity-badge crit">CRITIQUE · CVSS 9.1</span>
    </div>
    <div class="finding-body">
      <div class="finding-meta">
        <span class="meta-pill">CWE-284</span>
        <span class="meta-pill">OWASP A01:2021</span>
        <span class="meta-pill">Route : /equipe</span>
        <span class="meta-pill">Rôle testeur : EDITOR</span>
      </div>
      <p>Un compte Monteur accède à la page <code>/equipe</code> et obtient l'intégralité de l'annuaire de l'agence : emails personnels, numéros de téléphone et UUIDs de tous les membres. Aucune vérification de rôle n'est effectuée côté serveur avant de rendre cette page.</p>
      <div class="evidence-block">
        <div class="evidence-label">Preuve — Données extraites de /equipe (compte EDITOR)</div>
        <code>
          <span class="hl">Emails exposés (17) :</span><br>
          &nbsp;&nbsp;<span class="danger">charlesdp@gmail.com</span><br>
          &nbsp;&nbsp;<span class="danger">ianne@ewa-dev.com</span><br>
          &nbsp;&nbsp;<span class="danger">da@ewa-test.com</span><br>
          &nbsp;&nbsp;<span class="danger">admin@ewa-test.com</span><br>
          &nbsp;&nbsp;<span class="danger">pacome.freelance@gmail.com</span><br>
          &nbsp;&nbsp;[+12 autres]<br><br>
          <span class="hl">Téléphones :</span> <span class="warn">0238019778, 0033 2.34 2...</span><br>
          <span class="hl">UUIDs membres :</span> <span class="warn">53 identifiants uniques</span>
        </code>
      </div>
      <div class="reco-block">
        <div class="reco-label">Remédiation</div>
        <p>Ajouter un guard middleware sur la route <code>/equipe</code> vérifiant que <code>session.user.app_metadata.role === 'ADMIN'</code>. En Next.js, implémenter dans <code>middleware.ts</code> ou via un HOC de protection. La vérification doit se faire côté serveur (SSR/API route), jamais uniquement côté client.</p>
      </div>
    </div>
  </div>

  <!-- F-02 -->
  <div class="finding">
    <div class="finding-header">
      <div class="finding-stripe crit"></div>
      <div class="finding-head-content">
        <span class="finding-id">F-02</span>
        <span class="finding-title-text">Exposition données financières — /banque accessible à un Monteur</span>
      </div>
      <span class="severity-badge crit">CRITIQUE · CVSS 9.1</span>
    </div>
    <div class="finding-body">
      <div class="finding-meta">
        <span class="meta-pill">CWE-284</span>
        <span class="meta-pill">OWASP A01:2021</span>
        <span class="meta-pill">RGPD Art.32</span>
        <span class="meta-pill">Route : /banque</span>
      </div>
      <p>La section financière de l'agence est accessible sans restriction à un Monteur. Les données incluent des transactions avec montants en clair et 312 UUIDs de transactions. Cette exposition constitue une violation potentielle du RGPD (Art. 32 — sécurité du traitement) et un risque business majeur.</p>
      <div class="evidence-block">
        <div class="evidence-label">Preuve — Données extraites de /banque (compte EDITOR)</div>
        <code>
          <span class="hl">HTTP 200</span> — <span class="val">253 735 octets</span> de données rendues<br><br>
          <span class="hl">Transactions exposées :</span><br>
          &nbsp;&nbsp;Montants : <span class="warn">81€, 49€, 51€, 70€...</span><br>
          &nbsp;&nbsp;UUIDs : <span class="danger">312 identifiants de transactions</span><br>
          &nbsp;&nbsp;55e066b4-082b-4d3a-a8c9-e746e913f133<br>
          &nbsp;&nbsp;019ed038-4c3c-7a09-8121-67ff0afd828e<br>
          &nbsp;&nbsp;[+310 autres]
        </code>
      </div>
      <div class="reco-block">
        <div class="reco-label">Remédiation</div>
        <p>Restreindre <code>/banque</code> aux rôles <code>ADMIN</code> et <code>FINANCE</code> uniquement. Implémenter la vérification dans le middleware Next.js. Côté Supabase, activer la RLS sur la table de transactions avec une policy <code>auth.jwt() ->> 'role' = 'ADMIN'</code>.</p>
      </div>
    </div>
  </div>

  <!-- F-03 -->
  <div class="finding">
    <div class="finding-header">
      <div class="finding-stripe crit"></div>
      <div class="finding-head-content">
        <span class="finding-id">F-03</span>
        <span class="finding-title-text">Énumération de comptes via /parametres — emails Admin exposés</span>
      </div>
      <span class="severity-badge crit">CRITIQUE · CVSS 8.8</span>
    </div>
    <div class="finding-body">
      <div class="finding-meta">
        <span class="meta-pill">CWE-284</span>
        <span class="meta-pill">CWE-200</span>
        <span class="meta-pill">OWASP A01:2021</span>
        <span class="meta-pill">Route : /parametres</span>
      </div>
      <p>La page de paramètres expose tous les emails de la plateforme, y compris celui du compte Administrateur. Un attaquant avec un compte Monteur peut énumérer tous les utilisateurs et cibler le compte Admin pour des attaques ultérieures (phishing, credential stuffing, réinitialisation de mot de passe).</p>
      <div class="evidence-block">
        <div class="evidence-label">Preuve — Emails extraits de /parametres (compte EDITOR)</div>
        <code>
          <span class="danger">admin@ewa-test.com</span> &nbsp;← compte Admin exposé<br>
          <span class="warn">ianne@ewa-dev.com</span><br>
          <span class="warn">charlesdp@gmail.com</span><br>
          <span class="warn">da@ewa-test.com</span><br>
          <span class="warn">editor@ewa-test.com</span><br>
          [+7 autres · 12 emails total · 274 UUIDs]
        </code>
      </div>
      <div class="reco-block">
        <div class="reco-label">Remédiation</div>
        <p>Restreindre <code>/parametres</code> au rôle <code>ADMIN</code>. Si certaines sections doivent être accessibles aux éditeurs, implémenter un découpage par composant avec vérification granulaire. Ne jamais exposer la liste des utilisateurs à un rôle non-admin.</p>
      </div>
    </div>
  </div>

  <!-- F-04 -->
  <div class="finding">
    <div class="finding-header">
      <div class="finding-stripe high"></div>
      <div class="finding-head-content">
        <span class="finding-id">F-04</span>
        <span class="finding-title-text">Données clients externes exposées — /clients (violation RGPD)</span>
      </div>
      <span class="severity-badge high">ÉLEVÉ · CVSS 8.1</span>
    </div>
    <div class="finding-body">
      <div class="finding-meta">
        <span class="meta-pill">CWE-359</span>
        <span class="meta-pill">RGPD Art.5 §1f</span>
        <span class="meta-pill">OWASP A01:2021</span>
        <span class="meta-pill">Route : /clients</span>
      </div>
      <p>Les données personnelles de clients externes (emails, montants de contrats) sont accessibles à un Monteur sans que son rôle ne le justifie métier. En droit RGPD, le principe de minimisation des données (Art. 5 §1c) impose de ne donner accès qu'aux données strictement nécessaires à l'exercice de la fonction.</p>
      <div class="evidence-block">
        <div class="evidence-label">Preuve — Données clients extraites (compte EDITOR)</div>
        <code>
          <span class="hl">11 emails de clients :</span><br>
          &nbsp;&nbsp;<span class="warn">jgcoachingonline@gmail.com</span><br>
          &nbsp;&nbsp;<span class="warn">etienneniel@gmail.com</span><br>
          &nbsp;&nbsp;<span class="warn">liviocoaching@gmail.com</span><br>
          &nbsp;&nbsp;[+8 autres]<br><br>
          <span class="hl">Montants de contrats :</span> <span class="warn">216€ · 2 089€ · 288€ · 72€ · 306€</span><br>
          <span class="hl">Volume :</span> <span class="danger">1 214 944 octets · 723 UUIDs</span>
        </code>
      </div>
      <div class="reco-block">
        <div class="reco-label">Remédiation</div>
        <p>Évaluer si un Monteur a réellement besoin d'accéder aux données clients. Si non, restreindre <code>/clients</code> aux rôles <code>ADMIN</code> et <code>COMMERCIAL</code>. Documenter la base légale RGPD pour chaque rôle ayant accès aux données clients (registre de traitement).</p>
      </div>
    </div>
  </div>

  <!-- F-05 -->
  <div class="finding">
    <div class="finding-header">
      <div class="finding-stripe high"></div>
      <div class="finding-head-content">
        <span class="finding-id">F-05</span>
        <span class="finding-title-text">CSP unsafe-inline + CORS wildcard — surface XSS amplifiée</span>
      </div>
      <span class="severity-badge high">ÉLEVÉ · CVSS 7.4</span>
    </div>
    <div class="finding-body">
      <div class="finding-meta">
        <span class="meta-pill">CWE-1021</span>
        <span class="meta-pill">CWE-942</span>
        <span class="meta-pill">OWASP A05:2021</span>
      </div>
      <p>La directive <code>script-src 'unsafe-inline'</code> dans la CSP neutralise la principale protection contre les attaques XSS qu'offre ce mécanisme. En parallèle, le header <code>Access-Control-Allow-Origin: *</code> autorise n'importe quel domaine à effectuer des requêtes cross-origin vers l'application. La combinaison des deux élargit considérablement la surface d'exploitation en cas de XSS découverte.</p>
      <div class="evidence-block">
        <div class="evidence-label">Headers observés</div>
        <code>
          content-security-policy: default-src 'self';<br>
          &nbsp;&nbsp;<span class="danger">script-src 'self' 'unsafe-inline'</span> ...<br><br>
          <span class="danger">access-control-allow-origin: *</span>
        </code>
      </div>
      <div class="reco-block">
        <div class="reco-label">Remédiation</div>
        <p>Remplacer <code>'unsafe-inline'</code> par des nonces CSP (<code>'nonce-{random}'</code>) générés par requête — Next.js supporte cela nativement depuis la v13.4. Restreindre <code>Access-Control-Allow-Origin</code> aux domaines explicitement autorisés. Si l'app n'expose pas d'API publique, supprimer ce header ou le fixer à <code>https://ewa-app.vercel.app</code>.</p>
      </div>
    </div>
  </div>

  <!-- F-06 -->
  <div class="finding">
    <div class="finding-header">
      <div class="finding-stripe med"></div>
      <div class="finding-head-content">
        <span class="finding-id">F-06</span>
        <span class="finding-title-text">Rôle stocké dans user_metadata JWT — vecteur d'élévation potentiel</span>
      </div>
      <span class="severity-badge med">MOYEN · À confirmer</span>
    </div>
    <div class="finding-body">
      <div class="finding-meta">
        <span class="meta-pill">CWE-269</span>
        <span class="meta-pill">OWASP A01:2021</span>
        <span class="meta-pill">Supabase Auth</span>
      </div>
      <p>Le rôle <code>EDITOR</code> est stocké dans <code>user_metadata</code> du JWT Supabase. Ce champ est modifiable par l'utilisateur lui-même via l'API <code>/auth/v1/user</code> (PUT). Si l'application utilise ce champ pour ses décisions d'autorisation côté serveur, une élévation de privilèges est possible sans compte Admin. Le champ sécurisé pour les rôles est <code>app_metadata</code>, modifiable uniquement via la <code>service_role</code> key.</p>
      <div class="evidence-block">
        <div class="evidence-label">JWT payload observé</div>
        <code>
          {<br>
          &nbsp;&nbsp;"role": <span class="val">"authenticated"</span>,<br>
          &nbsp;&nbsp;"email": <span class="val">"editor@ewa-test.com"</span>,<br>
          &nbsp;&nbsp;<span class="danger">"user_metadata"</span>: {<br>
          &nbsp;&nbsp;&nbsp;&nbsp;<span class="danger">"role": "EDITOR"</span>,  <span class="warn">← modifiable par l'user</span><br>
          &nbsp;&nbsp;&nbsp;&nbsp;"full_name": "Marc (Monteur)"<br>
          &nbsp;&nbsp;},<br>
          &nbsp;&nbsp;"app_metadata": { ... }  <span class="val">← champ sécurisé</span><br>
          }
        </code>
      </div>
      <div class="reco-block">
        <div class="reco-label">Remédiation</div>
        <p>Stocker le rôle applicatif exclusivement dans <code>app_metadata</code> (via Admin SDK / service_role). Dans le code applicatif, lire le rôle via <code>session.user.app_metadata.role</code> et jamais via <code>user_metadata</code>. Vérifier avec : <code>supabaseAdmin.auth.admin.updateUserById(uid, { app_metadata: { role: 'EDITOR' } })</code>.</p>
      </div>
    </div>
  </div>

  <!-- F-07 -->
  <div class="finding">
    <div class="finding-header">
      <div class="finding-stripe med"></div>
      <div class="finding-head-content">
        <span class="finding-id">F-07</span>
        <span class="finding-title-text">/donnees/import accessible à un Monteur — risque upload non contrôlé</span>
      </div>
      <span class="severity-badge med">MOYEN · CVSS 6.5</span>
    </div>
    <div class="finding-body">
      <div class="finding-meta">
        <span class="meta-pill">CWE-434</span>
        <span class="meta-pill">OWASP A04:2021</span>
        <span class="meta-pill">Route : /donnees/import</span>
      </div>
      <p>La page d'import de données retourne HTTP 200 avec 47 750 octets de contenu pour un compte Monteur. Si cette page expose un formulaire d'upload de fichiers (CSV, XLSX) sans validation stricte du type MIME et de la taille côté serveur, elle constitue un vecteur d'injection de données ou, dans le pire cas, d'upload de fichiers malveillants. Tests d'exploitation non encore effectués faute de compte Admin de référence.</p>
      <div class="reco-block">
        <div class="reco-label">Remédiation</div>
        <p>Restreindre <code>/donnees/import</code> au rôle <code>ADMIN</code> si l'import est une action administrative. Si accessible aux Éditeurs, valider strictement côté serveur : type MIME réel (pas seulement l'extension), taille maximale, et scanner le contenu avant ingestion en base.</p>
      </div>
    </div>
  </div>

  <div class="divider"></div>

  <!-- ATTACK SURFACE -->
  <div class="section-header">
    <span class="section-num">05</span>
    <h2>Surface d'attaque cartographiée</h2>
  </div>

  <table class="route-table">
    <thead>
      <tr>
        <th>Route</th>
        <th>HTTP</th>
        <th>Taille</th>
        <th>Données sensibles</th>
        <th>Risque</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>/equipe</code></td>
        <td>200</td>
        <td>80 KB</td>
        <td>Emails, téléphones, UUIDs membres</td>
        <td><span class="status-dot crit"></span>Critique</td>
      </tr>
      <tr>
        <td><code>/banque</code></td>
        <td>200</td>
        <td>254 KB</td>
        <td>Transactions financières, montants</td>
        <td><span class="status-dot crit"></span>Critique</td>
      </tr>
      <tr>
        <td><code>/parametres</code></td>
        <td>200</td>
        <td>88 KB</td>
        <td>Emails tous comptes dont Admin</td>
        <td><span class="status-dot crit"></span>Critique</td>
      </tr>
      <tr>
        <td><code>/clients</code></td>
        <td>200</td>
        <td>1,2 MB</td>
        <td>Emails clients, montants contrats</td>
        <td><span class="status-dot high"></span>Élevé</td>
      </tr>
      <tr>
        <td><code>/donnees/import</code></td>
        <td>200</td>
        <td>48 KB</td>
        <td>Upload non restreint (à confirmer)</td>
        <td><span class="status-dot med"></span>Moyen</td>
      </tr>
      <tr>
        <td><code>/projets</code></td>
        <td>200</td>
        <td>258 KB</td>
        <td>Données projets agence</td>
        <td><span class="status-dot med"></span>Moyen</td>
      </tr>
      <tr>
        <td><code>/da</code></td>
        <td>200</td>
        <td>791 KB</td>
        <td>Contenus DA/créatifs</td>
        <td><span class="status-dot med"></span>Moyen</td>
      </tr>
      <tr>
        <td><code>/frameio</code></td>
        <td>200</td>
        <td>944 KB</td>
        <td>Intégration Frame.io (tokens ?)</td>
        <td><span class="status-dot med"></span>À approfondir</td>
      </tr>
      <tr>
        <td><code>/analytics</code></td>
        <td>200</td>
        <td>62 KB</td>
        <td>Métriques agence</td>
        <td><span class="status-dot med"></span>Moyen</td>
      </tr>
      <tr>
        <td><code>/activite</code></td>
        <td>200</td>
        <td>201 KB</td>
        <td>Logs activité</td>
        <td><span class="status-dot med"></span>Moyen</td>
      </tr>
      <tr>
        <td><code>/academie</code></td>
        <td>200</td>
        <td>49 KB</td>
        <td>Contenus formation</td>
        <td><span class="status-dot ok"></span>Faible</td>
      </tr>
      <tr>
        <td><code>/playbooks</code></td>
        <td>200</td>
        <td>43 KB</td>
        <td>Procédures internes</td>
        <td><span class="status-dot ok"></span>Faible</td>
      </tr>
      <tr>
        <td><code>/recherche-ig</code></td>
        <td>200</td>
        <td>104 KB</td>
        <td>Recherche Instagram</td>
        <td><span class="status-dot ok"></span>Faible</td>
      </tr>
      <tr>
        <td><code>/api/projects</code></td>
        <td>200</td>
        <td>—</td>
        <td>Endpoint API interne</td>
        <td><span class="status-dot med"></span>À approfondir</td>
      </tr>
    </tbody>
  </table>

  <div class="divider"></div>

  <!-- SUPABASE -->
  <div class="section-header">
    <span class="section-num">06</span>
    <h2>Bilan Supabase / RLS</h2>
  </div>

  <table class="header-table">
    <thead>
      <tr>
        <th>Test</th>
        <th>Résultat</th>
        <th>Statut</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Accès anonyme à <code>profiles</code></td>
        <td>HTTP 200 — [] (vide, RLS bloque)</td>
        <td class="tag-ok">✓ OK</td>
      </tr>
      <tr>
        <td>Accès authentifié à <code>profiles</code></td>
        <td>HTTP 200 — 1 row (propre profil uniquement)</td>
        <td class="tag-ok">✓ OK</td>
      </tr>
      <tr>
        <td>PATCH profil d'un autre user</td>
        <td>HTTP 401 (clé anon manquante dans test)</td>
        <td class="tag-warn">⚠ À reconfirmer</td>
      </tr>
      <tr>
        <td>INSERT dans <code>projects</code></td>
        <td>HTTP 401 (clé anon manquante dans test)</td>
        <td class="tag-warn">⚠ À reconfirmer</td>
      </tr>
      <tr>
        <td>Accès root <code>/rest/v1/</code></td>
        <td>HTTP 401 — service_role requis</td>
        <td class="tag-ok">✓ Normal</td>
      </tr>
      <tr>
        <td>Tables sensibles (<code>users</code>, <code>invoices</code>...)</td>
        <td>HTTP 404 — absentes du schema public</td>
        <td class="tag-ok">✓ OK</td>
      </tr>
      <tr>
        <td>Rôle dans <code>user_metadata</code></td>
        <td>EDITOR dans champ modifiable par l'user</td>
        <td class="tag-fail">✗ À corriger</td>
      </tr>
    </tbody>
  </table>

  <div class="divider"></div>

  <!-- PLAN DE REMÉDIATION -->
  <div class="section-header">
    <span class="section-num">07</span>
    <h2>Plan de remédiation priorisé</h2>
  </div>

  <div class="scope-box">
    <h3>Immédiat — sous 48h</h3>
    <ul>
      <li><strong>F-01/02/03/04</strong> — Implémenter un middleware Next.js (<code>middleware.ts</code>) vérifiant le rôle pour toutes les routes sensibles</li>
      <li><strong>F-06</strong> — Migrer le claim de rôle de <code>user_metadata</code> vers <code>app_metadata</code> via Admin SDK</li>
      <li>Bloquer l'accès à <code>/banque</code>, <code>/equipe</code>, <code>/parametres</code> pour les rôles non-Admin immédiatement</li>
    </ul>
  </div>

  <div class="scope-box">
    <h3>Court terme — sous 2 semaines</h3>
    <ul>
      <li><strong>F-05</strong> — Remplacer <code>unsafe-inline</code> par des nonces CSP dans Next.js</li>
      <li><strong>F-05</strong> — Restreindre <code>Access-Control-Allow-Origin</code> au domaine de l'app</li>
      <li><strong>F-07</strong> — Restreindre <code>/donnees/import</code> et ajouter validation serveur des uploads</li>
      <li>Activer la RLS sur toutes les tables Supabase avec policies basées sur <code>app_metadata.role</code></li>
    </ul>
  </div>

  <div class="scope-box">
    <h3>Moyen terme — avant mise en production</h3>
    <ul>
      <li>Conduire un audit complet avec le compte Admin pour valider la séparation des rôles</li>
      <li>Tester les endpoints <code>/frameio</code> pour d'éventuels tokens d'intégration exposés</li>
      <li>Mettre en place un registre de traitement RGPD avec les accès par rôle documentés</li>
      <li>Implémenter des logs d'accès aux données sensibles (audit trail)</li>
      <li>Planifier un pentest complet post-remédiation</li>
    </ul>
  </div>

  <div class="divider"></div>

  <!-- CONFORMITE -->
  <div class="section-header">
    <span class="section-num">08</span>
    <h2>Conformité RGPD</h2>
  </div>

  <div class="callout">
    <strong>Risque RGPD identifié :</strong> L'accès non restreint aux données personnelles de membres de l'équipe (emails, téléphones) et de clients externes par un rôle Monteur constitue une violation potentielle du principe de minimisation des données (Art. 5 §1c) et de l'obligation de sécurité (Art. 32). En cas de fuite ou d'usage abusif, l'entreprise s'expose à une notification obligatoire à la CNIL sous 72h (Art. 33) et à une amende pouvant aller jusqu'à 4% du CA mondial.
  </div>

  <div class="scope-box">
    <h3>Articles RGPD concernés</h3>
    <ul>
      <li><strong>Art. 5 §1c</strong> — Minimisation des données : accès limité à ce qui est nécessaire à la finalité</li>
      <li><strong>Art. 5 §1f</strong> — Intégrité et confidentialité : mesures de sécurité appropriées</li>
      <li><strong>Art. 32</strong> — Sécurité du traitement : contrôle d'accès basé sur les rôles requis</li>
      <li><strong>Art. 33</strong> — Notification de violation : obligation sous 72h en cas d'incident</li>
    </ul>
  </div>

</div>

<!-- FOOTER -->
<div class="footer">
  <div>
    <div style="color:#fff;font-weight:500;margin-bottom:4px">Rapport Red Team — EWA App</div>
    <div>Confidentiel · Usage interne uniquement</div>
  </div>
  <div style="text-align:right">
    <div>19 juin 2026</div>
    <div style="margin-top:4px">7 findings · CVSS max 9.1</div>
  </div>
</div>

</body>
</html>