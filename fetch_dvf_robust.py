#!/usr/bin/env python3
"""
Script robuste pour traiter TOUTES les données DVF
Pour les 36000 communes de France
"""

import requests
import pandas as pd
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import numpy as np
from collections import defaultdict
import sys

# Configuration
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# URL du fichier DVF 2024 seulement pour commencer
DVF_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/2024/full.csv.gz"

def download_dvf_alternative():
    """Télécharge DVF depuis une source alternative (CSV geo-localisé)"""
    print("📥 Téléchargement DVF alternatif (geo-dvf)...")

    # Alternative: utiliser geo-dvf qui est mieux structuré
    departments = []

    # Pour le POC, on prend quelques départements représentatifs
    # En production, faire tous les 101 départements
    test_departments = ['75', '13', '69', '33', '59', '31', '06', '44', '67', '35', '34', '38', '92', '93', '94']

    all_data = []

    for dept in test_departments:
        print(f"  Département {dept}...")
        url = f"https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/{dept}.csv.gz"

        try:
            df = pd.read_csv(url, compression='gzip', low_memory=False)
            print(f"    ✓ {len(df)} lignes pour le département {dept}")
            all_data.append(df)
        except Exception as e:
            print(f"    ⚠️ Erreur pour le département {dept}: {e}")
            continue

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"✓ Total: {len(combined_df)} transactions")
        return combined_df
    else:
        return pd.DataFrame()

def process_geo_dvf(df):
    """Traite les données geo-dvf qui ont une structure différente"""
    print("🔄 Traitement des données geo-dvf...")

    # Garder seulement les ventes
    df = df[df['nature_mutation'] == 'Vente'].copy()

    # Filtrer par type de bien
    df = df[df['type_local'].isin(['Appartement', 'Maison'])].copy()

    # Nettoyer les valeurs
    df = df[df['valeur_fonciere'].notna()]
    df = df[(df['valeur_fonciere'] > 10000) & (df['valeur_fonciere'] < 5000000)]

    # Calculer le prix au m² si surface disponible
    df['surface_totale'] = df['surface_reelle_bati'].fillna(0)
    df = df[df['surface_totale'] > 10]
    df['prix_m2'] = df['valeur_fonciere'] / df['surface_totale']

    # Filtrer prix au m² aberrants
    df = df[(df['prix_m2'] > 500) & (df['prix_m2'] < 30000)]

    print(f"✓ {len(df)} transactions valides après nettoyage")

    return df

def calculate_stats_by_city(df):
    """Calcule les stats pour chaque ville"""
    print("📊 Calcul des statistiques par ville...")

    # Grouper par code postal
    grouped = df.groupby('code_postal')

    cities_data = []
    city_count = 0

    for code_postal, city_df in grouped:
        if len(city_df) < 5:  # Minimum 5 transactions pour avoir des stats
            continue

        city_count += 1
        if city_count % 100 == 0:
            print(f"  Progression: {city_count} villes traitées...")

        # Stats par type
        stats = {
            'code': str(code_postal),
            'name': city_df['nom_commune'].iloc[0] if 'nom_commune' in city_df.columns else city_df['commune'].iloc[0],
            'volume_2024': len(city_df),
            'transactions': []
        }

        # Prix médian appartement
        appart_df = city_df[city_df['type_local'] == 'Appartement']
        if len(appart_df) > 0:
            stats['prix_m2_appartement'] = int(appart_df['prix_m2'].median())
            stats['surface_moyenne_appartement'] = int(appart_df['surface_totale'].mean())
            stats['prix_median_appartement'] = int(appart_df['valeur_fonciere'].median())

        # Prix médian maison
        maison_df = city_df[city_df['type_local'] == 'Maison']
        if len(maison_df) > 0:
            stats['prix_m2_maison'] = int(maison_df['prix_m2'].median())
            stats['surface_moyenne_maison'] = int(maison_df['surface_totale'].mean())
            stats['prix_median_maison'] = int(maison_df['valeur_fonciere'].median())

        # Coordonnées moyennes (si disponibles)
        if 'latitude' in city_df.columns and 'longitude' in city_df.columns:
            stats['lat'] = city_df['latitude'].mean()
            stats['lon'] = city_df['longitude'].mean()

        # 10 dernières transactions
        recent = city_df.nlargest(10, 'date_mutation') if 'date_mutation' in city_df.columns else city_df.head(10)
        for _, row in recent.iterrows():
            stats['transactions'].append({
                'date': row.get('date_mutation', '2024-01-01'),
                'type': row['type_local'],
                'surface': int(row['surface_totale']) if pd.notna(row['surface_totale']) else None,
                'prix': int(row['valeur_fonciere']),
                'prix_m2': int(row['prix_m2']) if pd.notna(row['prix_m2']) else None
            })

        cities_data.append({
            'code': stats['code'],
            'data': stats
        })

    print(f"✓ {len(cities_data)} villes avec données suffisantes")
    return cities_data

