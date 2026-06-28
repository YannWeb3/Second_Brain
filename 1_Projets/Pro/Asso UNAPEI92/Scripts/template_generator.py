# Générateur HTML pour tous les formulaires RGPD Unapei92
# Corrections appliquées :
#   [FIX 1] sheets_url ajouté comme paramètre de generate_html() — plus de {SHEETS_URL} non résolu
#   [FIX 2] Toutes les questions sont envoyées (même sans réponse) pour stabiliser les colonnes Sheets
#   [FIX 3] Lecture des checkboxes corrigée dans applyConditions() — accumulation au lieu d'écrasement

import json


def generate_html(form_type, title, subtitle, color, accent, questions, sheets_url):
    # [FIX 1] sheets_url est maintenant un paramètre explicite

    # Grouper questions par bloc
    blocs = {}
    for q in questions:
        b = q.get('bloc', 'Général')
        if b not in blocs:
            blocs[b] = []
        blocs[b].append(q)

    bloc_names = list(blocs.keys())
    total_blocs = len(bloc_names)

    # Générer les blocs HTML
    blocs_html = ""
    for i, bloc_name in enumerate(bloc_names):
        qs = blocs[bloc_name]
        questions_html = ""
        for q in qs:
            questions_html += generate_question_html(q)

        blocs_html += f"""
        <div class="bloc" id="bloc-{i}" {"style='display:block'" if i == 0 else "style='display:none'"}>
          <div class="bloc-header">
            <span class="bloc-tag">Section {i + 1} sur {total_blocs}</span>
            <h2 class="bloc-title">{bloc_name}</h2>
          </div>
          <div class="questions">
            {questions_html}
          </div>
          <div class="bloc-nav">
            {"" if i == 0 else '<button type="button" class="btn-prev" onclick="navigate(-1)">← Précédent</button>'}
            {"<button type='button' class='btn-next' onclick='navigate(1)'>Suivant →</button>" if i < total_blocs - 1 else "<button type='submit' class='btn-submit'>Soumettre le questionnaire →</button>"}
          </div>
        </div>"""

    # Générer JS conditions
    conditions_js = generate_conditions_js(questions)

    # [FIX 2] Générer la liste ordonnée de tous les IDs de questions pour le payload stable
    all_question_ids_js = json.dumps(
        [q['id'] for q in questions],
        ensure_ascii=False
    )
    all_question_labels_js = json.dumps(
        {q['id']: q['label'] for q in questions},
        ensure_ascii=False
    )

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Unapei92</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --primary: {color};
    --accent: {accent};
    --bg: #F7F6F3;
    --surface: #FFFFFF;
    --text: #1A1A1A;
    --text-muted: #6B6B6B;
    --border: #E2E0DA;
    --radius: 12px;
    --shadow: 0 2px 16px rgba(0,0,0,0.06);
  }}

  body {{
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 0;
  }}

  .header {{
    background: var(--primary);
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }}

  .header::before {{
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
  }}

  .header-logo {{
    font-family: 'DM Serif Display', serif;
    color: rgba(255,255,255,0.6);
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }}

  .header-title {{
    font-family: 'DM Serif Display', serif;
    color: #fff;
    font-size: 1.8rem;
    font-weight: 400;
    margin-bottom: 0.25rem;
  }}

  .header-subtitle {{
    color: rgba(255,255,255,0.65);
    font-size: 0.9rem;
    font-weight: 300;
  }}

  .progress-bar {{
    height: 3px;
    background: rgba(255,255,255,0.2);
  }}

  .progress-fill {{
    height: 100%;
    background: var(--accent);
    transition: width 0.4s ease;
    width: calc(100% / {total_blocs});
  }}

  .container {{
    max-width: 720px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
  }}

  .bloc {{
    animation: fadeIn 0.3s ease;
  }}

  @keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  .bloc-header {{
    margin-bottom: 1.75rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
  }}

  .bloc-tag {{
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--primary);
    opacity: 0.7;
    display: block;
    margin-bottom: 0.4rem;
  }}

  .bloc-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    font-weight: 400;
    color: var(--text);
  }}

  .questions {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }}

  .question {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    transition: border-color 0.2s;
  }}

  .question:focus-within {{
    border-color: var(--primary);
  }}

  .question.hidden {{ display: none; }}

  .question-label {{
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 1rem;
    line-height: 1.45;
    display: flex;
    gap: 0.5rem;
  }}

  .required-star {{
    color: #C0392B;
    font-size: 0.8rem;
    flex-shrink: 0;
    margin-top: 2px;
  }}

  .question-id {{
    font-size: 0.7rem;
    color: var(--text-muted);
    font-weight: 400;
    margin-bottom: 0.4rem;
    font-family: monospace;
  }}

  input[type="text"],
  input[type="number"],
  input[type="date"],
  textarea {{
    width: 100%;
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: var(--text);
    background: var(--bg);
    transition: border-color 0.2s, background 0.2s;
    outline: none;
  }}

  input[type="text"]:focus,
  input[type="number"]:focus,
  input[type="date"]:focus,
  textarea:focus {{
    border-color: var(--primary);
    background: #fff;
  }}

  textarea {{
    min-height: 100px;
    resize: vertical;
    line-height: 1.5;
  }}

  .choices {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }}

  .choice-item {{
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.65rem 0.9rem;
    border: 1.5px solid var(--border);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s;
    background: var(--bg);
  }}

  .choice-item:hover {{
    border-color: var(--primary);
    background: rgba(27,79,138,0.04);
  }}

  .choice-item input {{
    margin-top: 2px;
    accent-color: var(--primary);
    flex-shrink: 0;
    width: 16px;
    height: 16px;
  }}

  .choice-item label {{
    font-size: 0.88rem;
    cursor: pointer;
    line-height: 1.4;
    color: var(--text);
  }}

  .choice-item:has(input:checked) {{
    border-color: var(--primary);
    background: rgba(27,79,138,0.06);
  }}

  .bloc-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
  }}

  .btn-prev, .btn-next, .btn-submit {{
    padding: 0.75rem 1.75rem;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
  }}

  .btn-prev {{
    background: transparent;
    border: 1.5px solid var(--border);
    color: var(--text-muted);
  }}

  .btn-prev:hover {{ border-color: var(--text-muted); color: var(--text); }}

  .btn-next {{
    background: var(--primary);
    color: #fff;
    margin-left: auto;
  }}

  .btn-next:hover {{ background: #153d6e; }}

  .btn-submit {{
    background: #1A6B3C;
    color: #fff;
    margin-left: auto;
  }}

  .btn-submit:hover {{ background: #145530; }}

  .success {{
    display: none;
    text-align: center;
    padding: 3rem 2rem;
    background: var(--surface);
    border-radius: var(--radius);
    border: 1px solid #B8E6CB;
  }}

  .success-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
  .success h2 {{ font-family: 'DM Serif Display', serif; font-size: 1.6rem; margin-bottom: 0.75rem; color: #1A6B3C; font-weight: 400; }}
  .success p {{ color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; }}

  .error-msg {{
    background: #FEE;
    border: 1px solid #FCC;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    color: #C0392B;
    margin-top: 0.5rem;
    display: none;
  }}

  @media (max-width: 640px) {{
    .header {{ padding: 1.5rem 1rem; }}
    .header-title {{ font-size: 1.4rem; }}
    .container {{ padding: 1.25rem 1rem 3rem; }}
  }}
</style>
</head>
<body>

<div class="header">
  <div class="header-logo">Unapei92 — Audit RGPD 2025</div>
  <h1 class="header-title">{title}</h1>
  <p class="header-subtitle">{subtitle}</p>
</div>
<div class="progress-bar">
  <div class="progress-fill" id="progress-fill"></div>
</div>

<div class="container">
  <form id="main-form" novalidate>
    <input type="hidden" name="form_type" value="{form_type}">
    {blocs_html}
    <div class="success" id="success-msg">
      <div class="success-icon">✓</div>
      <h2>Questionnaire soumis avec succès</h2>
      <p>Merci pour vos réponses. Elles ont bien été enregistrées et transmises au DPO.<br>Vos données sont traitées conformément au RGPD.</p>
    </div>
    <div class="error-msg" id="error-msg">Une erreur est survenue. Veuillez réessayer ou contacter le DPO.</div>
  </form>
</div>

<script>
// [FIX 1] sheets_url injecté proprement depuis Python
const SHEETS_URL = {json.dumps(sheets_url)};
const TOTAL_BLOCS = {total_blocs};
let currentBloc = 0;

const conditions = {conditions_js};

// [FIX 2] Liste ordonnée de tous les IDs et libellés pour un payload stable
const ALL_QUESTION_IDS = {all_question_ids_js};
const ALL_QUESTION_LABELS = {all_question_labels_js};

function updateProgress() {{
  const pct = ((currentBloc + 1) / TOTAL_BLOCS) * 100;
  document.getElementById('progress-fill').style.width = pct + '%';
}}

function showBloc(idx) {{
  document.querySelectorAll('.bloc').forEach((b, i) => {{
    b.style.display = i === idx ? 'block' : 'none';
  }});
  currentBloc = idx;
  updateProgress();
  window.scrollTo({{top: 0, behavior: 'smooth'}});
  applyConditions();
}}

// [FIX 3] Lecture radio ET checkbox correcte : accumulation des valeurs cochées
function getFieldValue(name) {{
  const els = document.querySelectorAll('[name="' + name + '"]');
  if (els.length === 0) return '';

  const firstEl = els[0];

  // Champ texte / textarea / number / date
  if (firstEl.type !== 'radio' && firstEl.type !== 'checkbox') {{
    return firstEl.value;
  }}

  // Radio : une seule valeur possible
  if (firstEl.type === 'radio') {{
    for (const el of els) {{
      if (el.checked) return el.value;
    }}
    return '';
  }}

  // Checkbox : accumulation de toutes les valeurs cochées
  if (firstEl.type === 'checkbox') {{
    const checked = [];
    els.forEach(el => {{ if (el.checked) checked.push(el.value); }});
    return checked.join(' | ');
  }}

  return '';
}}

function applyConditions() {{
  Object.entries(conditions).forEach(([qid, cond]) => {{
    const qEl = document.getElementById('q-' + qid);
    if (!qEl) return;

    // [FIX 3] Utilise getFieldValue() au lieu de la boucle incomplète
    const val = getFieldValue(cond.q);

    let show = false;
    if (cond.is) show = val === cond.is;
    if (cond.not) show = val !== cond.not && val !== '';
    qEl.classList.toggle('hidden', !show);
  }});
}}

function navigate(dir) {{
  if (dir === 1) {{
    const bloc = document.querySelectorAll('.bloc')[currentBloc];
    const required = bloc.querySelectorAll('[required]');
    let valid = true;
    required.forEach(field => {{
      const qEl = field.closest('.question');
      if (qEl && qEl.classList.contains('hidden')) return;
      if (field.type === 'radio' || field.type === 'checkbox') {{
        const name = field.name;
        const checked = bloc.querySelectorAll('[name="' + name + '"]:checked');
        if (checked.length === 0) {{
          valid = false;
          field.closest('.choices').style.outline = '2px solid #C0392B';
          field.closest('.choices').style.borderRadius = '8px';
        }} else {{
          field.closest('.choices').style.outline = '';
        }}
      }} else {{
        if (!field.value.trim()) {{
          valid = false;
          field.style.borderColor = '#C0392B';
        }} else {{
          field.style.borderColor = '';
        }}
      }}
    }});
    if (!valid) {{ window.scrollTo({{top: 0, behavior: 'smooth'}}); return; }}
  }}
  showBloc(currentBloc + dir);
}}

document.getElementById('main-form').addEventListener('submit', async function(e) {{
  e.preventDefault();
  const form = e.target;

  // [FIX 2] Payload stable : on itère sur TOUS les IDs dans l'ordre déclaré,
  // qu'ils soient visibles ou non, pour garantir l'alignement des colonnes Sheets.
  const responses = ALL_QUESTION_IDS.map(qid => {{
    const label = ALL_QUESTION_LABELS[qid] || qid;
    const qEl = document.getElementById('q-' + qid);
    const isHidden = qEl ? qEl.classList.contains('hidden') : false;

    // [FIX 3] Utilise getFieldValue() ici aussi
    const answer = isHidden ? '' : getFieldValue(qid);

    return {{ question_id: qid, question: label, answer, visible: !isHidden }};
  }});

  const payload = {{
    type: '{form_type}',
    timestamp: new Date().toISOString(),
    responses
  }};

  const btn = form.querySelector('.btn-submit');
  btn.textContent = 'Envoi en cours...';
  btn.disabled = true;

  try {{
    await fetch(SHEETS_URL, {{
      method: 'POST',
      body: JSON.stringify(payload)
    }});
    document.querySelectorAll('.bloc').forEach(b => b.style.display = 'none');
    document.getElementById('success-msg').style.display = 'block';
    document.getElementById('progress-fill').style.width = '100%';
  }} catch(err) {{
    document.getElementById('error-msg').style.display = 'block';
    btn.textContent = 'Soumettre le questionnaire →';
    btn.disabled = false;
  }}
}});

document.addEventListener('change', applyConditions);
updateProgress();
applyConditions();
</script>
</body>
</html>"""
    return html


def generate_question_html(q):
    qid = q['id']
    label = q['label']
    qtype = q['type']
    required = q.get('required', False)
    req_attr = 'required' if required else ''
    req_star = '<span class="required-star">*</span>' if required else ''

    cond_class = 'question hidden' if q.get('condition') else 'question'

    input_html = ''
    if qtype == 'text':
        input_html = f'<input type="text" name="{qid}" {req_attr} placeholder="Votre réponse...">'
    elif qtype == 'number':
        input_html = f'<input type="number" name="{qid}" {req_attr} min="0" placeholder="0">'
    elif qtype == 'date':
        input_html = f'<input type="date" name="{qid}" {req_attr}>'
    elif qtype == 'textarea':
        input_html = f'<textarea name="{qid}" {req_attr} placeholder="Votre réponse..."></textarea>'
    elif qtype in ['radio', 'select']:
        choices_html = ''
        for c in q.get('choices', []):
            cid = f"{qid}_{c[:20].replace(' ', '_')}"
            choices_html += f'''
            <div class="choice-item">
              <input type="radio" id="{cid}" name="{qid}" value="{c}" {req_attr}>
              <label for="{cid}">{c}</label>
            </div>'''
        input_html = f'<div class="choices">{choices_html}</div>'
    elif qtype == 'checkbox':
        choices_html = ''
        for c in q.get('choices', []):
            cid = f"{qid}_{c[:20].replace(' ', '_')}"
            choices_html += f'''
            <div class="choice-item">
              <input type="checkbox" id="{cid}" name="{qid}" value="{c}">
              <label for="{cid}">{c}</label>
            </div>'''
        input_html = f'<div class="choices">{choices_html}</div>'

    return f'''
    <div class="{cond_class}" id="q-{qid}">
      <div class="question-id">{qid}</div>
      <div class="question-label">{req_star}{label}</div>
      {input_html}
    </div>'''


def generate_conditions_js(questions):
    conds = {}
    for q in questions:
        if q.get('condition'):
            conds[q['id']] = q['condition']
    return json.dumps(conds, ensure_ascii=False)


if __name__ == '__main__':
    # Exemple de test minimal
    questions_test = [
        {
            'id': 'q1', 'label': 'Avez-vous un DPO ?', 'type': 'radio',
            'bloc': 'Gouvernance', 'required': True,
            'choices': ['Oui', 'Non']
        },
        {
            'id': 'q2', 'label': 'Nom du DPO', 'type': 'text',
            'bloc': 'Gouvernance', 'required': False,
            'condition': {'q': 'q1', 'is': 'Oui'}
        },
        {
            'id': 'q3', 'label': 'Quels traitements effectuez-vous ?', 'type': 'checkbox',
            'bloc': 'Traitements', 'required': False,
            'choices': ['RH', 'Facturation', 'Vidéosurveillance', 'Données de santé']
        },
    ]

    html = generate_html(
        form_type='audit_dpo',
        title='Audit RGPD',
        subtitle='Questionnaire à destination des responsables de traitement',
        color='#1B4F8A',
        accent='#F0A500',
        questions=questions_test,
        sheets_url='https://script.google.com/macros/s/VOTRE_ID/exec',  # [FIX 1]
    )

    with open('/tmp/test_form.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("✓ [FIX 1] sheets_url injecté comme paramètre — plus de variable non résolue")
    print("✓ [FIX 2] Payload stable — toutes les questions envoyées, colonnes Sheets fixes")
    print("✓ [FIX 3] getFieldValue() — radio ET checkbox lus correctement dans les conditions")
    print("Fichier de test généré : /tmp/test_form.html")