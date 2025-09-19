#!/usr/bin/env python3
"""
Génère des pages HTML dans la structure /region/code-insee/nom-ville.html
"""

import json
import os
import re
from unidecode import unidecode

print("🔨 Génération des pages HTML structurées par région...")

# Mapping département -> région
DEPT_TO_REGION = {
    # Auvergne-Rhône-Alpes
    '01': 'auvergne-rhone-alpes', '03': 'auvergne-rhone-alpes', '07': 'auvergne-rhone-alpes',
    '15': 'auvergne-rhone-alpes', '26': 'auvergne-rhone-alpes', '38': 'auvergne-rhone-alpes',
    '42': 'auvergne-rhone-alpes', '43': 'auvergne-rhone-alpes', '63': 'auvergne-rhone-alpes',
    '69': 'auvergne-rhone-alpes', '73': 'auvergne-rhone-alpes', '74': 'auvergne-rhone-alpes',

    # Bourgogne-Franche-Comté
    '21': 'bourgogne-franche-comte', '25': 'bourgogne-franche-comte', '39': 'bourgogne-franche-comte',
    '58': 'bourgogne-franche-comte', '70': 'bourgogne-franche-comte', '71': 'bourgogne-franche-comte',
    '89': 'bourgogne-franche-comte', '90': 'bourgogne-franche-comte',

    # Bretagne
    '22': 'bretagne', '29': 'bretagne', '35': 'bretagne', '56': 'bretagne',

    # Centre-Val de Loire
    '18': 'centre-val-de-loire', '28': 'centre-val-de-loire', '36': 'centre-val-de-loire',
    '37': 'centre-val-de-loire', '41': 'centre-val-de-loire', '45': 'centre-val-de-loire',

    # Corse
    '2A': 'corse', '2B': 'corse',

    # Grand Est
    '08': 'grand-est', '10': 'grand-est', '51': 'grand-est', '52': 'grand-est',
    '54': 'grand-est', '55': 'grand-est', '57': 'grand-est', '67': 'grand-est',
    '68': 'grand-est', '88': 'grand-est',

    # Hauts-de-France
    '02': 'hauts-de-france', '59': 'hauts-de-france', '60': 'hauts-de-france',
    '62': 'hauts-de-france', '80': 'hauts-de-france',

    # Île-de-France
    '75': 'ile-de-france', '77': 'ile-de-france', '78': 'ile-de-france',
    '91': 'ile-de-france', '92': 'ile-de-france', '93': 'ile-de-france',
    '94': 'ile-de-france', '95': 'ile-de-france',

    # Normandie
    '14': 'normandie', '27': 'normandie', '50': 'normandie', '61': 'normandie', '76': 'normandie',

    # Nouvelle-Aquitaine
    '16': 'nouvelle-aquitaine', '17': 'nouvelle-aquitaine', '19': 'nouvelle-aquitaine',
    '23': 'nouvelle-aquitaine', '24': 'nouvelle-aquitaine', '33': 'nouvelle-aquitaine',
    '40': 'nouvelle-aquitaine', '47': 'nouvelle-aquitaine', '64': 'nouvelle-aquitaine',
    '79': 'nouvelle-aquitaine', '86': 'nouvelle-aquitaine', '87': 'nouvelle-aquitaine',

    # Occitanie
    '09': 'occitanie', '11': 'occitanie', '12': 'occitanie', '30': 'occitanie',
    '31': 'occitanie', '32': 'occitanie', '34': 'occitanie', '46': 'occitanie',
    '48': 'occitanie', '65': 'occitanie', '66': 'occitanie', '81': 'occitanie', '82': 'occitanie',

    # Pays de la Loire
    '44': 'pays-de-la-loire', '49': 'pays-de-la-loire', '53': 'pays-de-la-loire',
    '72': 'pays-de-la-loire', '85': 'pays-de-la-loire',

    # Provence-Alpes-Côte d'Azur
    '04': 'provence-alpes-cote-azur', '05': 'provence-alpes-cote-azur', '06': 'provence-alpes-cote-azur',
    '13': 'provence-alpes-cote-azur', '83': 'provence-alpes-cote-azur', '84': 'provence-alpes-cote-azur',

    # DOM-TOM
    '971': 'guadeloupe', '972': 'martinique', '973': 'guyane', '974': 'la-reunion', '976': 'mayotte'
}

def slugify(text):
    """Convertit un nom de ville en slug URL-friendly"""
    # Convertir en minuscules et retirer les accents
    text = unidecode(text.lower())
    # Remplacer les espaces et caractères spéciaux par des tirets
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Retirer les tirets en début et fin
    text = text.strip('-')
    return text

def get_region(code):
    """Obtient la région à partir du code INSEE"""
    # Extraire le département
    if code.startswith('97'):
        dept = code[:3]
    else:
        dept = code[:2]

    # Retourner la région ou 'autres' par défaut
    return DEPT_TO_REGION.get(dept, 'autres')

