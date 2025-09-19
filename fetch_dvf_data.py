#!/usr/bin/env python3
"""
Script pour télécharger et traiter les données DVF
Génère des JSON optimisés pour Cloudflare KV
"""

import requests
import pandas as pd
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import numpy as np
from collections import defaultdict

# Configuration
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# URLs des fichiers DVF (2023-2024 pour commencer)
DVF_URLS = {
    "2024": "https://www.data.gouv.fr/api/1/datasets/r/5ffa8553-0e8f-4622-add9-5c0b593ca1f8",
    "2023": "https://www.data.gouv.fr/api/1/datasets/r/bc213c7c-c4d4-4385-bf1f-719573d39e90",
}

def download_dvf(year, url):
    """Télécharge un fichier DVF"""
    file_path = DATA_DIR / f"dvf_{year}.txt"

    if file_path.exists():
        print(f"✓ {year} déjà téléchargé")
        return file_path

    print(f"📥 Téléchargement DVF {year}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✓ {year} téléchargé ({file_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return file_path

def process_dvf(file_path, year):
    """Traite un fichier DVF et extrait les données pertinentes"""
    print(f"🔄 Traitement DVF {year}...")

    # Colonnes importantes
    cols_to_keep = [
        'date_mutation', 'nature_mutation', 'valeur_fonciere',
        'code_postal', 'commune', 'code_departement',
        'type_local', 'surface_reelle_bati', 'nombre_pieces_principales',
        'surface_terrain', 'longitude', 'latitude'
    ]

    # Lire le fichier avec pandas (encoding latin-1 pour DVF)
    df = pd.read_csv(file_path, sep='|', low_memory=False,
                     encoding='latin-1',
                     usecols=lambda x: x in cols_to_keep)

    # Nettoyer les données
    df = df[df['nature_mutation'] == 'Vente']
    df = df[df['valeur_fonciere'].notna()]
    df = df[df['type_local'].isin(['Appartement', 'Maison', 'Local industriel. commercial ou assimilé'])]

    # Convertir valeur_fonciere en float
    df['valeur_fonciere'] = df['valeur_fonciere'].str.replace(',', '.').astype(float)

    # Filtrer les valeurs aberrantes
    df = df[(df['valeur_fonciere'] > 10000) & (df['valeur_fonciere'] < 10000000)]

    # Calculer le prix au m²
    df['prix_m2'] = df['valeur_fonciere'] / df['surface_reelle_bati']
    df = df[(df['prix_m2'] > 100) & (df['prix_m2'] < 50000)]

    # Ajouter l'année
    df['annee'] = year

    print(f"✓ {len(df)} transactions valides pour {year}")
    return df

def calculate_city_stats(df, code_postal):
    """Calcule les statistiques pour une ville"""
    city_data = df[df['code_postal'] == code_postal]

    if city_data.empty:
        return None

    stats = {
        'code': code_postal,
        'name': city_data['commune'].iloc[0] if not city_data.empty else 'Commune',
        'volume_2024': 0,
        'volume_2023': 0,
        'transactions': []
    }

    # Stats par type de bien
    for type_bien in ['Appartement', 'Maison']:
        type_data = city_data[city_data['type_local'] == type_bien]
        if not type_data.empty:
            key_prefix = 'appartement' if type_bien == 'Appartement' else 'maison'
            stats[f'prix_m2_{key_prefix}'] = int(type_data['prix_m2'].median())
            stats[f'surface_moyenne_{key_prefix}'] = int(type_data['surface_reelle_bati'].mean())
            stats[f'prix_median_{key_prefix}'] = int(type_data['valeur_fonciere'].median())

    # Volume par année
    for year in city_data['annee'].unique():
        year_data = city_data[city_data['annee'] == year]
        stats[f'volume_{year}'] = len(year_data)

    # Evolution (si on a 2 ans de données)
    if 'prix_m2_appartement' in stats:
        appart_2024 = city_data[(city_data['annee'] == 2024) & (city_data['type_local'] == 'Appartement')]['prix_m2'].median()
        appart_2023 = city_data[(city_data['annee'] == 2023) & (city_data['type_local'] == 'Appartement')]['prix_m2'].median()

        if pd.notna(appart_2024) and pd.notna(appart_2023) and appart_2023 > 0:
            stats['evolution_1y'] = round(((appart_2024 - appart_2023) / appart_2023) * 100, 1)

    # Dernières transactions
    recent = city_data.nlargest(10, 'date_mutation')
    for _, row in recent.iterrows():
        stats['transactions'].append({
            'date': row['date_mutation'],
            'type': row['type_local'],
            'surface': int(row['surface_reelle_bati']) if pd.notna(row['surface_reelle_bati']) else None,
            'prix': int(row['valeur_fonciere']),
            'prix_m2': int(row['prix_m2']) if pd.notna(row['prix_m2']) else None
        })

    # Coordonnées moyennes
    if 'latitude' in city_data.columns:
        stats['lat'] = city_data['latitude'].mean()
        stats['lon'] = city_data['longitude'].mean()

    return stats

def generate_slug(name):
    """Génère un slug URL-friendly"""
    import re
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug

def main():
    print("🚀 Démarrage du traitement DVF")

    # Télécharger les données
    all_data = []
    for year, url in DVF_URLS.items():
        file_path = download_dvf(year, url)
        df = process_dvf(file_path, int(year))
        all_data.append(df)

    # Combiner toutes les années
    print("🔄 Fusion des données...")
    df_all = pd.concat(all_data, ignore_index=True)

    # Obtenir la liste des codes postaux uniques
    codes_postaux = df_all['code_postal'].unique()
    print(f"📍 {len(codes_postaux)} communes trouvées")

    # Calculer les stats par ville
    cities_data = []
    top_cities = []

    print("📊 Calcul des statistiques par ville...")
    for i, code_postal in enumerate(codes_postaux[:500]):  # Limiter à 500 pour le test
        if i % 100 == 0:
            print(f"  Progression: {i}/{len(codes_postaux)}")

        stats = calculate_city_stats(df_all, code_postal)
        if stats and stats.get('volume_2024', 0) + stats.get('volume_2023', 0) > 10:
            cities_data.append({
                'code': code_postal,
                'data': stats
            })

            # Ajouter aux top villes si assez de volume
            if stats.get('volume_2024', 0) > 50:
                top_cities.append({
                    'code': code_postal,
                    'name': stats['name'],
                    'slug': generate_slug(stats['name']),
                    'prix_m2': stats.get('prix_m2_appartement', 0),
                    'evolution': stats.get('evolution_1y', 0),
                    'volume': stats.get('volume_2024', 0)
                })

    # Trier les top villes par volume
    top_cities.sort(key=lambda x: x['volume'], reverse=True)
    top_cities = top_cities[:50]  # Top 50

    # Créer la liste de toutes les villes pour la recherche
    all_cities_list = [{
        'code': c['data']['code'],
        'name': c['data']['name'],
        'slug': generate_slug(c['data']['name'])
    } for c in cities_data]

    # Sauvegarder pour l'upload vers Cloudflare KV
    print("💾 Sauvegarde des données...")

    # Format pour bulk upload KV
    kv_data = {
        'cities': cities_data,
        'top_cities': top_cities,
        'all_cities': all_cities_list,
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_cities': len(cities_data),
            'total_transactions': len(df_all)
        }
    }

    output_file = OUTPUT_DIR / "kv_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kv_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Données sauvegardées dans {output_file}")
    print(f"   - {len(cities_data)} villes avec données")
    print(f"   - {len(top_cities)} top villes")
    print(f"   - {len(df_all)} transactions totales")

    # Créer aussi des fichiers individuels pour test
    sample_city = cities_data[0] if cities_data else None
    if sample_city:
        with open(OUTPUT_DIR / f"sample_city_{sample_city['code']}.json", 'w') as f:
            json.dump(sample_city['data'], f, ensure_ascii=False, indent=2)
        print(f"   - Exemple: {sample_city['data']['name']} ({sample_city['code']})")

if __name__ == "__main__":
    main()