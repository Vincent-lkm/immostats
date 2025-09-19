# 🔄 Pipeline de Mise à Jour Automatisé

## Architecture Complète

```
┌──────────────────┐     ┌─────────────┐     ┌──────────────┐
│   DVF (API)      │────>│  Pipeline   │────>│  Site Static │
│  Mise à jour     │     │   Python     │     │    HTML      │
│   Bi-annuelle    │     │              │     │              │
└──────────────────┘     └─────────────┘     └──────────────┘
         │                      │                     │
         │                      ▼                     ▼
         │               ┌─────────────┐       ┌──────────┐
         └──────────────>│   SQLite    │       │  GitHub  │
                        │  Historique  │       │  Pages   │
                        └─────────────┘       └──────────┘
```

## 1. Structure des Données

### Base SQLite locale
```sql
-- transactions.db
CREATE TABLE transactions (
    id TEXT PRIMARY KEY,
    date_mutation DATE,
    code_postal TEXT,
    commune TEXT,
    type_local TEXT,
    surface_reelle INTEGER,
    prix INTEGER,
    prix_m2 REAL,
    lat REAL,
    lon REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    batch_id TEXT  -- Pour tracker les imports
);

CREATE TABLE stats_cache (
    city_code TEXT,
    period TEXT,  -- '2024', '2024-Q1', '2024-11'
    stat_type TEXT,  -- 'prix_m2_appart', 'volume', etc
    value REAL,
    calculated_at TIMESTAMP,
    PRIMARY KEY (city_code, period, stat_type)
);

CREATE TABLE update_log (
    batch_id TEXT PRIMARY KEY,
    source_file TEXT,
    rows_imported INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status TEXT
);
```

### Format JSON par ville
```json
{
  "metadata": {
    "city_code": "75008",
    "city_name": "Paris 8ème",
    "last_update": "2024-11-20T10:00:00Z",
    "data_version": "2024.11.20",
    "total_transactions": 487
  },
  "current_stats": {
    "prix_m2_appartement": 11250,
    "prix_m2_maison": 14500,
    "volume_2024": 487,
    "surface_moyenne": 78
  },
  "evolution": {
    "monthly": [
      {"month": "2024-01", "prix_m2": 11000, "volume": 42},
      {"month": "2024-02", "prix_m2": 11050, "volume": 38}
    ],
    "yearly": [
      {"year": 2020, "prix_m2": 10000, "volume": 420},
      {"year": 2021, "prix_m2": 10200, "volume": 445}
    ]
  },
  "transactions_recent": [
    {
      "date": "2024-11-15",
      "type": "appartement",
      "surface": 85,
      "prix": 980000,
      "adresse_hash": "abc123"  // Anonymisé
    }
  ]
}
```

## 2. Scripts Python