# Charger les données
with open('../output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

with open('../output/top1000_cities.json', 'r') as f:
    top_cities = json.load(f)

# Charger le template
with open('gab.html', 'r', encoding='utf-8') as f:
    template = f.read()

def generate_city_page(code, city_data):
    """Génère une page HTML pour une ville"""
    # Extraire les données
    if isinstance(city_data, list):
        name = city_data[0]
        price = city_data[1] if len(city_data) > 1 else 2500
    else:
        name = city_data.get('n', 'Ville')
        price = city_data.get('p', 2500)

    # Générer les données mock pour le template
    import random

    evolution = random.uniform(-5, 10)
    volume = random.randint(10, 500)
    price_house = int(price * random.uniform(0.8, 1.2))
    surface = random.randint(60, 120)
    delay = random.randint(30, 120)
    tension = random.uniform(0.5, 5.0)
    roi = random.uniform(3, 8)

    dept = code[:2] if not code.startswith('97') else code[:3]

    # Coordonnées approximatives
    coords = {
        '75': [48.8566, 2.3522],
        '13': [43.2965, 5.3698],
        '69': [45.764, 4.8357],
        '31': [43.6047, 1.4442],
        '06': [43.7102, 7.2620],
    }.get(dept, [46.603354, 1.888334])

    lat = coords[0] + random.uniform(-0.5, 0.5)
    lon = coords[1] + random.uniform(-0.5, 0.5)

    # Données historiques pour graphiques
    years = list(range(2020, 2025))
    price_history = []
    volume_history = []
    current_price = price
    current_volume = volume

    for year in reversed(years):
        price_history.insert(0, int(current_price))
        volume_history.insert(0, int(current_volume))
        current_price *= 0.95
        current_volume = int(current_volume * random.uniform(0.8, 1.2))

    # Remplacer les placeholders
    html = template
    replacements = {
        '{{VILLE_NOM}}': name,
        '{{VILLE_CODE}}': code,
        '{{PRIX_M2}}': f"{price:,}".replace(',', ' '),
        '{{EVOLUTION}}': f"{evolution:+.1f}",
        '{{VOLUME}}': str(volume),
        '{{PRIX_MAISON}}': f"{price_house:,}".replace(',', ' '),
        '{{SURFACE_MOYENNE}}': str(surface),
        '{{DELAI_VENTE}}': str(delay),
        '{{TENSION}}': f"{tension:.1f}",
        '{{ROI}}': f"{roi:.1f}",
        '{{LATITUDE}}': str(lat),
        '{{LONGITUDE}}': str(lon),
        '{{YEARS}}': str(years),
        '{{PRICE_HISTORY}}': str(price_history),
        '{{VOLUME_HISTORY}}': str(volume_history),
        '{{DEPARTEMENT}}': dept,
        '{{POPULATION}}': f"{random.randint(1000, 50000):,}".replace(',', ' '),
    }

    # Remplacer tous les placeholders
    for key, value in replacements.items():
        html = html.replace(key, value)

    # Nettoyer les placeholders restants
    html = re.sub(r'\{\{[^}]+\}\}', '', html)

    # Ajuster les chemins des ressources (remonter de 3 niveaux)
    html = html.replace('href="../', 'href="../../../')
    html = html.replace('src="../', 'src="../../../')

    return html

# Générer les pages
count = 0
total = len(cities_index)
print(f"📝 Génération de {total} pages structurées...")

for code, city_data in cities_index.items():
    # Obtenir le nom de la ville et la région
    if isinstance(city_data, list):
        name = city_data[0]
    else:
        name = city_data.get('n', 'Ville')

    region = get_region(code)
    slug = slugify(name)

    # Créer la structure de dossiers
    dir_path = f"{region}/{code}"
    os.makedirs(dir_path, exist_ok=True)

    # Utiliser les données complètes si disponibles
    if code in top_cities:
        html = generate_city_page(code, top_cities[code])
    else:
        html = generate_city_page(code, city_data)

    # Sauvegarder la page
    file_path = f"{dir_path}/{slug}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    count += 1

    if count % 1000 == 0:
        print(f"  ✓ {count}/{total} pages créées...")

    # Pour tester, limiter à 100 pages
    if count >= 100:
        print(f"\n🔧 Test limité à 100 pages pour validation")
        break

print(f"\n✅ {count} pages HTML créées avec structure /region/code-insee/nom-ville.html")
print(f"📁 Structure créée dans site/[region]/[code]/[nom-ville].html")

# Afficher quelques exemples
print("\n📌 Exemples de pages créées:")
examples = 0
for code in list(cities_index.keys())[:5]:
    if isinstance(cities_index[code], list):
        name = cities_index[code][0]
    else:
        name = cities_index[code].get('n', 'Ville')

    region = get_region(code)
    slug = slugify(name)
    print(f"  • /{region}/{code}/{slug}.html")