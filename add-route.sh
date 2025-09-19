#!/bin/bash

echo "🌐 Ajout de la route immobilier.guide au Worker"

# Ajouter les routes
wrangler route add "immobilier.guide/*" --zone-name immobilier.guide
wrangler route add "www.immobilier.guide/*" --zone-name immobilier.guide

echo "✅ Routes ajoutées!"
echo ""
echo "Test dans quelques heures (propagation DNS):"
echo "  https://immobilier.guide"
echo "  https://www.immobilier.guide"