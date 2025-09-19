#!/bin/bash

echo "🚀 Deploy ImmoStats sur Cloudflare Workers"

# 1. Create KV namespace
echo "📚 Création KV namespace..."
wrangler kv:namespace create "DATA_KV"

# 2. Set webhook secret
echo "🔑 Configuration secret..."
read -p "Webhook secret: " secret
wrangler secret put WEBHOOK_SECRET <<< "$secret"

# 3. Deploy
echo "🚀 Déploiement..."
wrangler deploy --config wrangler-simple.toml

echo "✅ Fait! URL: https://immo-stats.YOUR.workers.dev"