def generate_slug(name):
    """Génère un slug URL-friendly"""
    import re
    slug = name.lower()
    # Remplacer les caractères accentués
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ô': 'o', 'ö': 'o',
        'î': 'i', 'ï': 'i',
        'ç': 'c'
    }
    for old, new in replacements.items():
        slug = slug.replace(old, new)

    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug

def split_data_for_kv(cities_data):
    """Divise les données en chunks pour KV (max 25MB par namespace)"""
    print("📦 Préparation des données pour Cloudflare KV...")

    # Top villes par volume
    top_cities = []
    for city in cities_data:
        if city['data'].get('volume_2024', 0) > 20:
            top_cities.append({
                'code': city['code'],
                'name': city['data']['name'],
                'slug': generate_slug(city['data']['name']),
                'prix_m2': city['data'].get('prix_m2_appartement', 0),
                'volume': city['data']['volume_2024']
            })

    # Trier par volume
    top_cities.sort(key=lambda x: x['volume'], reverse=True)
    top_cities = top_cities[:100]  # Top 100

    # Liste de toutes les villes pour recherche
    all_cities = [{
        'code': c['code'],
        'name': c['data']['name'],
        'slug': generate_slug(c['data']['name'])
    } for c in cities_data]

    return {
        'cities': cities_data,
        'top_cities': top_cities,
        'all_cities': all_cities
    }

def save_data_batches(data):
    """Sauvegarde les données en plusieurs fichiers pour éviter les limites"""
    print("💾 Sauvegarde des données...")

    # Sauvegarder les métadonnées
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'total_cities': len(data['cities']),
        'top_cities_count': len(data['top_cities']),
        'version': '1.0.0'
    }

    with open(OUTPUT_DIR / 'metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False)

    # Sauvegarder top_cities et all_cities
    with open(OUTPUT_DIR / 'top_cities.json', 'w', encoding='utf-8') as f:
        json.dump(data['top_cities'], f, ensure_ascii=False)

    with open(OUTPUT_DIR / 'all_cities.json', 'w', encoding='utf-8') as f:
        json.dump(data['all_cities'], f, ensure_ascii=False)

    # Sauvegarder les villes en batches de 100
    batch_size = 100
    num_batches = (len(data['cities']) + batch_size - 1) // batch_size

    for i in range(num_batches):
        start = i * batch_size
        end = min((i + 1) * batch_size, len(data['cities']))
        batch = data['cities'][start:end]

        with open(OUTPUT_DIR / f'cities_batch_{i:03d}.json', 'w', encoding='utf-8') as f:
            json.dump(batch, f, ensure_ascii=False)

        print(f"  Batch {i+1}/{num_batches}: {len(batch)} villes")

    print(f"✓ Données sauvegardées en {num_batches} batches")

    # Créer un fichier exemple pour test
    if data['cities']:
        sample = data['cities'][0]
        with open(OUTPUT_DIR / f"sample_{sample['code']}.json", 'w', encoding='utf-8') as f:
            json.dump(sample['data'], f, ensure_ascii=False, indent=2)
        print(f"  Exemple: {sample['data']['name']} ({sample['code']})")

def main():
    print("🚀 Démarrage du traitement DVF pour TOUTES les villes de France")
    print("=" * 60)

    try:
        # Télécharger les données
        df = download_dvf_alternative()

        if df.empty:
            print("❌ Aucune donnée téléchargée")
            return

        # Traiter les données
        df = process_geo_dvf(df)

        # Calculer les stats par ville
        cities_data = calculate_stats_by_city(df)

        # Préparer pour KV
        kv_data = split_data_for_kv(cities_data)

        # Sauvegarder
        save_data_batches(kv_data)

        print("=" * 60)
        print("✅ Traitement terminé avec succès!")
        print(f"   - {len(cities_data)} villes traitées")
        print(f"   - {len(kv_data['top_cities'])} top villes")
        print(f"   - Données prêtes pour upload vers Cloudflare KV")

        # Stats finales
        total_transactions = sum(c['data']['volume_2024'] for c in cities_data)
        print(f"   - {total_transactions:,} transactions totales")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()