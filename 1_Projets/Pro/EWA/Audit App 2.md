cat > /mnt/user-data/outputs/ewa_correctifs.md << 'EOF'
# EWA App — Guide de correctifs sécurité
> Version 1.0 · 24 juin 2026 · Post-audit red team v2.1

---

## Priorités

| ID | Fichier cible | Effort | Délai |
|----|--------------|--------|-------|
| C-01 | `app/api/portail/[token]/route.ts` | 5 min | **Aujourd'hui** |
| C-02 | `middleware.ts` | 2h | **48h** |
| C-03 | Dépend de C-02 | — | **48h** |
| H-01 | Script migration + `middleware.ts` | 2h | 2 sem |
| H-02 | `next.config.ts` | 1h | 2 sem |
| H-03 | `app/api/import/route.ts` | 15 min | 2 sem |
| M-01 | `middleware.ts` | 1h | 2 sem |

---

## C-01 — Portail client public sans auth

**Fichier :** `app/api/portail/[token]/route.ts`

**Problème :** L'endpoint retourne les données du client sans vérifier la session.

```typescript
// ❌ AVANT — aucune vérification
export async function GET(
  request: Request,
  { params }: { params: { token: string } }
) {
  const client = await getClientByPortalToken(params.token);
  return Response.json({ client });
}
```

```typescript
// ✅ APRÈS — vérification session en premier
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function GET(
  request: Request,
  { params }: { params: { token: string } }
) {
  // 1. Vérifier la session AVANT tout traitement
  const cookieStore = cookies();
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    { cookies: { get: (name) => cookieStore.get(name)?.value } }
  );

  const { data: { session } } = await supabase.auth.getSession();

  if (!session) {
    return Response.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // 2. Seulement après : récupérer les données
  const client = await getClientByPortalToken(params.token);
  return Response.json({ client });
}
```

> **Alternative recommandée à terme :** Générer des tokens signés HMAC à durée limitée plutôt que des UUID persistants.
> ```typescript
> // Génération d'un lien portail expirant (7 jours)
> import { createHmac } from 'crypto';
> 
> function generatePortalLink(clientId: string): string {
>   const exp = Math.floor(Date.now() / 1000) + 7 * 24 * 3600;
>   const sig = createHmac('sha256', process.env.PORTAL_SECRET!)
>     .update(`${clientId}:${exp}`)
>     .digest('hex');
>   return `/portail/${clientId}?exp=${exp}&sig=${sig}`;
> }
> 
> // Vérification dans le handler
> function verifyPortalToken(clientId: string, exp: string, sig: string): boolean {
>   if (Date.now() / 1000 > Number(exp)) return false; // expiré
>   const expected = createHmac('sha256', process.env.PORTAL_SECRET!)
>     .update(`${clientId}:${exp}`)
>     .digest('hex');
>   return sig === expected;
> }
> ```

---

## C-02 — RBAC absent côté serveur (routes sensibles)

**Fichier :** `middleware.ts` (à la racine du projet)

**Problème :** Toutes les routes sont accessibles à n'importe quel rôle authentifié. Le RBAC est uniquement côté client.

```typescript
// ✅ middleware.ts — Matrice de droits par route
import { createServerClient } from '@supabase/ssr';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Matrice : route → rôles autorisés
const ROUTE_PERMISSIONS: Record<string, string[]> = {
  '/banque':         ['ADMIN', 'FINANCE'],
  '/equipe':         ['ADMIN'],
  '/parametres':     ['ADMIN'],
  '/analytics':      ['ADMIN', 'MANAGER'],
  '/donnees/import': ['ADMIN'],
  '/clients':        ['ADMIN', 'MANAGER', 'COMMERCIAL'],
  // Routes accessibles à tous les rôles authentifiés :
  // /projets, /da, /academie, /playbooks, /frameio, /activite, /recherche-ig
};

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const response = NextResponse.next();

  // 1. Routes publiques — laisser passer
  if (pathname.startsWith('/login') || pathname === '/') {
    return response;
  }

  // 2. Initialiser Supabase côté serveur
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get: (name) => request.cookies.get(name)?.value,
        set: (name, value, options) => {
          response.cookies.set({ name, value, ...options });
        },
        remove: (name, options) => {
          response.cookies.set({ name, value: '', ...options });
        },
      },
    }
  );

  // 3. Vérifier la session
  const { data: { session } } = await supabase.auth.getSession();

  if (!session) {
    const loginUrl = request.nextUrl.clone();
    loginUrl.pathname = '/login';
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // 4. Lire le rôle depuis app_metadata (JAMAIS user_metadata)
  const role = session.user.app_metadata?.role as string ?? 'EDITOR';

  // 5. Vérifier les permissions pour les routes protégées
  for (const [route, allowedRoles] of Object.entries(ROUTE_PERMISSIONS)) {
    if (pathname.startsWith(route)) {
      if (!allowedRoles.includes(role)) {
        // Rôle insuffisant → 403
        return NextResponse.json(
          { error: 'Forbidden', required: allowedRoles, current: role },
          { status: 403 }
        );
      }
      break;
    }
  }

  // 6. Protéger aussi les API routes portail
  if (pathname.startsWith('/api/portail')) {
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
  }

  return response;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|login).*)',
  ],
};
```

