#!/usr/bin/env python3
"""
Ajoute les villes similaires à toutes les pages existantes
Basé sur : même département + prix similaires
"""

import json
import os
import re
from unidecode import unidecode
from glob import glob

print("🔍 Ajout des villes similaires à toutes les pages...")

# Charger les données
print("📊 Chargement des données...")
with open('../output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

try:
    with open('../output/top1000_cities.json', 'r') as f:
        top_cities = json.load(f)
except:
    top_cities = {}

def slugify(text):
    """Convertit un nom en slug URL"""
    text = unidecode(text.lower())
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def get_city_info(code, city_data):
    """Extrait les infos d'une ville"""
    info = {
        'code': code,
        'name': 'Ville',
        'price': 2500,
        'slug': 'ville'
    }

    # Extraire le nom et prix
    if isinstance(city_data, list) and len(city_data) > 0:
        info['name'] = city_data[0]
        if len(city_data) > 1:
            info['price'] = city_data[1]
    elif isinstance(city_data, dict):
        info['name'] = city_data.get('n', 'Ville')
        info['price'] = city_data.get('p', 2500)

    # Enrichir avec top1000
    if code in top_cities:
        top = top_cities[code]
        if isinstance(top, dict):
            info['price'] = top.get('p', info['price'])

    info['slug'] = slugify(info['name'])
    return info

def find_similar_cities(target_code, max_results=3):
    """Trouve les villes similaires dans le même département"""
    target_info = get_city_info(target_code, cities_index.get(target_code, ['Ville', 2500]))
    target_price = target_info['price']

    # Département de la ville cible
    target_dept = target_code[:3] if target_code.startswith('97') else target_code[:2]

    similar = []

    # Parcourir toutes les villes
    for code, city_data in cities_index.items():
        if code == target_code:
            continue

        # Vérifier si même département
        dept = code[:3] if code.startswith('97') else code[:2]
        if dept != target_dept:
            continue

        # Obtenir les infos
        city_info = get_city_info(code, city_data)

        # Calculer la différence de prix
        price_diff = abs(city_info['price'] - target_price)
        price_diff_pct = (price_diff / target_price * 100) if target_price > 0 else 0

        # Ajouter à la liste
        similar.append({
            'code': code,
            'name': city_info['name'],
            'slug': city_info['slug'],
            'price': city_info['price'],
            'diff': price_diff,
            'diff_pct': price_diff_pct
        })

    # Trier par différence de prix
    similar.sort(key=lambda x: x['diff'])

    # Prendre les N plus proches
    return similar[:max_results]

def generate_comparison_html(target_code, similar_cities):
    """Génère le HTML pour les villes similaires"""
    target_info = get_city_info(target_code, cities_index.get(target_code, ['Ville', 2500]))
    target_price = target_info['price']

    html = ''
    for city in similar_cities:
        # Calculer la différence en pourcentage par rapport à la ville cible
        diff_value = city['price'] - target_price
        diff_pct = (diff_value / target_price * 100) if target_price > 0 else 0

        # Classe CSS selon la différence
        diff_class = 'positive' if diff_value < 0 else 'negative' if diff_value > 0 else ''

        # Texte de comparaison
        if abs(diff_pct) < 0.1:
            diff_text = "Prix similaire"
        else:
            diff_text = f"{diff_pct:+.1f}% par rapport à {target_info['name']}"

        html += f'''
        <a href="../{city['code']}/{city['slug']}.html" class="comparison-card">
            <div class="comparison-city">{city['name']}</div>
            <div class="comparison-price">{city['price']:,}€/m²</div>
            <div class="comparison-diff {diff_class}">{diff_text}</div>
        </a>'''

    return html.strip()

# Traiter toutes les pages existantes
print("\n📝 Mise à jour des pages avec villes similaires...")

# Compteurs
updated = 0
errors = 0
total = len(cities_index)

for code, city_data in cities_index.items():
    try:
        # Trouver les villes similaires
        similar = find_similar_cities(code)

        if not similar:
            continue

        # Générer le HTML de comparaison
        comparison_html = generate_comparison_html(code, similar)

        # Trouver le fichier HTML correspondant
        city_info = get_city_info(code, city_data)

        # Chercher dans toutes les régions
        pattern = f"*/{code}/{city_info['slug']}.html"
        files = glob(pattern)

        if not files:
            continue

        filepath = files[0]

        # Lire le fichier
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remplacer la section villes similaires
        # Chercher la div comparison-grid vide
        pattern = r'(<div class="comparison-grid">\s*)(</div>)'
        replacement = f'\\1\n{comparison_html}\n            \\2'

        new_content = re.sub(pattern, replacement, content)

        # Si changement effectué
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1

            if updated % 1000 == 0:
                print(f"  ✓ {updated} pages mises à jour...")

    except Exception as e:
        errors += 1
        if errors < 10:  # Afficher seulement les 10 premières erreurs
            print(f"  ❌ Erreur pour {code}: {str(e)}")
        continue

print("\n✅ Mise à jour terminée!")
print(f"  • {updated} pages mises à jour avec villes similaires")
print(f"  • {errors} erreurs rencontrées")
print(f"  • Villes similaires basées sur: même département + prix proches")

# Exemple de vérification
print("\n📊 Exemple de villes similaires trouvées:")
example_code = '75056'  # Paris
if example_code in cities_index:
    similar = find_similar_cities(example_code, 5)
    print(f"\nPour Paris (75056):")
    for city in similar[:3]:
        print(f"  • {city['name']}: {city['price']:,}€/m² ({city['diff_pct']:.1f}% de différence)")