### `update_manager.py`
```python
import sqlite3
import pandas as pd
import json
import hashlib
from datetime import datetime
from pathlib import Path
import requests

class DVFUpdateManager:
    def __init__(self):
        self.db = sqlite3.connect('data/transactions.db')
        self.batch_id = datetime.now().strftime('%Y%m%d_%H%M%S')

    def check_for_updates(self):
        """Vérifie si nouvelles données DVF disponibles"""
        # Check data.gouv.fr API pour dernière version
        api_url = "https://www.data.gouv.fr/api/1/datasets/demandes-de-valeurs-foncieres/"
        response = requests.get(api_url)
        latest_update = response.json()['last_update']

        # Compare avec dernière update locale
        cursor = self.db.execute(
            "SELECT MAX(completed_at) FROM update_log WHERE status='success'"
        )
        last_local = cursor.fetchone()[0]

        return latest_update > last_local if last_local else True

    def download_incremental(self):
        """Télécharge seulement les nouvelles données"""
        # Option 1: Si API permet requêtes par date
        params = {
            'date_mutation_min': self.get_last_mutation_date(),
            'date_mutation_max': datetime.now().strftime('%Y-%m-%d')
        }

        # Option 2: Télécharger tout et déduper
        df_new = pd.read_csv('dvf_latest.csv', sep='|')
        existing_ids = self.get_existing_transaction_ids()
        df_new = df_new[~df_new['id_mutation'].isin(existing_ids)]

        return df_new

    def update_stats(self, city_code):
        """Recalcule les stats pour une ville"""
        query = """
        SELECT
            type_local,
            AVG(prix_m2) as prix_moyen,
            COUNT(*) as volume,
            AVG(surface_reelle) as surface_moyenne,
            DATE(date_mutation) as date
        FROM transactions
        WHERE code_postal = ?
        AND date_mutation >= date('now', '-5 years')
        GROUP BY type_local, strftime('%Y-%m', date_mutation)
        """

        df = pd.read_sql(query, self.db, params=[city_code])

        # Calculs additionnels
        stats = {
            'current': df[df.date >= '2024-01-01'].to_dict(),
            'evolution_1y': self.calculate_evolution(df, 1),
            'evolution_5y': self.calculate_evolution(df, 5),
            'seasonality': self.calculate_seasonality(df)
        }

        # Sauvegarder en cache
        self.save_to_cache(city_code, stats)

        return stats

    def generate_json(self, city_code):
        """Génère le JSON pour une ville"""
        stats = self.get_stats_from_cache(city_code)
        transactions = self.get_recent_transactions(city_code, limit=20)

        output = {
            'metadata': {
                'city_code': city_code,
                'last_update': datetime.now().isoformat(),
                'data_version': self.batch_id
            },
            'stats': stats,
            'transactions': transactions
        }

        # Sauvegarder
        output_path = f'site/data/villes/{city_code}.json'
        with open(output_path, 'w') as f:
            json.dump(output, f, ensure_ascii=False)

        return output_path

    def detect_changes(self):
        """Détecte quelles villes ont changé"""
        query = """
        SELECT DISTINCT code_postal
        FROM transactions
        WHERE created_at > (
            SELECT MAX(completed_at)
            FROM update_log
            WHERE status='success'
        )
        """

        changed_cities = pd.read_sql(query, self.db)
        return changed_cities['code_postal'].tolist()

    def regenerate_html(self, city_codes):
        """Régénère seulement les pages modifiées"""
        from html_generator import CityPageGenerator

        generator = CityPageGenerator()
        for city_code in city_codes:
            json_path = f'site/data/villes/{city_code}.json'
            html_path = f'site/ville/{city_code}/index.html'

            generator.generate_page(json_path, html_path)
            print(f"✅ Régénéré: {city_code}")

    def run_update(self):
        """Process complet de mise à jour"""
        print("🔍 Vérification des mises à jour...")

        if not self.check_for_updates():
            print("✅ Données déjà à jour")
            return

        print("📥 Téléchargement des nouvelles données...")
        new_data = self.download_incremental()

        print(f"💾 Import de {len(new_data)} nouvelles transactions...")
        self.import_to_db(new_data)

        print("📊 Mise à jour des statistiques...")
        changed_cities = self.detect_changes()

        for city in changed_cities:
            self.update_stats(city)
            self.generate_json(city)

        print(f"🏗️ Régénération de {len(changed_cities)} pages...")
        self.regenerate_html(changed_cities)

        print("✅ Mise à jour terminée!")
        self.log_update_success(len(new_data), len(changed_cities))

if __name__ == "__main__":
    manager = DVFUpdateManager()
    manager.run_update()
```

## 3. GitHub Actions Workflow