---

## C-03 — Énumération de comptes via /parametres

Dépend entièrement de **C-02**. Une fois la matrice RBAC en place, ajouter la ligne :

```typescript
// Dans ROUTE_PERMISSIONS de middleware.ts :
const ROUTE_PERMISSIONS: Record<string, string[]> = {
  '/banque':         ['ADMIN', 'FINANCE'],
  '/equipe':         ['ADMIN'],
  '/parametres':     ['ADMIN'],   // ← déjà inclus ci-dessus
  // ...
};
```

Aucun autre changement nécessaire.

---

## H-01 — Rôle dans user_metadata (falsifiable)

**Problème :** Le rôle est dans `user_metadata`, modifiable par l'utilisateur lui-même.

### Étape 1 — Script de migration (à exécuter une fois)

```typescript
// scripts/migrate-roles.ts
// Exécuter avec : npx ts-node scripts/migrate-roles.ts

import { createClient } from '@supabase/supabase-js';

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!, // clé service_role (jamais côté client)
);

async function migrateRoles() {
  // Récupérer tous les users
  const { data: { users }, error } = await supabaseAdmin.auth.admin.listUsers();
  if (error) throw error;

  for (const user of users) {
    // Lire le rôle depuis user_metadata (ancienne position)
    const role = user.user_metadata?.role ?? 'EDITOR';

    // Écrire dans app_metadata (position sécurisée)
    await supabaseAdmin.auth.admin.updateUserById(user.id, {
      app_metadata: { role }
    });

    console.log(`✓ ${user.email} → app_metadata.role = ${role}`);
  }
}

migrateRoles();
```

### Étape 2 — Lire le rôle depuis app_metadata dans le code

```typescript
// ❌ AVANT — champ falsifiable
const role = session.user.user_metadata?.role;

// ✅ APRÈS — champ signé côté serveur uniquement
const role = session.user.app_metadata?.role;
```

### Étape 3 — Activer les custom JWT claims Supabase (optionnel mais recommandé)

```sql
-- Dans Supabase Dashboard → SQL Editor
-- Ajoute le rôle directement dans le JWT token

create or replace function public.custom_access_token_hook(event jsonb)
returns jsonb language plpgsql as $$
declare
  claims jsonb;
  user_role text;
begin
  select raw_app_meta_data->>'role'
  into user_role
  from auth.users
  where id = (event->>'user_id')::uuid;

  claims := event->'claims';
  claims := jsonb_set(claims, '{app_role}', to_jsonb(coalesce(user_role, 'EDITOR')));

  return jsonb_set(event, '{claims}', claims);
end;
$$;

grant execute on function public.custom_access_token_hook to supabase_auth_admin;
```

---

## H-02 — CSP unsafe-inline + CORS wildcard

**Fichier :** `next.config.ts`

```typescript
// ✅ next.config.ts
import type { NextConfig } from 'next';
import crypto from 'crypto';

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          // CORS — restreindre au domaine de l'app
          {
            key: 'Access-Control-Allow-Origin',
            value: 'https://ewa-app.vercel.app',  // ← remplacer * par le domaine exact
          },
          // CSP — nonces à la place de unsafe-inline
          // Note : Next.js 13.4+ gère les nonces nativement
          // Voir : https://nextjs.org/docs/app/building-your-application/configuring/content-security-policy
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              "script-src 'self' 'nonce-{nonce}'",  // nonce généré par requête
              "style-src 'self' 'unsafe-inline'",   // styles inline tolérés
              "img-src 'self' data: https:",
              "connect-src 'self' https://*.supabase.co https://api.frame.io",
              "frame-ancestors 'none'",
              "upgrade-insecure-requests",
            ].join('; '),
          },
        ],
      },
    ];
  },
};

export default nextConfig;
```

> **Pour les nonces CSP avec Next.js App Router :**
> Voir la documentation officielle : https://nextjs.org/docs/app/building-your-application/configuring/content-security-policy

---

## H-03 — /api/import sans vérification auth préalable

**Fichier :** `app/api/import/route.ts`

