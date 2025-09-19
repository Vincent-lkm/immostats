#!/usr/bin/env python3
"""
Génère les pages HTML pour TOUTES les communes
"""

import json
import os
from pathlib import Path

print("🔨 Génération des pages pour TOUTES les communes...")

# Charger les données
with open('../output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

with open('../output/top1000_cities.json', 'r') as f:
    top_cities = json.load(f)

# Template HTML simple pour les villes
def generate_city_page(code, city_data):
    # Récupérer les données de base
    if isinstance(city_data, list):
        # Format index: [nom, prix]
        name = city_data[0]
        price = city_data[1]
        # Données minimales
        evolution = 0
        volume = 0
        population = 0
    else:
        # Format complet (top1000)
        name = city_data.get('n', 'Ville')
        price = city_data.get('p', 0)
        evolution = city_data.get('e', 0)
        volume = city_data.get('v', 0)
        population = city_data.get('po', 0)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} ({code}) - {price:,}€/m² | ImmoStats</title>
    <meta name="description" content="Prix immobilier {name}: {price:,}€/m² en 2024. Données DVF officielles.">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="nav">
                <a href="../index.html" class="logo">ImmoStats</a>
                <div class="nav-links">
                    <a href="../index.html">← Retour à l'accueil</a>
                </div>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>{name}</h1>
            <p style="opacity: 0.8; margin-bottom: 1rem;">Code INSEE: {code}</p>
            <div style="font-size: 3rem; font-weight: bold; margin: 1rem 0;">
                {price:,} €/m²
            </div>"""

    # Ajouter évolution si disponible
    if evolution != 0 or volume != 0:
        html += f"""
            <div style="font-size: 1.25rem;">"""

        if evolution != 0:
            html += f"""
                <span class="{'positive' if evolution > 0 else 'negative'}">
                    {'↑' if evolution > 0 else '↓'} {abs(evolution)}% sur 1 an
                </span>"""

        html += """
            </div>"""

    html += """
        </div>
    </section>

    <div class="container">"""

    # Stats si disponibles
    if volume > 0 or population > 0:
        html += """
        <div class="stats-bar">"""

        if volume > 0:
            html += f"""
            <div class="stat-item">
                <div class="stat-value">{volume}</div>
                <div class="stat-label">Transactions 2024</div>
            </div>"""

        if population > 0:
            html += f"""
            <div class="stat-item">
                <div class="stat-value">{population:,}</div>
                <div class="stat-label">Population</div>
            </div>"""

        html += """
        </div>"""

    html += f"""
        <section class="content-block">
            <h2>Marché Immobilier à {name}</h2>
            <p>
                {name} affiche un prix moyen de <strong>{price:,}€ au mètre carré</strong> pour un appartement.
                Ces données sont basées sur les transactions immobilières officielles DVF 2024.
            </p>
            <p>
                Cette commune fait partie des 36 000 communes françaises analysées par ImmoStats.
                Les prix sont calculés à partir des données publiques des Demandes de Valeurs Foncières (DVF).
            </p>
        </section>

        <section class="content-block">
            <h2>Informations Pratiques</h2>
            <ul style="line-height: 2;">
                <li>Code INSEE : <strong>{code}</strong></li>
                <li>Prix moyen au m² : <strong>{price:,}€</strong></li>"""

    if volume > 0:
        html += f"""
                <li>Volume de transactions 2024 : <strong>{volume}</strong></li>"""

    if population > 0:
        html += f"""
                <li>Population : <strong>{population:,} habitants</strong></li>"""

    html += """
            </ul>
        </section>
    </div>

    <footer class="footer">
        <div class="container">
            <p>© 2024 ImmoStats France - Données DVF publiques</p>
            <p><a href="../index.html" style="color: #9ca3af;">Retour à l'accueil</a></p>
        </div>
    </footer>
</body>
</html>"""

    return html

# Créer le dossier ville s'il n'existe pas
os.makedirs('ville', exist_ok=True)

# Générer les pages pour TOUTES les communes
count = 0
batch_size = 1000
total = len(cities_index)

print(f"📝 Génération de {total} pages HTML...")

for code, city_data in cities_index.items():
    # Vérifier si on a les données complètes dans top_cities
    if code in top_cities:
        full_data = top_cities[code]
        html = generate_city_page(code, full_data)
    else:
        # Utiliser les données minimales de l'index
        html = generate_city_page(code, city_data)

    # Sauvegarder la page
    with open(f'ville/{code}.html', 'w', encoding='utf-8') as f:
        f.write(html)

    count += 1

    # Afficher la progression
    if count % batch_size == 0:
        print(f"  ✓ {count}/{total} pages créées...")

print(f"\n✅ Terminé! {count} pages HTML créées")
print(f"📁 Toutes les communes sont maintenant accessibles dans site/ville/")