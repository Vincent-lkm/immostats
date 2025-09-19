#!/usr/bin/env python3
"""
Script pour télécharger et traiter TOUS les départements de France
Optimisé pour 36000 communes
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import concurrent.futures
import time

# Configuration
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# TOUS les départements de France (métropole + DOM)
ALL_DEPARTMENTS = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '2A', '2B',
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
    '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
    '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
    '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
    '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
    '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
    '81', '82', '83', '84', '85', '86', '87', '88', '89', '90',
    '91', '92', '93', '94', '95',
    '971', '972', '973', '974', '976'  # DOM
]

def download_department(dept):
    """Télécharge les données d'un département"""
    url = f"https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/{dept}.csv.gz"

    try:
        print(f"  📥 Département {dept}...", end='', flush=True)
        df = pd.read_csv(url, compression='gzip', low_memory=False,
                        dtype={'code_postal': str, 'code_commune': str})
        print(f" ✓ {len(df)} lignes")
        return df
    except Exception as e:
        print(f" ❌ Erreur: {e}")
        return None

def process_department_data(df):
    """Nettoie les données d'un département"""
    if df is None or df.empty:
        return pd.DataFrame()

    # Filtrer ventes uniquement
    df = df[df['nature_mutation'] == 'Vente'].copy()

    # Types de biens intéressants
    df = df[df['type_local'].isin(['Appartement', 'Maison', 'Local industriel. commercial ou assimilé'])].copy()

    # Nettoyer valeurs
    df = df[df['valeur_fonciere'].notna()]
    df = df[(df['valeur_fonciere'] > 5000) & (df['valeur_fonciere'] < 10000000)]

    # Surface et prix/m²
    if 'surface_reelle_bati' in df.columns:
        df['surface_totale'] = df['surface_reelle_bati'].fillna(0)
        df = df[df['surface_totale'] > 10]
        df['prix_m2'] = df['valeur_fonciere'] / df['surface_totale']
        df = df[(df['prix_m2'] > 100) & (df['prix_m2'] < 50000)]

    return df

def calculate_city_stats(city_group):
    """Calcule les stats pour une ville"""
    code_postal, city_df = city_group

    if len(city_df) < 3:  # Minimum 3 transactions
        return None

    stats = {
        'code': str(code_postal).zfill(5),
        'name': city_df['nom_commune'].iloc[0] if 'nom_commune' in city_df.columns else f"Commune {code_postal}",
        'volume_2024': len(city_df),
        'department': str(city_df['code_departement'].iloc[0]) if 'code_departement' in city_df.columns else code_postal[:2]
    }

    # Stats appartements
    appart_df = city_df[city_df['type_local'] == 'Appartement']
    if len(appart_df) >= 2:
        stats['prix_m2_appartement'] = int(appart_df['prix_m2'].median())
        stats['surface_moyenne_appartement'] = int(appart_df['surface_totale'].mean())

    # Stats maisons
    maison_df = city_df[city_df['type_local'] == 'Maison']
    if len(maison_df) >= 2:
        stats['prix_m2_maison'] = int(maison_df['prix_m2'].median())
        stats['surface_moyenne_maison'] = int(maison_df['surface_totale'].mean())

    # Coordonnées
    if 'latitude' in city_df.columns:
        lat = city_df['latitude'].median()
        lon = city_df['longitude'].median()
        if pd.notna(lat) and pd.notna(lon):
            stats['lat'] = float(lat)
            stats['lon'] = float(lon)

    # Top 5 transactions récentes
    stats['transactions'] = []
    recent = city_df.nlargest(5, 'date_mutation') if 'date_mutation' in city_df.columns else city_df.head(5)
    for _, row in recent.iterrows():
        stats['transactions'].append({
            'date': row.get('date_mutation', '2024-01-01'),
            'type': row['type_local'],
            'prix': int(row['valeur_fonciere']),
            'surface': int(row.get('surface_totale', 0))
        })

    return stats

def generate_slug(name):
    """Génère un slug URL"""
    import re
    import unicodedata

    # Normaliser les caractères Unicode
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')

    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug

