#!/bin/bash

echo "🔍 Recherche de domaines immobilier disponibles..."
echo ""

DOMAINS=(
  "immostats"
  "immo-stats"
  "statimmo"
  "stat-immo"
  "immodata"
  "immo-data"
  "dataimmobilier"
  "data-immo"
  "prix-immo"
  "prix-immobilier"
  "immoanalyse"
  "immo-analyse"
  "immotracker"
  "immo-tracker"
  "immoviz"
  "immo-viz"
  "immomap"
  "immo-map"
)

EXTENSIONS=(
  ".fr"
  ".com"
  ".io"
  ".app"
  ".info"
)

echo "Domaines potentiellement disponibles:"
echo "======================================"

for domain in "${DOMAINS[@]}"; do
  for ext in "${EXTENSIONS[@]}"; do
    full_domain="$domain$ext"

    # Essayer avec curl sur who.is
    result=$(curl -s "https://who.is/whois/$full_domain" | grep -i "No match\|not found\|available" | head -1)

    if [[ ! -z "$result" ]]; then
      echo "✅ $full_domain - Probablement disponible"
    fi

    sleep 0.2
  done
done

echo ""
echo "Suggestions courtes et mémorables:"
echo "=================================="
echo "📊 statimmo.fr"
echo "📈 immodata.io"
echo "🗺️ immomap.fr"
echo "📉 immoviz.app"