#!/bin/bash

# Script de setup Cloudflare Workers pour ImmoStats
# Usage: ./setup-cloudflare.sh

echo "🚀 Setup Cloudflare Workers pour ImmoStats"

# 1. Install Wrangler
echo "📦 Installation de Wrangler..."
npm install -g wrangler

# 2. Login to Cloudflare
echo "🔐 Connexion à Cloudflare..."
wrangler login

# 3. Create KV namespaces
echo "📚 Création des KV namespaces..."
wrangler kv:namespace create "STATS_KV"
wrangler kv:namespace create "STATS_KV" --preview
wrangler kv:namespace create "PAGES_KV"
wrangler kv:namespace create "PAGES_KV" --preview

# 4. Create D1 database
echo "🗄️ Création de la base D1..."
wrangler d1 create immo-stats

# 5. Initialize D1 schema
echo "📊 Initialisation du schéma D1..."
wrangler d1 execute immo-stats --file=./schema.sql

# 6. Create R2 bucket
echo "🪣 Création du bucket R2..."
wrangler r2 bucket create immo-assets

# 7. Set secrets
echo "🔑 Configuration des secrets..."
read -p "Enter webhook secret: " webhook_secret
wrangler secret put WEBHOOK_SECRET <<< "$webhook_secret"

# 8. Deploy worker
echo "🚀 Déploiement du Worker..."
wrangler deploy

# 9. Test deployment
echo "✅ Test du déploiement..."
curl -I https://immo-stats.YOUR_SUBDOMAIN.workers.dev/

echo "✨ Setup terminé!"
echo ""
echo "URLs:"
echo "  Worker: https://immo-stats.YOUR_SUBDOMAIN.workers.dev"
echo "  Custom: https://immo.votredomaine.fr (après configuration DNS)"
echo ""
echo "Prochaines étapes:"
echo "1. Configurer le DNS pour pointer vers Cloudflare"
echo "2. Uploader les templates dans R2"
echo "3. Importer les données DVF initiales"
echo "4. Configurer GitHub Actions pour les updates"