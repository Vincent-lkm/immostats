#!/usr/bin/env python3
"""
Corrige les liens de la homepage pour pointer vers la nouvelle structure
"""

import json
import re
from unidecode import unidecode

# Charger l'index des villes
with open('output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

# Mapping des codes vers les régions
region_mapping = {
    '75': 'ile-de-france', '77': 'ile-de-france', '78': 'ile-de-france', '91': 'ile-de-france',
    '92': 'ile-de-france', '93': 'ile-de-france', '94': 'ile-de-france', '95': 'ile-de-france',
    '13': 'provence-alpes-cote-azur', '06': 'provence-alpes-cote-azur', '83': 'provence-alpes-cote-azur',
    '69': 'auvergne-rhone-alpes',
    '31': 'occitanie', '34': 'occitanie',
    '44': 'pays-de-la-loire',
    '67': 'grand-est',
    '33': 'nouvelle-aquitaine',
    '59': 'hauts-de-france',
    '35': 'bretagne'
}

def get_region(code):
    """Obtient la région d'une commune"""
    dept = code[:3] if code.startswith('97') else code[:2]
    return region_mapping.get(dept, 'autres')

def slugify(text):
    """Convertit un nom en slug URL"""
    text = unidecode(text.lower())
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

# Lire la homepage
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Codes des villes sur la homepage
city_codes = ['75056', '13055', '69123', '31555', '44109', '34172', '67482', '33063', '59350', '35238', '83137']

# Remplacer chaque lien
for code in city_codes:
    if code in cities_index:
        city_data = cities_index[code]

        # Extraire le nom
        if isinstance(city_data, list):
            city_name = city_data[0]
        elif isinstance(city_data, dict):
            city_name = city_data.get('n', 'ville')
        else:
            city_name = 'ville'

        # Construire le nouveau lien
        region = get_region(code)
        slug = slugify(city_name)
        new_url = f"{region}/{code}/{slug}.html"

        # Remplacer l'ancien lien
        old_pattern = f'href="ville/{code}.html"'
        new_pattern = f'href="{new_url}"'

        content = content.replace(old_pattern, new_pattern)
        print(f"Remplacé: ville/{code}.html → {new_url}")

# Sauvegarder
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Homepage mise à jour avec les nouveaux liens!")