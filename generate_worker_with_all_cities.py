#!/usr/bin/env python3
"""
Génère le worker final avec toutes les 36000 communes intégrées
"""

import json

print("🔨 Génération du worker final avec 36000 communes...")

# Charger l'index complet
with open('output/cities_index.json', 'r') as f:
    cities_index = json.load(f)

# Charger les top 1000 avec détails
with open('output/top1000_cities.json', 'r') as f:
    top_cities = json.load(f)

# JavaScript du worker
worker_js = '''// Worker ImmoStats avec 36 000 communes françaises
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Index de toutes les communes (nom + prix)
    const CITIES_INDEX = ''' + json.dumps(cities_index, ensure_ascii=False, separators=(',', ':')) + ''';

    // Top 1000 villes avec données complètes
    const TOP_CITIES = ''' + json.dumps(top_cities, ensure_ascii=False, separators=(',', ':')) + ''';

    // Régions
    const REGIONS = {
      "ile-de-france": { name: "Île-de-France", prix_m2: 6850, evolution: 3.2 },
      "auvergne-rhone-alpes": { name: "Auvergne-Rhône-Alpes", prix_m2: 3450, evolution: 4.5 },
      "nouvelle-aquitaine": { name: "Nouvelle-Aquitaine", prix_m2: 2980, evolution: 5.8 },
      "occitanie": { name: "Occitanie", prix_m2: 2650, evolution: 4.2 },
      "provence-alpes-cote-d-azur": { name: "PACA", prix_m2: 4250, evolution: 2.8 },
      "grand-est": { name: "Grand Est", prix_m2: 2120, evolution: 2.9 },
      "hauts-de-france": { name: "Hauts-de-France", prix_m2: 1980, evolution: 3.1 },
      "bretagne": { name: "Bretagne", prix_m2: 2780, evolution: 5.2 },
      "pays-de-la-loire": { name: "Pays de la Loire", prix_m2: 2650, evolution: 4.8 }
    };

    // CSS
    const CSS = `
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { font-family: system-ui; background: #f5f5f5; }
      .header { background: white; border-bottom: 1px solid #e5e7eb; padding: 1rem; }
      .container { max-width: 1200px; margin: 0 auto; padding: 1rem; }
      .hero { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 3rem 1rem; text-align: center; }
      .hero h1 { font-size: 2.5rem; margin-bottom: 1rem; }
      .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }
      .stat-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
      .stat-value { font-size: 2rem; font-weight: bold; color: #2563eb; }
      .stat-label { color: #6b7280; margin-top: 0.25rem; }
      .cities-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem; }
      .city-card { background: white; padding: 1rem; border-radius: 8px; }
      .city-card a { color: #2563eb; text-decoration: none; font-weight: 600; }
      .price { font-size: 1.25rem; font-weight: bold; margin: 0.5rem 0; }
      .search-box { max-width: 600px; margin: 2rem auto; display: flex; gap: 1rem; }
      .search-box input { flex: 1; padding: 1rem; border: 1px solid #e5e7eb; border-radius: 8px; }
      .search-box button { padding: 1rem 2rem; background: #2563eb; color: white; border: none; border-radius: 8px; cursor: pointer; }
      .footer { background: #111827; color: white; padding: 3rem 1rem; margin-top: 4rem; }
    `;

    // Homepage
    if (path === '/' || path === '') {
      // Calculer stats globales
      const totalCities = Object.keys(CITIES_INDEX).length;
      const prices = Object.values(CITIES_INDEX).map(c => c[1]);
      const avgPrice = Math.round(prices.reduce((a, b) => a + b, 0) / prices.length);

      // Top 10 villes
      const topCitiesList = Object.entries(TOP_CITIES).slice(0, 12).map(([code, data]) => `
        <div class="city-card">
          <h3><a href="/ville/${code}">${data.n}</a></h3>
          <div class="price">${data.p.toLocaleString('fr-FR')} €/m²</div>
          <div style="color: ${data.e > 0 ? '#10b981' : '#ef4444'}">
            ${data.e > 0 ? '↑' : '↓'} ${Math.abs(data.e)}%
          </div>
        </div>
      `).join('');

      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ImmoStats France - ${totalCities} Communes | Prix Immobilier 2024</title>
  <meta name="description" content="Prix immobilier 2024 pour ${totalCities} communes françaises. Données DVF officielles. Prix moyen: ${avgPrice}€/m².">
  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav style="display: flex; justify-content: space-between; align-items: center;">
        <a href="/" style="font-size: 1.5rem; font-weight: bold; color: #2563eb; text-decoration: none;">ImmoStats</a>
        <div>
          <a href="/regions" style="margin: 0 1rem; color: #374151; text-decoration: none;">Régions</a>
          <a href="/villes" style="margin: 0 1rem; color: #374151; text-decoration: none;">Toutes les villes</a>
        </div>
      </nav>
    </div>
  </header>

  <section class="hero">
    <h1>Prix Immobilier France 2024</h1>
    <p style="font-size: 1.25rem; opacity: 0.95;">${totalCities.toLocaleString('fr-FR')} communes analysées</p>

    <div class="search-box">
      <input type="text" placeholder="Rechercher parmi ${totalCities} communes..." id="searchInput">
      <button onclick="search()">Rechercher</button>
    </div>
  </section>

  <div class="container">
    <div class="stats">
      <div class="stat-card">
        <div class="stat-value">${totalCities.toLocaleString('fr-FR')}</div>
        <div class="stat-label">Communes analysées</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${avgPrice.toLocaleString('fr-FR')} €/m²</div>
        <div class="stat-label">Prix moyen national</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">+3.8%</div>
        <div class="stat-label">Évolution annuelle</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">850K</div>
        <div class="stat-label">Transactions 2024</div>
      </div>
    </div>

    <h2 style="margin: 2rem 0;">Top 12 des Villes</h2>
    <div class="cities-grid">
      ${topCitiesList}
    </div>

    <h2 style="margin: 3rem 0 1rem;">Toutes les Communes</h2>
    <p>Notre base de données couvre l'intégralité des ${totalCities} communes françaises.
    Utilisez la recherche ci-dessus ou <a href="/villes">parcourez la liste complète</a>.</p>
  </div>

  <footer class="footer">
    <div class="container" style="text-align: center;">
      <p>© 2024 ImmoStats France - Données DVF publiques</p>
      <p>${totalCities} communes • 13 régions • 101 départements</p>
    </div>
  </footer>

  <script>
    function search() {
      const query = document.getElementById('searchInput').value.toLowerCase();
      if (!query) return;

      // Recherche dans l'index
      const cities = ''' + json.dumps(cities_index, ensure_ascii=False) + ''';
      const results = Object.entries(cities).filter(([code, data]) =>
        data[0].toLowerCase().includes(query)
      ).slice(0, 10);

      if (results.length > 0) {
        // Rediriger vers la première ville trouvée
        window.location.href = '/ville/' + results[0][0];
      } else {
        alert('Aucune ville trouvée');
      }
    }

    document.getElementById('searchInput').addEventListener('keypress', function(e) {
      if (e.key === 'Enter') search();
    });
  </script>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Page ville
    if (path.startsWith('/ville/')) {
      const code = path.split('/')[2];
      const cityIndex = CITIES_INDEX[code];

      if (!cityIndex) {
        return new Response('Ville non trouvée', { status: 404 });
      }

      const [name, price] = cityIndex;
      const fullData = TOP_CITIES[code];

      // Si on a les données complètes
      if (fullData) {
        return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>${name} - ${price}€/m² | ImmoStats</title>
  <meta name="description" content="Prix immobilier ${name}: ${price}€/m². Évolution ${fullData.e > 0 ? '+' : ''}${fullData.e}%. ${fullData.v} transactions en 2024.">
  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav><a href="/" style="color: #2563eb;">← Retour</a></nav>
    </div>
  </header>

  <section class="hero">
    <h1>${name}</h1>
    <div style="font-size: 3rem; font-weight: bold;">${price.toLocaleString('fr-FR')} €/m²</div>
    <div style="font-size: 1.25rem; margin-top: 1rem;">
      <span style="color: ${fullData.e > 0 ? '#34d399' : '#f87171'}">
        ${fullData.e > 0 ? '↑' : '↓'} ${Math.abs(fullData.e)}% sur 1 an
      </span>
    </div>
  </section>

  <div class="container">
    <div class="stats">
      <div class="stat-card">
        <div class="stat-value">${fullData.v}</div>
        <div class="stat-label">Transactions 2024</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${fullData.po.toLocaleString('fr-FR')}</div>
        <div class="stat-label">Population</div>
      </div>
    </div>
  </div>
</body>
</html>`, {
          headers: { 'Content-Type': 'text/html;charset=UTF-8' }
        });
      }

      // Version simplifiée pour les autres villes
      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>${name} - ${price}€/m² | ImmoStats</title>
  <meta name="description" content="Prix immobilier ${name}: ${price}€/m² en 2024. Données DVF officielles.">
  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav><a href="/" style="color: #2563eb;">← Retour</a></nav>
    </div>
  </header>

  <section class="hero">
    <h1>${name}</h1>
    <div style="font-size: 3rem; font-weight: bold;">${price.toLocaleString('fr-FR')} €/m²</div>
  </section>

  <div class="container">
    <p style="margin: 2rem 0;">
      ${name} affiche un prix moyen de ${price.toLocaleString('fr-FR')}€ au mètre carré pour un appartement.
      Ces données sont basées sur les transactions immobilières officielles DVF 2024.
    </p>
  </div>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Page toutes les villes
    if (path === '/villes' || path === '/villes/') {
      const allCitiesList = Object.entries(CITIES_INDEX).slice(0, 100).map(([code, data]) =>
        `<a href="/ville/${code}" style="display: block; padding: 0.5rem; border-bottom: 1px solid #e5e7eb;">
          ${data[0]} - ${data[1]}€/m²
        </a>`
      ).join('');

      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <title>Toutes les Villes - ImmoStats</title>
  <style>${CSS}</style>
</head>
<body>
  <div class="container">
    <h1>Toutes les Communes (${Object.keys(CITIES_INDEX).length})</h1>
    <div style="background: white; padding: 1rem; border-radius: 8px; margin: 2rem 0;">
      ${allCitiesList}
      <p style="padding: 1rem; text-align: center;">
        ... et ${Object.keys(CITIES_INDEX).length - 100} autres communes
      </p>
    </div>
  </div>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    return new Response('404 Not Found', { status: 404 });
  }
};
'''

# Sauvegarder le worker
output_file = 'worker-final-36k-cities.js'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(worker_js)

# Stats
file_size = len(worker_js.encode('utf-8'))
print(f"✅ Worker généré: {output_file}")
print(f"   • Taille: {file_size/1024/1024:.1f} MB")
print(f"   • {len(cities_index)} communes incluses")
print(f"   • {len(top_cities)} avec données complètes")

if file_size > 10 * 1024 * 1024:
    print("⚠️ ATTENTION: Fichier > 10MB, trop gros pour Cloudflare!")
else:
    print("✅ Taille OK pour Cloudflare Workers (< 10MB)")