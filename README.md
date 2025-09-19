# 🏠 ImmoStats France

Générateur de site statique d'analyse du marché immobilier français basé sur les données publiques DVF (Demandes de Valeurs Foncières).

## 🎯 Objectif

Créer un site HTML statique avec 36,000+ pages présentant des statistiques immobilières détaillées pour chaque ville de France:
- Prix au m² par type de bien
- Volume de transactions
- Évolution sur 5 ans
- Comparaisons locales
- Cartes interactives

## 📊 Sources de Données

### Principales
- **DVF** (data.gouv.fr): Transactions immobilières 2020-2024
- **BAN**: Géocodage et adresses
- **BDNB**: Base nationale des bâtiments
- **INSEE**: Données socio-démographiques

### APIs Utilisées
```
https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres/
https://adresse.data.gouv.fr/api
https://api-portail.bdnb.io
```

## 🏗️ Architecture

```
immo-stats/
├── data/               # Données brutes DVF
│   ├── raw/           # Fichiers CSV originaux
│   ├── processed/     # Données nettoyées
│   └── stats/         # JSON par ville
├── scripts/           # Pipeline Python
│   ├── download.py    # Télécharge DVF
│   ├── process.py     # Nettoie et enrichit
│   ├── stats.py       # Calcule statistiques
│   └── generate.py    # Génère HTML
├── site/              # Site statique généré
│   ├── index.html     # Carte France
│   ├── ville/         # 36,000 pages villes
│   ├── dept/          # 101 pages départements
│   ├── region/        # 13 pages régions
│   ├── assets/        # CSS, JS, images
│   └── data/          # JSON pour charts
└── templates/         # Templates HTML
```

## 📈 Statistiques Calculées

### Par Ville
- **Prix médian/m²** (appartement, maison, terrain)
- **Volume transactions** annuel et mensuel
- **Évolution prix** (YoY, 3 ans, 5 ans)
- **Surface moyenne** par type de bien
- **Délai moyen** entre mutations
- **Top quartiers** (si applicable)
- **Saisonnalité** des ventes

### Indices Composites
- **Tension immobilière** (0-10)
- **Attractivité** vs moyenne nationale
- **Dynamisme** du marché
- **ROI locatif** estimé

## 🛠️ Stack Technique

```yaml
Pipeline Data:
  - Python 3.11+
  - pandas, numpy
  - requests, aiohttp
  - sqlite3 (cache local)

Générateur Site:
  - Node.js 20+
  - Custom SSG ou 11ty
  - Minification HTML/CSS/JS
  - Image optimization

Visualisations:
  - Chart.js 4.0
  - Leaflet 1.9 (cartes)
  - Simple Statistics

Déploiement:
  - GitHub Actions (build)
  - GitHub Pages ou Netlify
  - CloudFlare CDN
```

## 🚀 Installation

```bash
# Clone repo
git clone https://github.com/[user]/immo-stats.git
cd immo-stats

# Setup Python env
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup Node
npm install

# Download DVF data (400MB)
python scripts/download.py

# Process data
python scripts/process.py

# Generate stats
python scripts/stats.py

# Build site
npm run build

# Preview locally
npm run serve
```

## 📅 Roadmap

### Phase 1 - MVP (En cours)
- [x] Analyse APIs disponibles
- [ ] Pipeline DVF basique
- [ ] Calculs stats principales
- [ ] Générateur 100 villes test
- [ ] Template ville responsive

### Phase 2 - Scale
- [ ] Toutes communes (36,000+)
- [ ] Pages départements/régions
- [ ] Carte France interactive
- [ ] Charts comparatifs
- [ ] Search engine

### Phase 3 - Enrichissement
- [ ] Intégration BDNB
- [ ] Données INSEE
- [ ] Prédictions ML
- [ ] API publique

### Phase 4 - Optimisation
- [ ] Progressive Web App
- [ ] Service Worker
- [ ] Lazy loading
- [ ] SEO avancé

## 📝 Structure Page Ville

```html
/ville/75001/paris-1er/

- Header: Ville, Code Postal, Département
- KPIs: Prix/m², Volume, Évolution
- Chart 1: Évolution prix 5 ans
- Chart 2: Répartition types biens
- Chart 3: Volume mensuel
- Map: Localisation + heat map prix
- Table: Dernières transactions
- Comparaison: Villes similaires
- Footer: Méthodologie, Sources
```

## 🔍 SEO

- **36,000+ pages uniques**
- **Schema.org** RealEstateAgent
- **Sitemap XML** auto-généré
- **Meta** descriptions dynamiques
- **OpenGraph** pour partage
- **URLs** optimisées: `/ville/[cp]/[nom]`

## ⚡ Performance

Objectifs:
- Lighthouse Score: 95+
- Page Load: < 2s
- Time to Interactive: < 3s
- Bundle Size: < 200KB

Techniques:
- HTML statique pré-généré
- Critical CSS inline
- Lazy load charts
- WebP images
- Brotli compression

## 📊 Exemples de Données

```json
{
  "ville": "Paris 1er",
  "code_postal": "75001",
  "stats_2024": {
    "prix_m2": {
      "appartement": 12500,
      "evolution_1an": "+3.2%"
    },
    "volume": {
      "total": 245,
      "appartements": 230,
      "locaux": 15
    },
    "surface_moyenne": {
      "appartement": 65
    }
  }
}
```

## 🤝 Contribution

Les PRs sont bienvenues! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT - Données DVF sous Licence Ouverte 2.0

## 🙏 Credits

- [Data.gouv.fr](https://data.gouv.fr) pour les données DVF
- [Etalab](https://www.etalab.gouv.fr/) pour l'open data
- [DGFIP](https://www.impots.gouv.fr/) source des données

---

*Site généré automatiquement à partir des données publiques DVF. Mise à jour bi-annuelle.*