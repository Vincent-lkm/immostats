# 🌐 Configuration immobilier.guide avec Cloudflare

## 1. Acheter le domaine

### Option A: Via Cloudflare (Recommandé)
- Prix: ~12€/an pour .guide
- DNS automatique
- Pas de frais de transfert

### Option B: Autre registrar
- Namecheap: ~25€/an
- OVH: ~30€/an
- Puis transférer vers Cloudflare

## 2. Setup DNS dans Cloudflare

```
Type    Name              Value                   Proxy
A       immobilier.guide  192.0.2.1              ✅ (Orange cloud)
AAAA    immobilier.guide  100::                  ✅ (Orange cloud)
CNAME   www              immobilier.guide        ✅ (Orange cloud)
```

**Note:** Les IPs sont fictives, Cloudflare Workers route automatiquement.

## 3. Déployer le Worker

```bash
# 1. Créer KV namespace
wrangler kv:namespace create "DATA_KV"

# 2. Copier l'ID retourné dans wrangler-simple.toml

# 3. Deploy
wrangler deploy --config wrangler-simple.toml

# 4. Tester
curl https://immobilier.guide
```

## 4. SSL/TLS Settings

Dans Cloudflare Dashboard:
- SSL/TLS → Overview → **Full (strict)**
- SSL/TLS → Edge Certificates → **Always Use HTTPS** ✅
- SSL/TLS → Edge Certificates → **Automatic HTTPS Rewrites** ✅

## 5. Performance

Dans Cloudflare Dashboard:
- Speed → Optimization → **Auto Minify** (JS, CSS, HTML) ✅
- Speed → Optimization → **Brotli** ✅
- Caching → Configuration → **Browser Cache TTL**: 4 hours

## 6. Analytics

Cloudflare Analytics gratuit inclus:
- Visiteurs uniques
- Requêtes
- Bande passante
- Top pages
- Géolocalisation

## URLs Finales

```
https://immobilier.guide
https://www.immobilier.guide
https://immobilier.guide/ville/75008/paris-8
https://immobilier.guide/api/search?q=lyon
```

## Coûts Estimés

```yaml
Domaine: 12€/an
Cloudflare Workers (Paid):
  - $5/mois (10M requêtes incluses)
  - KV: $0.50/million lectures

Total: ~72€/an + usage
```

Pour 1M visiteurs/mois: ~$10/mois