### `.github/workflows/update-data.yml`
```yaml
name: Update Real Estate Data

on:
  schedule:
    # Tous les lundis à 3h du matin
    - cron: '0 3 * * 1'

  workflow_dispatch:  # Permet déclenchement manuel

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
      with:
        token: ${{ secrets.GITHUB_TOKEN }}

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

    - name: Install dependencies
      run: |
        pip install pandas requests sqlite3 jinja2

    - name: Check for updates
      id: check
      run: |
        python scripts/check_updates.py
        echo "::set-output name=has_updates::$(cat .has_updates)"

    - name: Download new data
      if: steps.check.outputs.has_updates == 'true'
      run: python scripts/download_dvf.py

    - name: Update database
      if: steps.check.outputs.has_updates == 'true'
      run: python scripts/update_manager.py

    - name: Generate changed pages
      if: steps.check.outputs.has_updates == 'true'
      run: python scripts/generate_html.py --only-changed

    - name: Optimize assets
      if: steps.check.outputs.has_updates == 'true'
      run: |
        npx terser site/js/*.js -o site/js/
        npx csso site/css/*.css -o site/css/

    - name: Commit changes
      if: steps.check.outputs.has_updates == 'true'
      run: |
        git config user.name "GitHub Actions"
        git config user.email "actions@github.com"
        git add -A
        git commit -m "🔄 Update: $(date +'%Y-%m-%d') - $(cat .stats_summary)"
        git push

    - name: Purge CDN cache
      if: steps.check.outputs.has_updates == 'true'
      run: |
        curl -X POST "https://api.cloudflare.com/client/v4/zones/${{ secrets.CF_ZONE }}/purge_cache" \
          -H "X-Auth-Email: ${{ secrets.CF_EMAIL }}" \
          -H "X-Auth-Key: ${{ secrets.CF_API_KEY }}" \
          -H "Content-Type: application/json" \
          --data '{"purge_everything":false,"files":${{ steps.changed_files }}}'

    - name: Send notification
      if: always()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: |
          Update Data: ${{ job.status }}
          Changed cities: $(cat .changed_cities_count)
          New transactions: $(cat .new_transactions_count)
```

## 4. Versioning et Rollback

### Système de versions
```javascript
// version.json
{
  "current": "2024.11.20.1",
  "previous": "2024.11.13.1",
  "history": [
    {
      "version": "2024.11.20.1",
      "date": "2024-11-20T03:15:00Z",
      "changes": {
        "cities_updated": 1250,
        "new_transactions": 15420,
        "build_time": 320
      }
    }
  ]
}
```

### Script de rollback
```bash
#!/bin/bash
# rollback.sh

VERSION=${1:-"previous"}

echo "🔄 Rolling back to version: $VERSION"

# Restore from backup branch
git checkout backup/$VERSION -- site/
git commit -m "🔙 Rollback to $VERSION"
git push

# Clear CDN
./scripts/purge_cdn.sh

echo "✅ Rollback complete"
```

## 5. Monitoring

### Health check endpoint
```javascript
// /api/health (Vercel function)
export default function handler(req, res) {
  const stats = {
    last_update: getLastUpdateTime(),
    data_version: getCurrentVersion(),
    cities_count: getCitiesCount(),
    total_transactions: getTotalTransactions(),
    update_frequency: "weekly",
    next_update: getNextUpdateTime()
  };

  res.status(200).json(stats);
}
```

### Dashboard de monitoring
```html
<!-- /admin/dashboard.html -->
<div id="update-status">
  <h2>État des Données</h2>
  <div class="metric">
    <span>Dernière MAJ:</span>
    <span id="last-update">20/11/2024 03:15</span>
  </div>
  <div class="metric">
    <span>Prochaine MAJ:</span>
    <span id="next-update">27/11/2024 03:00</span>
  </div>
  <div class="metric">
    <span>Villes à jour:</span>
    <span id="cities-updated">35,847 / 36,000</span>
  </div>
  <button onclick="triggerManualUpdate()">
    Forcer Mise à Jour
  </button>
</div>
```

## 6. Optimisations

### Incrémental Build
- Seulement les villes avec nouvelles transactions
- Diff des stats pour détecter changements
- Cache CDN avec TTL intelligent

### Stratégie de Cache
```nginx
# CDN Rules
/data/*.json         Cache-Control: max-age=86400      # 1 jour
/ville/*/index.html  Cache-Control: max-age=604800     # 1 semaine
/assets/*            Cache-Control: max-age=31536000   # 1 an
```

### Notifications
```javascript
// Webhook Discord/Slack après update
{
  "content": "📊 Mise à jour ImmoStats",
  "embeds": [{
    "title": "Update Complete",
    "fields": [
      {"name": "Nouvelles transactions", "value": "15,420"},
      {"name": "Villes mises à jour", "value": "1,250"},
      {"name": "Temps de build", "value": "5 min 20s"}
    ],
    "color": 0x00ff00
  }]
}
```

---

Cette architecture permet:
✅ Updates automatiques hebdomadaires
✅ Seulement les pages modifiées sont rebuild
✅ Historique complet dans Git
✅ Rollback facile si problème
✅ 100% serverless et gratuit avec GitHub
✅ CDN pour performance optimale