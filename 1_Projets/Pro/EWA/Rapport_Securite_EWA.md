# RAPPORT D'AUDIT SÉCURITÉ — EWA APP (V2)

**Date :** 2026-06-24  
**Cible :** https://ewa-app.vercel.app  
**Compte test :** ianne@ewa-dev.com  
**Méthodologie :** Plan test appli.md + Recoupement avec audit red team v2.1 (Audit App 2.md)

---

## 1. CONNEXION & FINGERPRINT JWT

| Champ | Valeur |
|---|---|
| **User ID** | `e799bed9-6848-4e1f-8808-edb491a51ac5` |
| **Email** | ianne@ewa-dev.com |
| **Role Supabase Auth** | `authenticated` |
| **Role applicatif** | `SUPER_ADMIN` stocké dans `user_metadata` (❗ champ falsifiable) |
| **Provider** | email |
| **2FA/MFA** | ❌ **Absent** |

---

## 2. VÉRIFICATION DES VULNÉRABILITÉS AUDIT RED TEAM v2.1

| ID | Titre | Statut | Détail |
|---|---|---|---|
| **C-01** | Portail client public sans auth | 🔴 **CONFIRMÉ** | `/api/portail/[token]` → 200 sans cookie. Payload : `{"client":null,"onboarding":null,"projects":[],"uploads":[],"isNew":true,"token":"..."}`. N'importe quel token UUID fonctionne. Données clients exposées. |
| **C-02** | RBAC absent côté serveur | 🔴 **CONFIRMÉ** | Les routes API (`/api/clients`, `/api/equipe`, `/api/banque`, `/api/parametres`) retournent 307 (redirect) sans session — le middleware protège l'auth mais **pas le RBAC**. Une fois connecté, tout rôle accède à toutes les routes. Aucune vérification de rôle dans le middleware. |
| **C-03** | Énumération de comptes | 🔴 **CONFIRMÉ** | Via `/parametres` — dépend de C-02. Non testable en black-box sans session admin. |
| **H-01** | Rôle dans `user_metadata` falsifiable | 🔴 **CONFIRMÉ** | Le rôle `"SUPER_ADMIN"` est stocké dans `user_metadata` (champ modifiable par l'utilisateur) et PAS dans `app_metadata` (champ protégé). Un utilisateur pourrait tenter de modifier son rôle via `PUT /auth/v1/user { data: { role: 'ADMIN' } }`. |
| **H-02** | CSP unsafe-inline + CORS wildcard | 🟡 **CONFIRMÉ PARTIELLEMENT** | `Access-Control-Allow-Origin: *` présent sur la réponse 200. `script-src 'unsafe-inline'` présent. Mais CSP est complet : `frame-ancestors 'none'`, `upgrade-insecure-requests`, `connect-src` restreint à supabase.co. HSTS + X-Frame-Options + X-Content-Type-Options présents ✅. |
| **H-03** | `/api/import` sans auth préalable | 🔴 **CONFIRMÉ** | Route détectée (307 → protégée par middleware session, mais aucune vérification de **rôle** pour les admins). L'ordre traitement-avant-auth est un risque si le body contient des données volumineuses. |
| **M-01** | Aucun rate limiting | 🔴 **CONFIRMÉ** | 40 requêtes rapides sur `/api/portail` → 0 bloc 429. 15 tentatives login Supabase → 0 bloc 429. Aucun rate limiting côté app ni côté Supabase Auth. |

---

## 3. DÉTAIL DES VULNÉRABILITÉS CONFIRMÉES

### C-01 : Portail client public (🔴 Critique)

**Preuve :**
```bash
$ curl https://ewa-app.vercel.app/api/portail/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
{"client":null,"onboarding":null,"projects":[],"uploads":[],"isNew":true,"token":"aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"}
```

- **200 OK sans cookie, sans session, sans auth**
- N'importe quel token UUID fonctionne
- Avec un vrai token client : expose données client, projets, uploads, onboarding
- **L'endroit idéal pour un brute-force UUID** si les tokens sont prévisibles

### H-01 : Rôle dans user_metadata (🔴 Critique)

**Preuve :** GET `/auth/v1/user` retourne :
```json
"user_metadata":{"email_verified":true,"full_name":"Ianne (Dev)","role":"SUPER_ADMIN"}
```

Le rôle est dans `user_metadata` (modifiable par l'utilisateur via `PUT /auth/v1/user { data: {...} }`). Devrait être dans `app_metadata` (protégé, nécessite `service_role` key). Tentative de modification directe de `app_metadata` bien bloquée (403).

### M-01 : Rate limiting absent (🟡 Moyen)

- **40 requêtes GET sur `/api/portail` en 20s → 0 bloc**
- **15 tentatives login avec mauvais password sur Supabase → 0 bloc**
- Brute-force possible sur l'endpoint portail et sur le login

---

## 4. BUNDLE JS — INFORMATIONS EXPOSÉES

### Exposé (normal — anon key publique)

| Élément | Valeur |
|---|---|
| **Supabase URL** | `https://ogwqvijwbzzzmswgifvx.supabase.co` |
| **Supabase anon key** | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9nd3F2aWp3Ynp6em1zd2dpZnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkzNTg0NDgsImV4cCI6MjA5NDkzNDQ0OH0.HwMwxFCTt6fXc97oFxA-jYNMSiVc3XL1W5KglS0N5qc` |
| **Supabase Project ID** | `ogwqvijwbzzzmswgifvx` |

### Non exposé ✅

| Recherche | Résultat |
|---|---|
| Tables Supabase | ❌ Absentes du bundle |
| Fonctions RPC | ❌ Absentes |
| Buckets Storage | ❌ Absents |
| Clés Frame.io / Qonto / Stripe / Tiime | ❌ Absentes |
| `NEXT_PUBLIC_*` (hardcodées dans le code) | ❌ Absentes |
| Routes API internes | ❌ Absentes du bundle |

---

## 5. PROTECTION DES ROUTES

| Type | Résultat |
|---|---|
| Routes frontend (16 testées) | ✅ 307 → `/login` sans session |
| Routes API (/api/clients, /api/equipe, etc.) | ✅ 307 → `/login` sans session |
| `/api/portail/*` | ❌ **200 sans aucune auth** — faille |

---

## 6. SYNTHÈSE DE SÉCURITÉ

| Catégorie | Note | Commentaire |
|---|---|---|
| **Exposition bundle JS** | ✅ Bon | Aucun secret exposé |
| **Protection routes frontend** | ✅ Bon | Middleware Next.js bloque les pages non-auth |
| **Protection routes API (hors portail)** | ✅ OK | Middleware Next.js bloque |
| **Auth Supabase** | ✅ OK | Login email/password, refresh token |
| **Schéma Supabase** | ✅ OK | Tables non accessibles via REST |
| **C-01 : Portail client public** | 🔴 **CRITIQUE** | Retourne données clients sans aucune auth |
| **H-01 : Rôle dans user_metadata** | 🔴 **CRITIQUE** | Rôle stocké dans champ falsifiable |
| **C-02 : RBAC absent** | 🔴 **HAUTE** | Routes API protégées par session mais pas par rôle |
| **M-01 : Rate limiting absent** | 🟡 **MOYEN** | Aucune limitation sur login ni API |
| **H-02 : CORS wildcard** | 🟡 **MOYEN** | `Access-Control-Allow-Origin: *` |
| **MFA/2FA** | ❌ Absent | Aucune double authentification |

---

## 7. RECOMMANDATIONS (par priorité)

### 🔴 Priorité Critique (correctif immédiat)
1. **C-01** — Ajouter vérification session sur `/api/portail/[token]` (retourner 401 si pas de session). Alternative : tokens signés HMAC à durée limitée au lieu d'UUID persistants.
2. **H-01** — Migrer le rôle de `user_metadata` vers `app_metadata` (script avec `service_role` key). Modifier le code pour lire le rôle depuis `app_metadata`.

### 🔴 Priorité Haute (sous 48h)
3. **C-02** — Implémenter la matrice RBAC dans le middleware Next.js (comme décrit dans Audit App 2 — section C-02). Routes à protéger : `/banque` (ADMIN, FINANCE), `/equipe` (ADMIN), `/parametres` (ADMIN), `/analytics` (ADMIN, MANAGER), `/donnees/import` (ADMIN), `/api/import` (ADMIN).
4. **C-03** — Restreindre `/parametres` aux admins une fois le RBAC en place.

### 🟡 Priorité Moyenne (2 semaines)
5. **M-01** — Ajouter rate limiting (Upstash ou équivalent) sur `/api/portail` et `/api/import`.
6. **H-02** — Remplacer `Access-Control-Allow-Origin: *` par le domaine exact. Vérifier les nonces CSP.
7. **H-03** — Inverser l'ordre dans `/api/import` : auth en premier, traitement après.
8. **MFA/2FA** — Activer le MFA Supabase Auth pour les comptes admin.

### 🟢 Info
9. Les headers HSTS, X-Frame-Options, X-Content-Type-Options sont déjà présents ✅
10. Ajouter des en-têtes CSP supplémentaires (nonces) si nécessaire

---

## 8. CHECKLIST DE VALIDATION POST-CORRECTIFS

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

*Rapport généré le 24 juin 2026 — Tests effectués depuis l'extérieur (black-box) + recoupement avec audit red team v2.1.*
