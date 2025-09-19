#!/usr/bin/env python3
"""
Génère les sitemaps XML par région + un sitemap index
"""

import os
import json
from datetime import datetime
from unidecode import unidecode
import re
from glob import glob

# Charger l'index des villes
with open('output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

# Date actuelle pour lastmod
today = datetime.now().strftime('%Y-%m-%d')

# Mapping des départements vers régions
dept_to_region = {
    '01': 'auvergne-rhone-alpes', '03': 'auvergne-rhone-alpes', '07': 'auvergne-rhone-alpes',
    '15': 'auvergne-rhone-alpes', '26': 'auvergne-rhone-alpes', '38': 'auvergne-rhone-alpes',
    '42': 'auvergne-rhone-alpes', '43': 'auvergne-rhone-alpes', '63': 'auvergne-rhone-alpes',
    '69': 'auvergne-rhone-alpes', '73': 'auvergne-rhone-alpes', '74': 'auvergne-rhone-alpes',

    '21': 'bourgogne-franche-comte', '25': 'bourgogne-franche-comte', '39': 'bourgogne-franche-comte',
    '58': 'bourgogne-franche-comte', '70': 'bourgogne-franche-comte', '71': 'bourgogne-franche-comte',
    '89': 'bourgogne-franche-comte', '90': 'bourgogne-franche-comte',

    '22': 'bretagne', '29': 'bretagne', '35': 'bretagne', '56': 'bretagne',

    '18': 'centre-val-de-loire', '28': 'centre-val-de-loire', '36': 'centre-val-de-loire',
    '37': 'centre-val-de-loire', '41': 'centre-val-de-loire', '45': 'centre-val-de-loire',

    '2A': 'corse', '2B': 'corse',

    '08': 'grand-est', '10': 'grand-est', '51': 'grand-est', '52': 'grand-est',
    '54': 'grand-est', '55': 'grand-est', '57': 'grand-est', '67': 'grand-est',
    '68': 'grand-est', '88': 'grand-est',

    '02': 'hauts-de-france', '59': 'hauts-de-france', '60': 'hauts-de-france',
    '62': 'hauts-de-france', '80': 'hauts-de-france',

    '75': 'ile-de-france', '77': 'ile-de-france', '78': 'ile-de-france', '91': 'ile-de-france',
    '92': 'ile-de-france', '93': 'ile-de-france', '94': 'ile-de-france', '95': 'ile-de-france',

    '14': 'normandie', '27': 'normandie', '50': 'normandie', '61': 'normandie', '76': 'normandie',

    '16': 'nouvelle-aquitaine', '17': 'nouvelle-aquitaine', '19': 'nouvelle-aquitaine', '23': 'nouvelle-aquitaine',
    '24': 'nouvelle-aquitaine', '33': 'nouvelle-aquitaine', '40': 'nouvelle-aquitaine', '47': 'nouvelle-aquitaine',
    '64': 'nouvelle-aquitaine', '79': 'nouvelle-aquitaine', '86': 'nouvelle-aquitaine', '87': 'nouvelle-aquitaine',

    '09': 'occitanie', '11': 'occitanie', '12': 'occitanie', '30': 'occitanie',
    '31': 'occitanie', '32': 'occitanie', '34': 'occitanie', '46': 'occitanie',
    '48': 'occitanie', '65': 'occitanie', '66': 'occitanie', '81': 'occitanie', '82': 'occitanie',

    '44': 'pays-de-la-loire', '49': 'pays-de-la-loire', '53': 'pays-de-la-loire',
    '72': 'pays-de-la-loire', '85': 'pays-de-la-loire',

    '04': 'provence-alpes-cote-azur', '05': 'provence-alpes-cote-azur', '06': 'provence-alpes-cote-azur',
    '13': 'provence-alpes-cote-azur', '83': 'provence-alpes-cote-azur', '84': 'provence-alpes-cote-azur'
}

def get_region(code):
    """Obtient la région d'une commune"""
    if code.startswith('97'):
        dept = code[:3]
        if dept == '971': return 'guadeloupe'
        elif dept == '972': return 'martinique'
        elif dept == '973': return 'guyane'
        elif dept == '974': return 'la-reunion'
        elif dept == '976': return 'mayotte'
        else: return 'autres'
    elif code.startswith('98'):
        return 'autres'
    else:
        dept = code[:2]
        return dept_to_region.get(dept, 'autres')

def slugify(text):
    """Convertit un nom en slug URL"""
    text = unidecode(text.lower())
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# Organiser les villes par région
regions_data = {}

for code, city_data in cities_index.items():
    # Extraire le nom de la ville
    if isinstance(city_data, list):
        city_name = city_data[0]
    elif isinstance(city_data, dict):
        city_name = city_data.get('n', 'ville')
    else:
        city_name = 'ville'

    # Obtenir la région
    region = get_region(code)

    if region not in regions_data:
        regions_data[region] = []

    # Ajouter l'URL de la ville
    slug = slugify(city_name)
    url = f"https://www.immostats.fr/{region}/{code}/{slug}.html"

    regions_data[region].append({
        'url': url,
        'lastmod': today,
        'changefreq': 'weekly',
        'priority': '0.8'
    })

print("🗺️  Génération des sitemaps par région...")

# Générer un sitemap pour chaque région
sitemap_files = []

for region, urls in regions_data.items():
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''

    for url_data in urls:
        sitemap_content += f'''
  <url>
    <loc>{url_data['url']}</loc>
    <lastmod>{url_data['lastmod']}</lastmod>
    <changefreq>{url_data['changefreq']}</changefreq>
    <priority>{url_data['priority']}</priority>
  </url>'''

    sitemap_content += '\n</urlset>'

    # Sauvegarder le sitemap de la région
    filename = f'sitemap-{region}.xml'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)

    sitemap_files.append(filename)
    print(f"  ✓ {filename} - {len(urls)} URLs")

