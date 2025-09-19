#!/usr/bin/env python3
"""
Compresse les données des villes pour le Worker
Ne garde que les champs essentiels et groupe par département
"""

import json
import gzip

print("📦 Compression des données...")

# Charger les données complètes
with open('output/all_cities_data.json', 'r') as f:
    all_cities = json.load(f)

# Version minimale pour le worker (seulement les champs essentiels)
minimal_cities = {}
for code, city in all_cities.items():
    # Ne garder que les champs essentiels
    minimal_cities[code] = {
        'n': city['name'],  # n = name
        'p': city['prix_m2_appartement'],  # p = prix
        'e': city['evolution_1y'],  # e = evolution
        'v': city['volume_2024'],  # v = volume
        'd': city['departement'],  # d = departement
        'po': city['population']  # po = population
    }

# Sauvegarder version minimale
with open('output/cities_minimal.json', 'w') as f:
    json.dump(minimal_cities, f, ensure_ascii=False, separators=(',', ':'))

# Version gzippée
with gzip.open('output/cities_minimal.json.gz', 'wt', encoding='utf-8') as f:
    json.dump(minimal_cities, f, ensure_ascii=False, separators=(',', ':'))

# Stats
original_size = len(json.dumps(all_cities))
minimal_size = len(json.dumps(minimal_cities))
reduction = (1 - minimal_size/original_size) * 100

print(f"✅ Compression terminée")
print(f"  • Taille originale: {original_size/1024/1024:.1f} MB")
print(f"  • Taille minimale: {minimal_size/1024/1024:.1f} MB")
print(f"  • Réduction: {reduction:.1f}%")

# Créer aussi un index des départements
dept_index = {}
for code, city in minimal_cities.items():
    dept = city['d']
    if dept not in dept_index:
        dept_index[dept] = []
    dept_index[dept].append(code)

with open('output/dept_index.json', 'w') as f:
    json.dump(dept_index, f)

print(f"  • {len(dept_index)} départements indexés")