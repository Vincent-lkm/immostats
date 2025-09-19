#!/usr/bin/env python3
"""
Génère les données pour toutes les communes de France
Utilise l'API geo.api.gouv.fr pour la liste complète
"""

import requests
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def get_all_communes():
    """Récupère la liste de toutes les communes françaises"""
    print("📍 Récupération de toutes les communes de France...")

    # API officielle pour toutes les communes
    url = "https://geo.api.gouv.fr/communes?fields=nom,code,codesPostaux,centre,departement,region,population"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            communes = response.json()
            print(f"✓ {len(communes)} communes trouvées")
            return communes
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

def calculate_realistic_price(commune):
    """Calcule un prix réaliste basé sur la commune"""

    # Prix de base par région (approximatif)
    region_base_prices = {
        "11": 5500,  # Île-de-France
        "93": 3200,  # PACA
        "84": 3400,  # Auvergne-Rhône-Alpes
        "75": 2800,  # Nouvelle-Aquitaine
        "76": 2650,  # Occitanie
        "44": 2100,  # Grand Est
        "32": 1950,  # Hauts-de-France
        "53": 2750,  # Bretagne
        "52": 2600,  # Pays de la Loire
        "28": 2100,  # Normandie
        "24": 1850,  # Centre-Val de Loire
        "27": 1780,  # Bourgogne-Franche-Comté
        "94": 3450,  # Corse
    }

    # Population influence le prix
    pop = commune.get('population', 1000)
    region_code = commune.get('codeRegion', '75')
    dept = commune.get('codeDepartement', '75')

    # Prix de base selon région
    base_price = region_base_prices.get(region_code, 2000)

    # Ajustement selon population
    if pop > 100000:
        price_mult = 2.5  # Grande ville
    elif pop > 50000:
        price_mult = 1.8
    elif pop > 20000:
        price_mult = 1.4
    elif pop > 10000:
        price_mult = 1.2
    elif pop > 5000:
        price_mult = 1.0
    elif pop > 2000:
        price_mult = 0.85
    else:
        price_mult = 0.7  # Petite commune

    # Paris et départements spéciaux
    if dept == '75':  # Paris
        base_price = random.randint(9500, 12500)
        price_mult = 1.0
    elif dept == '92':  # Hauts-de-Seine
        base_price = random.randint(6500, 8500)
    elif dept == '78' or dept == '91':  # Yvelines, Essonne
        base_price = random.randint(4500, 6000)
    elif dept == '06':  # Alpes-Maritimes
        base_price = random.randint(4500, 6500)
    elif dept == '13':  # Bouches-du-Rhône
        base_price = random.randint(3000, 4500)
    elif dept == '69':  # Rhône
        base_price = random.randint(3500, 5000)
    elif dept == '33':  # Gironde
        base_price = random.randint(3000, 4500)

    prix_m2 = int(base_price * price_mult)

    # Variation aléatoire ±10%
    prix_m2 = int(prix_m2 * random.uniform(0.9, 1.1))

    return prix_m2

def process_commune(commune):
    """Traite une commune et génère ses données"""

    code = commune.get('code', '')
    nom = commune.get('nom', 'Inconnu')
    pop = commune.get('population', 0)
    dept = commune.get('codeDepartement', '')
    region = commune.get('codeRegion', '')

    # Coordonnées
    centre = commune.get('centre', {})
    lat = centre.get('coordinates', [0, 0])[1] if centre else 0
    lon = centre.get('coordinates', [0, 0])[0] if centre else 0

    # Prix réaliste
    prix_m2_appart = calculate_realistic_price(commune)
    prix_m2_maison = int(prix_m2_appart * random.uniform(1.1, 1.3))

    # Évolutions réalistes
    evolution_1y = round(random.uniform(-2, 8), 1)
    evolution_5y = round(random.uniform(5, 25), 1)

    # Volume selon population
    if pop > 100000:
        volume_2024 = random.randint(500, 2000)
    elif pop > 50000:
        volume_2024 = random.randint(200, 500)
    elif pop > 10000:
        volume_2024 = random.randint(50, 200)
    elif pop > 5000:
        volume_2024 = random.randint(20, 50)
    else:
        volume_2024 = random.randint(5, 20)

    return {
        "code": code,
        "name": nom,
        "population": pop,
        "departement": dept,
        "region": region,
        "lat": lat,
        "lon": lon,
        "prix_m2_appartement": prix_m2_appart,
        "prix_m2_maison": prix_m2_maison,
        "evolution_1y": evolution_1y,
        "evolution_5y": evolution_5y,
        "volume_2024": volume_2024,
        "volume_2023": int(volume_2024 * 0.95),
        "surface_moyenne": random.randint(55, 85),
        "delai_vente": random.randint(30, 90),
        "tension": round(random.uniform(4, 9), 1),
        "roi_locatif": round(random.uniform(2.5, 5.5), 1)
    }

def main():
    print("🚀 Génération des données pour TOUTES les communes de France")
    print("=" * 60)

    # Récupérer toutes les communes
    communes = get_all_communes()

    if not communes:
        print("❌ Impossible de récupérer les communes")
        return

    print(f"\n🔄 Traitement de {len(communes)} communes...")

    # Traiter toutes les communes
    cities_data = {}

    # Traitement par batch pour afficher la progression
    batch_size = 1000
    total_batches = (len(communes) + batch_size - 1) // batch_size

    for i in range(0, len(communes), batch_size):
        batch = communes[i:i+batch_size]
        batch_num = i // batch_size + 1

        print(f"  Batch {batch_num}/{total_batches} ({len(batch)} communes)...", end='')

        for commune in batch:
            try:
                data = process_commune(commune)
                cities_data[data['code']] = data
            except Exception as e:
                continue

        print(f" ✓ {len(cities_data)} communes traitées")

    # Sauvegarder en plusieurs fichiers pour éviter les gros fichiers
    print(f"\n💾 Sauvegarde des données...")

    # Fichier principal avec toutes les communes
    output_file = "output/all_cities_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cities_data, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(cities_data)} communes sauvegardées dans {output_file}")

    # Créer aussi des fichiers par département pour optimisation
    print("\n📁 Création des fichiers par département...")

    depts = {}
    for code, city in cities_data.items():
        dept = city.get('departement', 'XX')
        if dept not in depts:
            depts[dept] = {}
        depts[dept][code] = city

    for dept, dept_cities in depts.items():
        dept_file = f"output/dept_{dept}_cities.json"
        with open(dept_file, 'w', encoding='utf-8') as f:
            json.dump(dept_cities, f, ensure_ascii=False, indent=2)
        print(f"  Département {dept}: {len(dept_cities)} communes")

    # Stats finales
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print(f"  • {len(cities_data)} communes traitées")
    print(f"  • {len(depts)} départements")
    print(f"  • Prix moyen national: {int(sum(c['prix_m2_appartement'] for c in cities_data.values()) / len(cities_data))} €/m²")

    # Top 10 villes les plus chères
    top_cities = sorted(cities_data.values(), key=lambda x: x['prix_m2_appartement'], reverse=True)[:10]
    print("\n🏆 TOP 10 villes les plus chères:")
    for i, city in enumerate(top_cities, 1):
        print(f"  {i}. {city['name']}: {city['prix_m2_appartement']} €/m²")

if __name__ == "__main__":
    main()