# Ajouter les pages principales dans un sitemap séparé
print("\n🏠 Génération du sitemap des pages principales...")

main_pages = [
    {'url': 'https://www.immostats.fr/', 'priority': '1.0', 'changefreq': 'daily'},
    {'url': 'https://www.immostats.fr/regions.html', 'priority': '0.9', 'changefreq': 'weekly'},
    {'url': 'https://www.immostats.fr/departements.html', 'priority': '0.9', 'changefreq': 'weekly'},
    {'url': 'https://www.immostats.fr/villes.html', 'priority': '0.9', 'changefreq': 'weekly'},
]

# Ajouter les pages de régions principales
for region in regions_data.keys():
    main_pages.append({
        'url': f'https://www.immostats.fr/{region}/',
        'priority': '0.9',
        'changefreq': 'weekly'
    })

main_sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''

for page in main_pages:
    main_sitemap += f'''
  <url>
    <loc>{page['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>'''

main_sitemap += '\n</urlset>'

with open('sitemap-main.xml', 'w', encoding='utf-8') as f:
    f.write(main_sitemap)

sitemap_files.append('sitemap-main.xml')
print(f"  ✓ sitemap-main.xml - {len(main_pages)} URLs")

# Générer le sitemap index
print("\n📑 Génération du sitemap index...")

sitemap_index = '''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''

for filename in sorted(sitemap_files):
    sitemap_index += f'''
  <sitemap>
    <loc>https://www.immostats.fr/{filename}</loc>
    <lastmod>{today}</lastmod>
  </sitemap>'''

sitemap_index += '\n</sitemapindex>'

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_index)

print(f"  ✓ sitemap.xml - Index principal avec {len(sitemap_files)} sitemaps")

# Statistiques
total_urls = sum(len(urls) for urls in regions_data.values()) + len(main_pages)
print(f"\n✅ Sitemaps générés avec succès!")
print(f"  • {len(sitemap_files)} fichiers sitemap créés")
print(f"  • {total_urls} URLs totales")
print(f"  • 1 sitemap index principal (sitemap.xml)")

# Créer aussi un robots.txt mis à jour
print("\n🤖 Mise à jour du robots.txt...")

robots_content = f'''User-agent: *
Allow: /
Sitemap: https://www.immostats.fr/sitemap.xml

# Sitemaps par région'''

for filename in sorted(sitemap_files):
    robots_content += f'\nSitemap: https://www.immostats.fr/{filename}'

robots_content += f'''

# Performance: limiter le crawl des ressources
Crawl-delay: 1

# Deployed: {today}'''

with open('robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots_content)

print("  ✓ robots.txt mis à jour avec tous les sitemaps")