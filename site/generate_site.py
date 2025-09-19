#!/usr/bin/env python3
"""
Génère le site statique local avec toutes les communes
"""

import json
import os
from pathlib import Path

print("🔨 Génération du site statique local...")

# Créer structure des dossiers
os.makedirs('site/ville', exist_ok=True)
os.makedirs('site/css', exist_ok=True)
os.makedirs('site/js', exist_ok=True)
os.makedirs('site/data', exist_ok=True)

# Charger les données
with open('../output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

with open('../output/top1000_cities.json', 'r') as f:
    top_cities = json.load(f)

# CSS commun
css_content = """
* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
    --primary: #2563eb;
    --primary-dark: #1e40af;
    --success: #10b981;
    --danger: #ef4444;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-500: #6b7280;
    --gray-700: #374151;
    --gray-900: #111827;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--gray-50);
    color: var(--gray-900);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.header {
    background: white;
    border-bottom: 1px solid var(--gray-200);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
    text-decoration: none;
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-links a {
    color: var(--gray-700);
    text-decoration: none;
    transition: color 0.2s;
}

.nav-links a:hover {
    color: var(--primary);
}

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 0;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.5rem;
    opacity: 0.95;
    margin-bottom: 2rem;
}

.search-box {
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    gap: 1rem;
}

.search-box input {
    flex: 1;
    padding: 1rem;
    font-size: 1rem;
    border: none;
    border-radius: 0.5rem;
}

.search-box button {
    padding: 1rem 2rem;
    background: var(--primary-dark);
    color: white;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: 600;
}

.stats-bar {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: -2rem 0 3rem 0;
    padding: 1.5rem;
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.stat-item {
    text-align: center;
    padding: 1rem;
}

.stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: var(--primary);
}

.stat-label {
    font-size: 0.875rem;
    color: var(--gray-500);
    margin-top: 0.25rem;
}

.cities-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.city-card {
    background: white;
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    transition: all 0.2s;
}

.city-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.city-card h3 {
    margin-bottom: 0.5rem;
}

.city-card a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
}

.price {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0.5rem 0;
}

.evolution {
    font-size: 0.875rem;
}

.positive { color: var(--success); }
.negative { color: var(--danger); }

.volume {
    font-size: 0.875rem;
    color: var(--gray-500);
    margin-top: 0.5rem;
}

.footer {
    background: var(--gray-900);
    color: white;
    padding: 3rem 0;
    margin-top: 4rem;
    text-align: center;
}

.footer p {
    margin: 0.5rem 0;
    color: var(--gray-400);
}

h2 {
    font-size: 2rem;
    margin: 3rem 0 1.5rem 0;
    text-align: center;
}

.section {
    margin: 3rem 0;
}

.content-block {
    background: white;
    padding: 2rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}

@media (max-width: 768px) {
    .hero h1 { font-size: 2rem; }
    .stats-bar { grid-template-columns: 1fr; }
    .search-box { flex-direction: column; }
}
"""

with open('site/css/style.css', 'w') as f:
    f.write(css_content)

# JavaScript pour la recherche
js_content = """
// Données des villes
const citiesData = """ + json.dumps(cities_index, ensure_ascii=False) + """;

function search() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    if (!query) return;

    const results = Object.entries(citiesData).filter(([code, data]) =>
        data[0].toLowerCase().includes(query)
    );

    if (results.length > 0) {
        // Rediriger vers la première ville trouvée
        window.location.href = '/ville/' + results[0][0] + '.html';
    } else {
        alert('Aucune ville trouvée');
    }
}

function searchLive() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const resultsDiv = document.getElementById('searchResults');

    if (!query) {
        resultsDiv.innerHTML = '';
        resultsDiv.style.display = 'none';
        return;
    }

    const results = Object.entries(citiesData).filter(([code, data]) =>
        data[0].toLowerCase().includes(query)
    ).slice(0, 10);

    if (results.length > 0) {
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = results.map(([code, data]) =>
            `<a href="/ville/${code}.html" class="search-result">
                ${data[0]} - ${data[1]}€/m²
            </a>`
        ).join('');
    } else {
        resultsDiv.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', searchLive);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') search();
        });
    }
});
"""

with open('site/js/search.js', 'w') as f:
    f.write(js_content)

# Sauvegarder les données pour JavaScript
with open('site/data/cities.json', 'w') as f:
    json.dump(cities_index, f, ensure_ascii=False, separators=(',', ':'))

# Générer la homepage
total_cities = len(cities_index)
prices = [c[1] for c in cities_index.values()]
avg_price = round(sum(prices) / len(prices))

# Top 12 villes
top_cities_html = ''
for code, data in list(top_cities.items())[:12]:
    top_cities_html += f'''
    <div class="city-card">
        <h3><a href="ville/{code}.html">{data['n']}</a></h3>
        <div class="price">{data['p']:,} €/m²</div>
        <div class="evolution {'positive' if data['e'] > 0 else 'negative'}">
            {'↑' if data['e'] > 0 else '↓'} {abs(data['e'])}%
        </div>
        <div class="volume">{data['v']} ventes en 2024</div>
    </div>'''

homepage_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImmoStats France - {total_cities:,} Communes | Prix Immobilier 2024</title>
    <meta name="description" content="Prix immobilier 2024 pour {total_cities:,} communes françaises. Prix moyen: {avg_price}€/m². Données DVF officielles.">
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
            <p class="hero-subtitle">{total_cities:,} communes analysées</p>

            <div class="search-box">
                <input type="text" placeholder="Rechercher parmi {total_cities:,} communes..." id="searchInput">
                <button onclick="search()">Rechercher</button>
            </div>
            <div id="searchResults" style="display: none; background: white; border-radius: 0.5rem; margin-top: 1rem; max-width: 600px; margin: 1rem auto;"></div>
        </div>
    </section>

    <div class="container">
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">{total_cities:,}</div>
                <div class="stat-label">Communes analysées</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{avg_price:,} €/m²</div>
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
            <h2>Top 12 des Villes par Prix au m²</h2>
            <div class="cities-grid">
                {top_cities_html}
            </div>
        </section>

        <section class="content-block">
            <h2>Le Marché Immobilier Français en 2024</h2>
            <p>
                Avec {total_cities:,} communes analysées, ImmoStats offre la vue la plus complète
                du marché immobilier français. Le prix moyen national s'établit à {avg_price:,}€/m²
                avec des disparités importantes selon les régions et la taille des villes.
            </p>
            <p>
                Les données sont basées sur les transactions officielles DVF (Demandes de Valeurs Foncières)
                publiées par l'État, garantissant une transparence totale sur les prix réels du marché.
            </p>
        </section>
    </div>

    <footer class="footer">
        <div class="container">
            <p>© 2024 ImmoStats France - Données DVF publiques</p>
            <p>{total_cities:,} communes • 13 régions • 101 départements</p>
        </div>
    </footer>

    <script src="js/search.js"></script>
</body>
</html>"""

with open('site/index.html', 'w', encoding='utf-8') as f:
    f.write(homepage_html)

print(f"✅ Homepage créée")

# Générer pages pour top 100 villes
count = 0
for code, data in list(top_cities.items())[:100]:
    city_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['n']} ({code}) - {data['p']}€/m² | ImmoStats</title>
    <meta name="description" content="Prix immobilier {data['n']}: {data['p']}€/m². Évolution {'+' if data['e'] > 0 else ''}{data['e']}%. {data['v']} transactions en 2024.">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="nav">
                <a href="../index.html" class="logo">ImmoStats</a>
                <div class="nav-links">
                    <a href="../index.html">Accueil</a>
                </div>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>{data['n']}</h1>
            <div style="font-size: 3rem; font-weight: bold; margin: 1rem 0;">
                {data['p']:,} €/m²
            </div>
            <div style="font-size: 1.25rem;">
                <span class="{'positive' if data['e'] > 0 else 'negative'}">
                    {'↑' if data['e'] > 0 else '↓'} {abs(data['e'])}% sur 1 an
                </span>
            </div>
        </div>
    </section>

    <div class="container">
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">{data['v']}</div>
                <div class="stat-label">Transactions 2024</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{data.get('po', 0):,}</div>
                <div class="stat-label">Population</div>
            </div>
        </div>

        <section class="content-block">
            <h2>Marché Immobilier à {data['n']}</h2>
            <p>
                {data['n']} affiche un prix moyen de {data['p']:,}€ au mètre carré pour un appartement.
                Avec {data['v']} transactions enregistrées en 2024, le marché reste {'dynamique' if data['v'] > 50 else 'stable'}.
                L'évolution sur un an de {'+' if data['e'] > 0 else ''}{data['e']}% {'témoigne d une croissance soutenue' if data['e'] > 0 else 'indique une stabilisation des prix'}.
            </p>
        </section>
    </div>

    <footer class="footer">
        <div class="container">
            <p>© 2024 ImmoStats France</p>
        </div>
    </footer>
</body>
</html>"""

    with open(f'site/ville/{code}.html', 'w', encoding='utf-8') as f:
        f.write(city_html)
    count += 1

print(f"✅ {count} pages de villes créées")

# Créer un serveur Python simple
server_py = """#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir('site')
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🚀 Serveur démarré sur http://localhost:{PORT}")
    print("   Appuyez sur Ctrl+C pour arrêter")
    httpd.serve_forever()
"""

with open('serve.py', 'w') as f:
    f.write(server_py)

print("\n" + "="*60)
print("✅ Site statique créé avec succès!")
print(f"   • {total_cities:,} communes indexées")
print(f"   • {count} pages de villes créées")
print(f"   • Prix moyen: {avg_price:,}€/m²")
print("\n📁 Structure:")
print("   site/")
print("   ├── index.html")
print("   ├── css/style.css")
print("   ├── js/search.js")
print("   ├── data/cities.json")
print("   └── ville/ (100 pages)")
print("\n🚀 Pour lancer le site:")
print("   python3 serve.py")
print("   Puis ouvrir http://localhost:8000")