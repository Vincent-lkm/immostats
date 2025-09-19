#!/usr/bin/env python3
"""
Limite le site à 19,000 villes pour Cloudflare Pages
Garde uniquement les villes avec le plus de transactions
"""

import os
import json
import shutil
from glob import glob

print("🔄 Limitation à 19,000 villes pour Cloudflare Pages...")

# Charger les données
with open('output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

with open('output/top1000_cities.json', 'r') as f:
    top_cities = json.load(f)

# Créer un dictionnaire avec le nombre de transactions pour chaque ville
city_transactions = {}

for code in cities_index.keys():
    # Récupérer le nombre de transactions depuis top1000 si disponible
    if code in top_cities:
        transactions = top_cities[code].get('t', 0)
    else:
        transactions = 0

    city_transactions[code] = transactions

# Trier les villes par nombre de transactions (décroissant)
sorted_cities = sorted(city_transactions.items(), key=lambda x: x[1], reverse=True)

# Prendre les 19,000 premières villes
cities_to_keep = [code for code, _ in sorted_cities[:19000]]
cities_to_delete = [code for code, _ in sorted_cities[19000:]]

print(f"📊 Statistiques:")
print(f"   • Total villes: {len(cities_index)}")
print(f"   • Villes à garder: {len(cities_to_keep)}")
print(f"   • Villes à supprimer: {len(cities_to_delete)}")
print(f"   • Seuil de transactions: {sorted_cities[18999][1]} ventes minimum")

# Supprimer les fichiers HTML des villes avec le moins de transactions
deleted_count = 0
errors = 0

print(f"\n🗑️  Suppression des {len(cities_to_delete)} villes avec le moins de transactions...")

for code in cities_to_delete:
    # Chercher le fichier HTML correspondant
    pattern = f"*/{code}/*.html"
    files = glob(pattern)

    for filepath in files:
        try:
            os.remove(filepath)
            deleted_count += 1

            # Supprimer aussi le dossier si vide
            folder = os.path.dirname(filepath)
            if not os.listdir(folder):
                os.rmdir(folder)

            if deleted_count % 1000 == 0:
                print(f"   ✓ {deleted_count} fichiers supprimés...")

        except Exception as e:
            errors += 1
            if errors < 10:
                print(f"   ❌ Erreur: {filepath} - {str(e)}")

# Créer un nouvel index avec seulement les villes gardées
cities_index_limited = {code: cities_index[code] for code in cities_to_keep if code in cities_index}

# Sauvegarder le nouvel index
with open('output/cities_index_19k.json', 'w') as f:
    json.dump(cities_index_limited, f, ensure_ascii=False)

print(f"\n✅ Limitation terminée!")
print(f"   • {deleted_count} fichiers supprimés")
print(f"   • {errors} erreurs")
print(f"   • Nouvel index: output/cities_index_19k.json")

# Compter les fichiers restants
remaining_files = len(glob("*/*/*.html"))
print(f"   • Fichiers HTML restants: {remaining_files}")

if remaining_files > 19000:
    print(f"\n⚠️  Attention: Il reste {remaining_files} fichiers, plus que la limite de 19,000")
    print(f"   Certaines régions ont plusieurs fichiers par ville")
else:
    print(f"\n✅ Le site contient maintenant moins de 19,000 fichiers!")
    print(f"   Prêt pour Cloudflare Pages!")

# Afficher les villes les plus populaires gardées
print(f"\n🏆 Top 10 des villes gardées (par transactions):")
for i, (code, transactions) in enumerate(sorted_cities[:10]):
    if code in cities_index:
        city_data = cities_index[code]
        if isinstance(city_data, list):
            name = city_data[0]
        else:
            name = city_data.get('n', 'Ville')
        print(f"   {i+1}. {name} ({code}): {transactions} ventes")

# Afficher quelques villes supprimées
print(f"\n📉 Exemples de villes supprimées (moins de transactions):")
for i, (code, transactions) in enumerate(sorted_cities[19000:19010]):
    if code in cities_index:
        city_data = cities_index[code]
        if isinstance(city_data, list):
            name = city_data[0]
        else:
            name = city_data.get('n', 'Ville')
        print(f"   • {name} ({code}): {transactions} ventes")