def main():
    print("🚀 Traitement DVF - TOUTE LA FRANCE (36000 communes)")
    print("=" * 60)
    start_time = time.time()

    all_data = []

    # Télécharger tous les départements (en parallèle par batch)
    print(f"📥 Téléchargement de {len(ALL_DEPARTMENTS)} départements...")

    batch_size = 10
    for i in range(0, len(ALL_DEPARTMENTS), batch_size):
        batch = ALL_DEPARTMENTS[i:i+batch_size]
        print(f"\nBatch {i//batch_size + 1}/{(len(ALL_DEPARTMENTS)+batch_size-1)//batch_size}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(download_department, dept) for dept in batch]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        for df in results:
            if df is not None:
                all_data.append(df)

    print(f"\n✓ {len(all_data)} départements téléchargés")

    # Combiner toutes les données
    print("\n🔄 Fusion des données...")
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"   {len(combined_df)} lignes au total")

    # Nettoyer
    print("🧹 Nettoyage des données...")
    combined_df = process_department_data(combined_df)
    print(f"   {len(combined_df)} transactions valides")

    # Calculer stats par ville
    print("\n📊 Calcul des statistiques par ville...")
    grouped = combined_df.groupby('code_postal')
    cities_data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(calculate_city_stats, group) for group in grouped]

        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            if i % 500 == 0:
                print(f"   Progression: {i}/{len(grouped)} villes")

            result = future.result()
            if result:
                cities_data.append(result)

    print(f"✓ {len(cities_data)} villes avec données")

    # Créer les différentes listes
    print("\n📦 Préparation des données pour export...")

    # Top villes (>50 transactions)
    top_cities = [
        {
            'code': c['code'],
            'name': c['name'],
            'slug': generate_slug(c['name']),
            'prix_m2': c.get('prix_m2_appartement', c.get('prix_m2_maison', 0)),
            'volume': c['volume_2024']
        }
        for c in cities_data if c['volume_2024'] > 50
    ]
    top_cities.sort(key=lambda x: x['volume'], reverse=True)
    top_cities = top_cities[:200]  # Top 200 villes

    # Liste complète pour recherche
    all_cities_list = [
        {
            'code': c['code'],
            'name': c['name'],
            'slug': generate_slug(c['name'])
        }
        for c in cities_data
    ]

    # Statistiques nationales
    national_stats = {
        'total_cities': len(cities_data),
        'total_transactions': len(combined_df),
        'average_price_m2': int(combined_df['prix_m2'].median()) if 'prix_m2' in combined_df.columns else 0,
        'top_departments': combined_df['code_departement'].value_counts().head(10).to_dict() if 'code_departement' in combined_df.columns else {}
    }

    # Sauvegarder
    print("\n💾 Sauvegarde des données...")

    # Metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'total_cities': len(cities_data),
        'total_transactions': len(combined_df),
        'departments_processed': len(ALL_DEPARTMENTS),
        'national_stats': national_stats
    }
    with open(OUTPUT_DIR / 'metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # Top cities
    with open(OUTPUT_DIR / 'top_cities.json', 'w', encoding='utf-8') as f:
        json.dump(top_cities, f, ensure_ascii=False, indent=2)

    # All cities (pour recherche)
    with open(OUTPUT_DIR / 'all_cities.json', 'w', encoding='utf-8') as f:
        json.dump(all_cities_list, f, ensure_ascii=False, indent=2)

    # Cities data en batches
    batch_size = 500  # 500 villes par fichier
    num_batches = (len(cities_data) + batch_size - 1) // batch_size

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, len(cities_data))
        batch = cities_data[start_idx:end_idx]

        filename = OUTPUT_DIR / f'cities_batch_{i:04d}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(batch, f, ensure_ascii=False)

        if i == 0 or (i + 1) % 10 == 0 or i == num_batches - 1:
            print(f"   Batch {i+1}/{num_batches} sauvegardé ({len(batch)} villes)")

    # Durée totale
    duration = time.time() - start_time

    print("\n" + "=" * 60)
    print("✅ TRAITEMENT TERMINÉ!")
    print(f"   🏘️  {len(cities_data)} communes traitées")
    print(f"   📊 {len(combined_df):,} transactions analysées")
    print(f"   🌟 {len(top_cities)} top villes identifiées")
    print(f"   📁 {num_batches} fichiers de données générés")
    print(f"   ⏱️  Durée: {duration//60:.0f}m {duration%60:.0f}s")
    print("\nDonnées prêtes pour upload vers Cloudflare KV!")

if __name__ == "__main__":
    main()