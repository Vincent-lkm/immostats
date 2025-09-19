#!/usr/bin/env python3
"""
Génère des données d'exemple pour tester le site
"""

import json
from pathlib import Path
import random

# Créer le dossier output
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Villes d'exemple avec des vraies coordonnées
SAMPLE_CITIES = [
    {"code": "75008", "name": "Paris 8ème", "lat": 48.8736, "lon": 2.2952, "dept": "75"},
    {"code": "75001", "name": "Paris 1er", "lat": 48.8606, "lon": 2.3376, "dept": "75"},
    {"code": "69001", "name": "Lyon 1er", "lat": 45.7640, "lon": 4.8357, "dept": "69"},
    {"code": "13001", "name": "Marseille 1er", "lat": 43.2965, "lon": 5.3698, "dept": "13"},
    {"code": "33000", "name": "Bordeaux", "lat": 44.8378, "lon": -0.5792, "dept": "33"},
    {"code": "59000", "name": "Lille", "lat": 50.6292, "lon": 3.0573, "dept": "59"},
    {"code": "31000", "name": "Toulouse", "lat": 43.6047, "lon": 1.4442, "dept": "31"},
    {"code": "06000", "name": "Nice", "lat": 43.7102, "lon": 7.2620, "dept": "06"},
    {"code": "44000", "name": "Nantes", "lat": 47.2184, "lon": -1.5536, "dept": "44"},
    {"code": "67000", "name": "Strasbourg", "lat": 48.5734, "lon": 7.7521, "dept": "67"},
]

def generate_city_data(city):
    """Génère des données réalistes pour une ville"""

    # Prix de base selon le département
    base_prices = {
        "75": 11000,  # Paris
        "69": 4500,   # Lyon
        "13": 3800,   # Marseille
        "33": 4200,   # Bordeaux
        "59": 3200,   # Lille
        "31": 3500,   # Toulouse
        "06": 5500,   # Nice
        "44": 3800,   # Nantes
        "67": 3600,   # Strasbourg
    }

    base_price = base_prices.get(city["dept"], 3000)
    variation = random.uniform(-0.2, 0.3)
    prix_m2_appart = int(base_price * (1 + variation))
    prix_m2_maison = int(prix_m2_appart * random.uniform(0.8, 1.2))

    # Evolution aléatoire mais réaliste
    evolution_1y = round(random.uniform(-5, 8), 1)

    # Volume de transactions
    volume = random.randint(50, 500)

    # Génération de transactions récentes
    transactions = []
    for i in range(10):
        type_bien = random.choice(["Appartement", "Maison", "Appartement", "Appartement"])  # Plus d'apparts
        if type_bien == "Appartement":
            surface = random.randint(20, 150)
            prix_m2 = prix_m2_appart + random.randint(-500, 500)
        else:
            surface = random.randint(60, 250)
            prix_m2 = prix_m2_maison + random.randint(-800, 800)

        prix_total = surface * prix_m2

        transactions.append({
            "date": f"2024-{random.randint(10,11):02d}-{random.randint(1,28):02d}",
            "type": type_bien,
            "surface": surface,
            "prix": prix_total,
            "prix_m2": prix_m2
        })

    # Evolution mensuelle
    evolution = []
    current_price = prix_m2_appart - (prix_m2_appart * 0.05)  # Start 5% lower
    for month in range(1, 13):
        current_price += random.uniform(-100, 150)
        evolution.append({
            "month": f"2024-{month:02d}",
            "prix_m2": int(current_price)
        })

    return {
        "code": city["code"],
        "name": city["name"],
        "lat": city["lat"],
        "lon": city["lon"],
        "prix_m2_appartement": prix_m2_appart,
        "prix_m2_maison": prix_m2_maison,
        "evolution_1y": evolution_1y,
        "volume_2024": volume,
        "surface_moyenne": random.randint(65, 85),
        "prix_median": prix_m2_appart * 75,  # Pour un 75m²
        "transactions": transactions,
        "evolution": evolution
    }

def generate_slug(name):
    """Génère un slug URL"""
    import re
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug

def main():
    print("🎲 Génération de données d'exemple...")

    cities_data = []
    top_cities = []
    all_cities = []

    for city in SAMPLE_CITIES:
        # Générer les données
        data = generate_city_data(city)

        # Ajouter aux listes
        cities_data.append({
            "code": city["code"],
            "data": data
        })

        top_cities.append({
            "code": city["code"],
            "name": city["name"],
            "slug": generate_slug(city["name"]),
            "prix_m2": data["prix_m2_appartement"],
            "evolution": data["evolution_1y"],
            "volume": data["volume_2024"]
        })

        all_cities.append({
            "code": city["code"],
            "name": city["name"],
            "slug": generate_slug(city["name"])
        })

    # Ajouter quelques villes supplémentaires pour la recherche
    extra_cities = [
        {"code": "92200", "name": "Neuilly-sur-Seine"},
        {"code": "92100", "name": "Boulogne-Billancourt"},
        {"code": "78000", "name": "Versailles"},
        {"code": "35000", "name": "Rennes"},
        {"code": "34000", "name": "Montpellier"},
    ]

    for city in extra_cities:
        all_cities.append({
            "code": city["code"],
            "name": city["name"],
            "slug": generate_slug(city["name"])
        })

    # Trier les top cities par prix
    top_cities.sort(key=lambda x: x["prix_m2"], reverse=True)

    # Préparer le format KV
    kv_data = {
        "cities": cities_data,
        "top_cities": top_cities,
        "all_cities": all_cities,
        "metadata": {
            "generated_at": "2024-11-20T10:00:00Z",
            "total_cities": len(cities_data),
            "demo_data": True
        }
    }

    # Sauvegarder
    output_file = OUTPUT_DIR / "kv_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kv_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Données générées!")
    print(f"   - {len(cities_data)} villes avec données complètes")
    print(f"   - {len(all_cities)} villes pour la recherche")
    print(f"   - Fichier: {output_file}")

    # Créer aussi un fichier d'exemple
    sample = cities_data[0]["data"]
    with open(OUTPUT_DIR / f"sample_city_{sample['code']}.json", 'w') as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)
        print(f"   - Exemple: {sample['name']} ({sample['code']})")

if __name__ == "__main__":
    main()