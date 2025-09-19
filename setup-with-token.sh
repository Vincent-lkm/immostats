#!/bin/bash

echo "🔑 Configuration avec API Token"
read -p "Colle ton API Token Cloudflare: " CF_TOKEN

export CLOUDFLARE_API_TOKEN=$CF_TOKEN

echo "📚 Création KV namespace..."
KV_ID=$(wrangler kv:namespace create "DATA_KV" --json | jq -r '.id')
echo "KV namespace créé: $KV_ID"

echo "✏️ Mise à jour wrangler.toml..."
sed -i '' "s/YOUR_KV_ID/$KV_ID/" wrangler-simple.toml

echo "🔐 Ajout du webhook secret..."
read -p "Entre un secret pour le webhook (ex: secret123): " WEBHOOK_SECRET
echo "$WEBHOOK_SECRET" | wrangler secret put WEBHOOK_SECRET

echo "🚀 Déploiement du Worker..."
wrangler deploy --config wrangler-simple.toml

echo "✅ Déployé!"
echo ""
echo "URLs:"
echo "  https://immo-stats.$(wrangler whoami --json | jq -r '.account_name').workers.dev"
echo "  https://immobilier.guide (après config DNS)"