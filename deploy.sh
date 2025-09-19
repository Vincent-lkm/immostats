#!/bin/bash

# Script de déploiement rapide pour ImmoStats
# Usage: ./deploy.sh "message de commit"

echo "🚀 Déploiement ImmoStats vers GitHub Pages"

# Message de commit (par défaut si non fourni)
COMMIT_MSG="${1:-Update site}"

# Ajouter tous les changements
echo "📦 Ajout des modifications..."
git add -A

# Commit
echo "💾 Commit: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# Push vers GitHub
echo "📤 Push vers GitHub..."
git push origin main

echo "✅ Déploiement lancé!"
echo "   Le site sera mis à jour dans 1-3 minutes sur:"
echo "   → https://www.immostats.fr"
echo "   → https://vincent-lkm.github.io/immostats/"
echo ""
echo "📊 Vérifier le statut:"
echo "   → https://github.com/Vincent-lkm/immostats/actions"