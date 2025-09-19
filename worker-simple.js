// Cloudflare Worker SIMPLE - KV Only (pas de D1)
// Deploy: wrangler deploy

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Router
    if (path === '/') {
      return handleHomepage(env);
    } else if (path.startsWith('/ville/')) {
      return handleCityPage(path, env);
    } else if (path.startsWith('/api/')) {
      return handleAPI(path, env);
    } else if (path === '/update') {
      return handleUpdate(request, env);
    }

    return new Response('404 Not Found', { status: 404 });
  }
};

// Homepage simple avec liste des villes
async function handleHomepage(env) {
  // Get top cities from KV
  const topCities = await env.DATA_KV.get('top_cities', 'json') || [];

  const citiesHTML = topCities.map(city => `
    <div class="city-card">
      <h3><a href="/ville/${city.code}/${city.slug}">${city.name}</a></h3>
      <div class="price">${city.prix_m2?.toLocaleString('fr-FR')} €/m²</div>
      <div class="evolution ${city.evolution > 0 ? 'positive' : 'negative'}">
        ${city.evolution > 0 ? '↑' : '↓'} ${Math.abs(city.evolution)}%
      </div>
    </div>
  `).join('');

  const html = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImmoStats France - Prix Immobilier par Ville</title>
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        margin: 0;
        background: #f9fafb;
      }
      .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 1rem;
        text-align: center;
      }
      h1 { margin: 0; font-size: 2.5rem; }
      .subtitle { opacity: 0.9; margin-top: 0.5rem; }
      .container {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 0 1rem;
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
      .city-card h3 {
        margin: 0 0 1rem 0;
      }
      .city-card a {
        color: #2563eb;
        text-decoration: none;
      }
      .city-card a:hover {
        text-decoration: underline;
      }
      .price {
        font-size: 1.5rem;
        font-weight: bold;
        color: #111827;
      }
      .evolution {
        margin-top: 0.5rem;
        font-size: 0.875rem;
      }
      .evolution.positive { color: #10b981; }
      .evolution.negative { color: #ef4444; }
      .search-box {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      }
      .search-input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        font-size: 1rem;
      }
      .stats-banner {
        background: white;
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        text-align: center;
      }
      .stat-item h4 {
        color: #6b7280;
        margin: 0 0 0.5rem 0;
        font-size: 0.875rem;
        text-transform: uppercase;
      }
      .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #111827;
      }
    </style>
</head>
<body>
    <header class="header">
        <h1>ImmoStats France</h1>
        <p class="subtitle">Analyse du marché immobilier - Données DVF 2024</p>
    </header>

    <div class="container">
        <div class="search-box">
            <input
              type="text"
              class="search-input"
              placeholder="Rechercher une ville (ex: Paris, Lyon, 75008)..."
              id="searchInput"
            >
            <div id="searchResults"></div>
        </div>

        <div class="stats-banner">
            <div class="stat-item">
                <h4>Villes Analysées</h4>
                <div class="stat-value">${topCities.length}</div>
            </div>
            <div class="stat-item">
                <h4>Prix Moyen National</h4>
                <div class="stat-value">3 500 €/m²</div>
            </div>
            <div class="stat-item">
                <h4>Évolution 2024</h4>
                <div class="stat-value">+3.2%</div>
            </div>
            <div class="stat-item">
                <h4>Dernière MAJ</h4>
                <div class="stat-value">Aujourd'hui</div>
            </div>
        </div>

        <h2>Top Villes</h2>
        <div class="cities-grid">
            ${citiesHTML}
        </div>
    </div>

    <script>
      // Simple search
      let searchTimeout;
      document.getElementById('searchInput').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value;

        if (query.length < 2) {
          document.getElementById('searchResults').innerHTML = '';
          return;
        }

        searchTimeout = setTimeout(() => {
          fetch(\`/api/search?q=\${query}\`)
            .then(r => r.json())
            .then(results => {
              const html = results.map(r =>
                \`<div><a href="/ville/\${r.code}/\${r.slug}">\${r.name} (\${r.code})</a></div>\`
              ).join('');
              document.getElementById('searchResults').innerHTML = html;
            });
        }, 300);
      });
    </script>
</body>
</html>`;

  return new Response(html, {
    headers: {
      'Content-Type': 'text/html;charset=UTF-8',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}

// Page ville avec données depuis KV
async function handleCityPage(path, env) {
  const parts = path.split('/');
  const cityCode = parts[2];

  if (!cityCode) {
    return new Response('Ville non trouvée', { status: 404 });
  }

  // Get city data from KV
  const cityData = await env.DATA_KV.get(`city:${cityCode}`, 'json');

  if (!cityData) {
    return new Response('Données non disponibles pour cette ville', { status: 404 });
  }

  // Generate charts data
  const evolutionData = cityData.evolution || [];
  const chartLabels = evolutionData.map(e => e.month);
  const chartValues = evolutionData.map(e => e.prix_m2);

  const html = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${cityData.name} - Prix Immobilier ${cityCode} | ImmoStats</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        margin: 0;
        background: #f9fafb;
      }
      .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1rem;
      }
      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
      }
      h1 {
        margin: 0;
        font-size: 2rem;
      }
      .price-hero {
        font-size: 3rem;
        font-weight: bold;
        margin: 1rem 0;
      }
      .evolution {
        font-size: 1.25rem;
      }
      .positive { color: #34d399; }
      .negative { color: #f87171; }
      .content {
        padding: 2rem 0;
      }
      .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
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
        color: #111827;
      }
      .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 2rem 0;
      }
      .chart-wrapper {
        position: relative;
        height: 400px;
      }
      .transactions-table {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        overflow: hidden;
        margin: 2rem 0;
      }
      table {
        width: 100%;
        border-collapse: collapse;
      }
      th {
        background: #f3f4f6;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        color: #374151;
      }
      td {
        padding: 1rem;
        border-top: 1px solid #e5e7eb;
      }
      .back-link {
        color: white;
        text-decoration: none;
        opacity: 0.9;
      }
      .back-link:hover {
        opacity: 1;
      }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <a href="/" class="back-link">← Retour</a>
            <h1>${cityData.name} (${cityCode})</h1>
            <div class="price-hero">${cityData.prix_m2_appartement?.toLocaleString('fr-FR')} €/m²</div>
            <div class="evolution ${cityData.evolution_1y > 0 ? 'positive' : 'negative'}">
                ${cityData.evolution_1y > 0 ? '↑' : '↓'} ${Math.abs(cityData.evolution_1y)}% sur 1 an
            </div>
        </div>
    </header>

    <div class="container content">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Volume 2024</div>
                <div class="stat-value">${cityData.volume_2024 || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Prix Maison</div>
                <div class="stat-value">${cityData.prix_m2_maison?.toLocaleString('fr-FR') || 'N/A'} €/m²</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Surface Moyenne</div>
                <div class="stat-value">${cityData.surface_moyenne || 'N/A'} m²</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Prix Médian Total</div>
                <div class="stat-value">${cityData.prix_median?.toLocaleString('fr-FR') || 'N/A'} €</div>
            </div>
        </div>

        <div class="chart-container">
            <h2>Évolution du Prix au m²</h2>
            <div class="chart-wrapper">
                <canvas id="evolutionChart"></canvas>
            </div>
        </div>

        ${cityData.transactions ? `
        <div class="transactions-table">
            <h2 style="padding: 1.5rem 1.5rem 0;">Dernières Transactions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Type</th>
                        <th>Surface</th>
                        <th>Prix</th>
                        <th>Prix/m²</th>
                    </tr>
                </thead>
                <tbody>
                    ${cityData.transactions.map(t => `
                        <tr>
                            <td>${new Date(t.date).toLocaleDateString('fr-FR')}</td>
                            <td>${t.type}</td>
                            <td>${t.surface} m²</td>
                            <td>${t.prix.toLocaleString('fr-FR')} €</td>
                            <td>${t.prix_m2.toLocaleString('fr-FR')} €</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
        ` : ''}
    </div>

    <script>
      // Evolution chart
      const ctx = document.getElementById('evolutionChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ${JSON.stringify(chartLabels)},
          datasets: [{
            label: 'Prix au m²',
            data: ${JSON.stringify(chartValues)},
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            tension: 0.3,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: function(value) {
                  return value.toLocaleString('fr-FR') + ' €';
                }
              }
            }
          }
        }
      });
    </script>
</body>
</html>`;

  return new Response(html, {
    headers: {
      'Content-Type': 'text/html;charset=UTF-8',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}

// API endpoints
async function handleAPI(path, env) {
  const url = new URL(path);

  // Search API
  if (path.startsWith('/api/search')) {
    const query = url.searchParams.get('q')?.toLowerCase();
    if (!query) {
      return new Response('[]', {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Get all cities list from KV
    const allCities = await env.DATA_KV.get('all_cities', 'json') || [];

    // Simple search
    const results = allCities
      .filter(city =>
        city.name.toLowerCase().includes(query) ||
        city.code.startsWith(query)
      )
      .slice(0, 10);

    return new Response(JSON.stringify(results), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=300'
      }
    });
  }

  // City data API
  if (path.startsWith('/api/ville/')) {
    const cityCode = path.split('/')[3];
    const cityData = await env.DATA_KV.get(`city:${cityCode}`, 'json');

    return new Response(JSON.stringify(cityData || {}), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600'
      }
    });
  }

  return new Response('{"error": "Not found"}', {
    status: 404,
    headers: { 'Content-Type': 'application/json' }
  });
}

// Update endpoint (appelé par GitHub Actions)
async function handleUpdate(request, env) {
  // Vérifier le secret
  const authHeader = request.headers.get('Authorization');
  if (authHeader !== `Bearer ${env.WEBHOOK_SECRET}`) {
    return new Response('Unauthorized', { status: 401 });
  }

  const data = await request.json();

  // Batch update KV
  const updates = [];

  // Update city data
  for (const city of data.cities) {
    updates.push(
      env.DATA_KV.put(
        `city:${city.code}`,
        JSON.stringify(city.data),
        { expirationTtl: 86400 * 30 } // 30 jours
      )
    );
  }

  // Update top cities
  if (data.top_cities) {
    updates.push(
      env.DATA_KV.put('top_cities', JSON.stringify(data.top_cities))
    );
  }

  // Update all cities list
  if (data.all_cities) {
    updates.push(
      env.DATA_KV.put('all_cities', JSON.stringify(data.all_cities))
    );
  }

  await Promise.all(updates);

  return new Response(JSON.stringify({
    success: true,
    updated: data.cities.length,
    timestamp: new Date().toISOString()
  }), {
    headers: { 'Content-Type': 'application/json' }
  });
}