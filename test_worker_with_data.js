// Test Worker avec données intégrées
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Données d'exemple intégrées
    const SAMPLE_CITIES = {
      "75001": {"name": "Paris 1er", "prix_m2_appartement": 12500, "evolution_1y": 3.2, "volume_2024": 245},
      "75008": {"name": "Paris 8ème", "prix_m2_appartement": 11250, "evolution_1y": 3.5, "volume_2024": 487},
      "69001": {"name": "Lyon 1er", "prix_m2_appartement": 4800, "evolution_1y": 4.1, "volume_2024": 312},
      "13001": {"name": "Marseille 1er", "prix_m2_appartement": 3200, "evolution_1y": 2.8, "volume_2024": 198},
      "33000": {"name": "Bordeaux", "prix_m2_appartement": 4500, "evolution_1y": 5.2, "volume_2024": 567},
      "59000": {"name": "Lille", "prix_m2_appartement": 3400, "evolution_1y": 3.9, "volume_2024": 423},
      "31000": {"name": "Toulouse", "prix_m2_appartement": 3700, "evolution_1y": 4.5, "volume_2024": 389},
      "06000": {"name": "Nice", "prix_m2_appartement": 5800, "evolution_1y": 2.1, "volume_2024": 298},
      "44000": {"name": "Nantes", "prix_m2_appartement": 3900, "evolution_1y": 6.2, "volume_2024": 445},
      "67000": {"name": "Strasbourg", "prix_m2_appartement": 3600, "evolution_1y": 3.3, "volume_2024": 367}
    };

    // Homepage
    if (path === '/') {
      const citiesList = Object.entries(SAMPLE_CITIES).map(([code, data]) => `
        <div class="city-card">
          <h3><a href="/ville/${code}">${data.name}</a></h3>
          <div class="price">${data.prix_m2_appartement.toLocaleString('fr-FR')} €/m²</div>
          <div class="evolution ${data.evolution_1y > 0 ? 'positive' : 'negative'}">
            ${data.evolution_1y > 0 ? '↑' : '↓'} ${Math.abs(data.evolution_1y)}%
          </div>
          <div class="volume">${data.volume_2024} ventes en 2024</div>
        </div>
      `).join('');

      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ImmoStats - Statistiques Immobilières France</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f9fafb;
      color: #111827;
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 3rem 1rem;
      text-align: center;
    }
    h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .subtitle { opacity: 0.9; }
    .container {
      max-width: 1200px;
      margin: 2rem auto;
      padding: 0 1rem;
    }
    .stats-bar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin: 2rem 0;
      padding: 1.5rem;
      background: white;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stat-item {
      text-align: center;
    }
    .stat-value {
      font-size: 2rem;
      font-weight: bold;
      color: #2563eb;
    }
    .stat-label {
      font-size: 0.875rem;
      color: #6b7280;
      margin-top: 0.25rem;
    }
    .cities-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.5rem;
      margin-top: 2rem;
    }
    .city-card {
      background: white;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .city-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .city-card h3 { margin-bottom: 1rem; }
    .city-card a {
      color: #2563eb;
      text-decoration: none;
    }
    .city-card a:hover { text-decoration: underline; }
    .price {
      font-size: 1.5rem;
      font-weight: bold;
      margin: 0.5rem 0;
    }
    .evolution { font-size: 0.875rem; margin: 0.25rem 0; }
    .evolution.positive { color: #10b981; }
    .evolution.negative { color: #ef4444; }
    .volume {
      font-size: 0.875rem;
      color: #6b7280;
      margin-top: 0.5rem;
    }
  </style>
</head>
<body>
  <header class="header">
    <h1>ImmoStats France</h1>
    <p class="subtitle">Analyse du marché immobilier français - Données DVF 2024</p>
  </header>

  <div class="container">
    <div class="stats-bar">
      <div class="stat-item">
        <div class="stat-value">${Object.keys(SAMPLE_CITIES).length}</div>
        <div class="stat-label">Villes analysées</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">4 850 €/m²</div>
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

    <h2>Principales villes de France</h2>
    <div class="cities-grid">
      ${citiesList}
    </div>
  </div>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Page ville
    if (path.startsWith('/ville/')) {
      const code = path.split('/')[2];
      const city = SAMPLE_CITIES[code];

      if (!city) {
        return new Response('Ville non trouvée', { status: 404 });
      }

      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>${city.name} - ImmoStats</title>
  <style>
    body { font-family: system-ui; margin: 0; background: #f5f5f5; }
    .header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; }
    .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
    .back { color: white; text-decoration: none; opacity: 0.8; }
    .back:hover { opacity: 1; }
    h1 { margin: 0.5rem 0; }
    .price-hero { font-size: 3rem; font-weight: bold; margin: 1rem 0; }
    .evolution { font-size: 1.25rem; }
    .positive { color: #34d399; }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1rem;
      margin: 2rem 0;
    }
    .stat-card {
      background: white;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stat-label {
      color: #6b7280;
      font-size: 0.875rem;
      text-transform: uppercase;
      margin-bottom: 0.5rem;
    }
    .stat-value {
      font-size: 2rem;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <header class="header">
    <div class="container">
      <a href="/" class="back">← Retour</a>
      <h1>${city.name}</h1>
      <div class="price-hero">${city.prix_m2_appartement.toLocaleString('fr-FR')} €/m²</div>
      <div class="evolution ${city.evolution_1y > 0 ? 'positive' : 'negative'}">
        ${city.evolution_1y > 0 ? '↑' : '↓'} ${Math.abs(city.evolution_1y)}% sur 1 an
      </div>
    </div>
  </header>

  <div class="container">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Volume 2024</div>
        <div class="stat-value">${city.volume_2024}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Prix médian appartement</div>
        <div class="stat-value">${(city.prix_m2_appartement * 70).toLocaleString('fr-FR')} €</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Surface moyenne</div>
        <div class="stat-value">70 m²</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Délai de vente</div>
        <div class="stat-value">45 jours</div>
      </div>
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