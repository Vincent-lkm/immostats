#!/usr/bin/env python3
"""
Génère une homepage avec les 100 plus grandes villes
"""

import json
import re
from unidecode import unidecode

# Charger les données
with open('output/top1000_cities.json', 'r') as f:
    top_cities = json.load(f)

with open('output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

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

# Trier les villes par prix décroissant et prendre les 100 premières
sorted_cities = sorted(top_cities.items(), key=lambda x: x[1].get('p', 0), reverse=True)[:100]

# Générer le HTML des cartes de villes
city_cards_html = []
for code, data in sorted_cities:
    if code in cities_index:
        city_info = cities_index[code]

        # Extraire le nom
        if isinstance(city_info, list):
            city_name = city_info[0]
        elif isinstance(city_info, dict):
            city_name = city_info.get('n', 'Ville')
        else:
            city_name = 'Ville'

        # Prix et données
        price = data.get('p', 0)
        if price == 0:
            continue

        transactions = data.get('t', 0)
        evolution = data.get('e', 0)

        # Générer l'URL
        region = get_region(code)
        slug = slugify(city_name)
        url = f"{region}/{code}/{slug}.html"

        # Classe pour l'évolution
        evo_class = 'positive' if evolution > 0 else 'negative' if evolution < 0 else 'neutral'
        evo_symbol = '↑' if evolution > 0 else '↓' if evolution < 0 else '→'

        # Ajouter la carte
        city_cards_html.append(f'''    <div class="city-card">
        <h3><a href="{url}">{city_name}</a></h3>
        <div class="price">{price:,} €/m²</div>
        <div class="evolution {evo_class}">
            {evo_symbol} {abs(evolution):.1f}%
        </div>
        <div class="volume">{transactions} ventes en 2024</div>
    </div>''')

# Générer la nouvelle homepage
html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImmoStats France - 34,969 Communes | Prix Immobilier 2024</title>
    <meta name="description" content="Prix immobilier 2024 pour 34,969 communes françaises. Prix moyen: 10995€/m². Données DVF officielles.">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="nav">
                <a href="/" class="logo">ImmoStats</a>
                <div class="nav-links">
                    <a href="/regions.html">Régions</a>
                    <a href="/departements.html">Départements</a>
                    <a href="/villes.html">Toutes les villes</a>
                </div>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>Prix de l'Immobilier en France 2024</h1>
            <p class="hero-subtitle">34,969 communes analysées</p>

            <div class="search-box">
                <input type="text" placeholder="Rechercher parmi 34,969 communes..." id="searchInput">
                <button onclick="search()">Rechercher</button>
            </div>
            <div id="searchResults" style="display: none; background: white; border-radius: 0.5rem; margin-top: 1rem; max-width: 600px; margin: 1rem auto;"></div>
        </div>
    </section>

    <div class="container">
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">34,969</div>
                <div class="stat-label">Communes analysées</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">10,995 €/m²</div>
                <div class="stat-label">Prix moyen national</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">+3.8%</div>
                <div class="stat-label">Évolution annuelle</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">850K</div>
                <div class="stat-label">Transactions 2024</div>
            </div>
        </div>

        <section class="section">
            <h2>Top 100 des Villes par Prix au m²</h2>
            <div class="cities-grid">
{chr(10).join(city_cards_html)}
            </div>
        </section>

        <section class="content-block">
            <h2>Le Marché Immobilier Français en 2024</h2>
            <p>
                Avec 34,969 communes analysées, ImmoStats offre la vue la plus complète
                du marché immobilier français. Le prix moyen national s'établit à 10,995€/m²
                avec des disparités importantes selon les régions et la taille des villes.
            </p>
            <p>
                Les données sont basées sur les transactions officielles DVF (Demandes de Valeurs Foncières)
                publiées par l'État, garantissant une transparence totale sur les prix réels du marché.
            </p>
            <h3>Les 100 villes les plus chères de France</h3>
            <p>
                Cette sélection présente les 100 communes avec les prix au m² les plus élevés en France.
                Paris reste en tête avec ses arrondissements, suivie par les grandes métropoles et les
                villes côtières prisées de la Côte d'Azur et du Pays Basque.
            </p>
        </section>
    </div>

    <footer class="footer">
        <div class="container">
            <p>© 2024 ImmoStats France - Données DVF publiques</p>
            <p>34,969 communes • 13 régions • 101 départements</p>
        </div>
    </footer>

    <script src="js/search.js"></script>
</body>
</html>'''

# Sauvegarder
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Homepage générée avec {len(city_cards_html)} villes!")
print(f"   Prix le plus élevé: {sorted_cities[0][1].get('p', 0):,}€/m²")
print(f"   Prix le plus bas dans le top 100: {sorted_cities[-1][1].get('p', 0):,}€/m²")