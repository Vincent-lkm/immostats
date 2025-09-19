#!/usr/bin/env python3
"""
Divise les données des villes en chunks pour Cloudflare Workers
Stratégie: créer plusieurs workers ou utiliser une API externe
"""

import json
import os

print("📦 Division des données pour Workers...")

# Charger les données minimales
with open('output/cities_minimal.json', 'r') as f:
    all_cities = json.load(f)

# Stratégie 1: Top 1000 villes par population pour le worker principal
cities_with_pop = [(code, data) for code, data in all_cities.items()]
cities_with_pop.sort(key=lambda x: x[1].get('po', 0), reverse=True)

# Top 1000 villes
top_cities = dict(cities_with_pop[:1000])

# Sauvegarder les top villes
with open('output/top1000_cities.json', 'w') as f:
    json.dump(top_cities, f, ensure_ascii=False, separators=(',', ':'))

# Calculer tailles
top_size = len(json.dumps(top_cities))
print(f"✅ Top 1000 villes: {top_size/1024:.1f} KB")

# Stratégie 2: Créer un index léger avec juste nom et prix
index_data = {}
for code, city in all_cities.items():
    index_data[code] = [city['n'], city['p']]  # [nom, prix]

with open('output/cities_index.json', 'w') as f:
    json.dump(index_data, f, ensure_ascii=False, separators=(',', ':'))

index_size = len(json.dumps(index_data))
print(f"✅ Index complet: {index_size/1024:.1f} KB")

# Stratégie 3: Créer fichiers par département pour API externe
dept_files = {}
for code, city in all_cities.items():
    # Extraire code département (2 ou 3 premiers caractères)
    if code.startswith('97'):
        dept = code[:3]  # DOM-TOM
    else:
        dept = code[:2]

    if dept not in dept_files:
        dept_files[dept] = {}

    dept_files[dept][code] = city

# Créer dossier pour fichiers département
os.makedirs('output/depts', exist_ok=True)

dept_summary = []
for dept, cities in dept_files.items():
    filename = f'output/depts/{dept}.json'
    with open(filename, 'w') as f:
        json.dump(cities, f, ensure_ascii=False, separators=(',', ':'))

    size = len(json.dumps(cities))
    dept_summary.append({
        'dept': dept,
        'cities': len(cities),
        'size_kb': round(size/1024, 1)
    })

# Afficher résumé
print(f"\n📊 Résumé des fichiers département:")
dept_summary.sort(key=lambda x: x['cities'], reverse=True)
for d in dept_summary[:10]:
    print(f"  Dept {d['dept']}: {d['cities']} villes, {d['size_kb']} KB")

print(f"\n✅ {len(dept_files)} fichiers département créés")

# Créer un manifest pour le worker
manifest = {
    'total_cities': len(all_cities),
    'top_cities_included': 1000,
    'departments': list(dept_files.keys()),
    'data_urls': {
        'index': 'https://raw.githubusercontent.com/immostats/data/main/cities_index.json',
        'top1000': 'https://raw.githubusercontent.com/immostats/data/main/top1000_cities.json'
    }
}

with open('output/manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)

print("\n💡 Stratégie recommandée:")
print("  1. Inclure top 1000 villes directement dans le worker")
print("  2. Charger les autres à la demande depuis GitHub/CDN")
print("  3. Utiliser cache Cloudflare pour optimiser")