```typescript
// ❌ AVANT — traitement avant vérification auth
export async function POST(request: Request) {
  const body = await request.formData(); // ← traitement avant auth
  if (!body.get('file')) {
    return Response.json({ error: 'Body invalide' }, { status: 400 });
  }
  // ...traitement...
}
```

```typescript
// ✅ APRÈS — auth EN PREMIER, puis traitement
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function POST(request: Request) {
  // 1. Auth en PREMIER — avant de toucher au body
  const cookieStore = cookies();
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    { cookies: { get: (name) => cookieStore.get(name)?.value } }
  );

  const { data: { session } } = await supabase.auth.getSession();
  if (!session) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // 2. Vérifier le rôle (import réservé aux admins)
  const role = session.user.app_metadata?.role;
  if (role !== 'ADMIN') {
    return Response.json({ error: 'Forbidden' }, { status: 403 });
  }

  // 3. Seulement après : lire et valider le body
  const body = await request.formData();
  const file = body.get('file') as File | null;

  if (!file) {
    return Response.json({ error: 'Fichier manquant' }, { status: 400 });
  }

  // 4. Valider le type MIME réel (pas l'extension)
  const allowedTypes = ['text/csv', 'application/vnd.ms-excel'];
  if (!allowedTypes.includes(file.type)) {
    return Response.json({ error: 'Type de fichier non autorisé' }, { status: 400 });
  }

  // 5. Limiter la taille (5 MB max)
  const MAX_SIZE = 5 * 1024 * 1024;
  if (file.size > MAX_SIZE) {
    return Response.json({ error: 'Fichier trop volumineux (max 5 MB)' }, { status: 400 });
  }

  // 6. Scanner les formules CSV dangereuses
  const text = await file.text();
  const dangerousPatterns = /^[=+\-@\t\r]/m;
  const lines = text.split('\n').slice(1); // ignorer l'en-tête
  for (const line of lines) {
    if (dangerousPatterns.test(line)) {
      return Response.json(
        { error: 'Contenu CSV invalide (formule détectée)' },
        { status: 400 }
      );
    }
  }

  // 7. Traitement normal
  // ...
}
```

---

## M-01 — Rate limiting

**Fichier :** `middleware.ts` (ajout dans le middleware existant)

### Installation

```bash
npm install @upstash/ratelimit @upstash/redis
```

```typescript
// Ajouter en haut de middleware.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(30, '1 m'), // 30 req/min par IP
});

// Dans la fonction middleware, avant les vérifications RBAC :
const ip = request.ip ?? request.headers.get('x-forwarded-for') ?? '127.0.0.1';

// Appliquer le rate limit sur les endpoints sensibles
if (
  pathname.startsWith('/api/portail') ||
  pathname.startsWith('/api/import')
) {
  const { success, limit, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: 'Too Many Requests' },
      {
        status: 429,
        headers: {
          'X-RateLimit-Limit': String(limit),
          'X-RateLimit-Remaining': String(remaining),
          'Retry-After': '60',
        },
      }
    );
  }
}
```

> **Variables d'environnement Upstash à ajouter dans Vercel :**
> ```
> UPSTASH_REDIS_REST_URL=...
> UPSTASH_REDIS_REST_TOKEN=...
> ```

---

## Checklist de validation post-correctifs

```
□ C-01 — curl /api/portail/{token} sans cookie → 401
□ C-01 — curl /api/portail/{token} avec cookie valide → 200
□ C-02 — Compte EDITOR → /banque → 403
□ C-02 — Compte EDITOR → /equipe → 403
□ C-02 — Compte EDITOR → /parametres → 403
□ C-02 — Compte ADMIN → /banque → 200
□ C-03 — Compte EDITOR → /parametres → 403 (emails admin non visibles)
□ H-01 — PUT /auth/v1/user { data: { role: 'ADMIN' } } → pas d'effet sur les autorisations
□ H-02 — curl -I / → Access-Control-Allow-Origin ≠ *
□ H-03 — POST /api/import sans cookie → 401 (pas 400)
□ M-01 — 31 requêtes rapides sur /api/portail → 429 sur la 31e
```

---

## Variables d'environnement à ajouter

```bash
# .env.local (ne jamais committer)
SUPABASE_SERVICE_ROLE_KEY=...   # pour le script de migration H-01
PORTAL_SECRET=...               # secret HMAC pour les tokens portail (C-01 option 2)
UPSTASH_REDIS_REST_URL=...      # rate limiting M-01
UPSTASH_REDIS_REST_TOKEN=...    # rate limiting M-01
```

---

*Guide généré suite à l'audit red team EWA App — 24 juin 2026*
EOF
echo "OK"
Sortie

OK
Terminé
