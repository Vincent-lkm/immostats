// Cloudflare Worker - ImmoStats France
// Deploy: wrangler deploy

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Router principal
    if (path === '/') {
      return handleHomepage(env);
    } else if (path.startsWith('/ville/')) {
      return handleCityPage(path, env, ctx);
    } else if (path.startsWith('/api/')) {
      return handleAPI(path, env);
    } else if (path.startsWith('/update/')) {
      return handleDataUpdate(request, env);
    } else {
      return serveStaticAsset(path, env);
    }
  }
};

// Page ville avec cache intelligent
async function handleCityPage(path, env, ctx) {
  // Extract city code: /ville/75008/paris-8
  const parts = path.split('/');
  const cityCode = parts[2];

  if (!cityCode) {
    return new Response('Ville non trouvée', { status: 404 });
  }

  // Check cache KV first
  const cacheKey = `city:${cityCode}`;
  const cachedHTML = await env.PAGES_KV.get(cacheKey);

  if (cachedHTML) {
    // Serve from cache with proper headers
    return new Response(cachedHTML, {
      headers: {
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'public, max-age=3600', // 1 hour browser cache
        'X-Cache': 'HIT'
      }
    });
  }

  // Generate page dynamically
  const html = await generateCityPage(cityCode, env);

  // Store in KV for next request (expire in 24h)
  ctx.waitUntil(
    env.PAGES_KV.put(cacheKey, html, {
      expirationTtl: 86400 // 24 hours
    })
  );

  // Track analytics
  ctx.waitUntil(trackPageView(cityCode, env));

  return new Response(html, {
    headers: {
      'Content-Type': 'text/html;charset=UTF-8',
      'Cache-Control': 'public, max-age=3600',
      'X-Cache': 'MISS'
    }
  });
}

// Generate HTML page for city
async function generateCityPage(cityCode, env) {
  // Get stats from KV
  const statsKey = `stats:${cityCode}`;
  const statsJSON = await env.STATS_KV.get(statsKey, 'json');

  if (!statsJSON) {
    // Fallback: compute on the fly from D1
    const stats = await computeStatsFromD1(cityCode, env);
    await env.STATS_KV.put(statsKey, JSON.stringify(stats));
  }

  // Get template from R2
  const template = await env.R2_BUCKET.get('templates/city.html');
  const templateHTML = await template.text();

  // Get city info
  const cityInfo = await getCityInfo(cityCode, env);

  // Generate HTML with real data
  const html = templateHTML
    .replace('{{CITY_NAME}}', cityInfo.name)
    .replace('{{CITY_CODE}}', cityCode)
    .replace('{{PRIX_M2}}', statsJSON.prix_m2_appartement?.toLocaleString('fr-FR') || 'N/A')
    .replace('{{EVOLUTION_1Y}}', statsJSON.evolution_1y || 'N/A')
    .replace('{{VOLUME_2024}}', statsJSON.volume_2024 || 0)
    .replace('{{SURFACE_MOY}}', statsJSON.surface_moyenne || 'N/A')
    .replace('{{CHART_DATA}}', JSON.stringify(statsJSON.chart_data))
    .replace('{{MAP_CENTER}}', JSON.stringify(cityInfo.coordinates))
    .replace('{{TRANSACTIONS_TABLE}}', generateTransactionsTable(statsJSON.recent_transactions))
    .replace('{{LAST_UPDATE}}', new Date(statsJSON.last_update).toLocaleDateString('fr-FR'));

  return html;
}

// API endpoints pour données JSON
async function handleAPI(path, env) {
  const endpoint = path.replace('/api/', '');

  // /api/ville/75008/stats
  if (endpoint.startsWith('ville/')) {
    const cityCode = endpoint.split('/')[1];
    const stats = await env.STATS_KV.get(`stats:${cityCode}`, 'json');

    return new Response(JSON.stringify(stats), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }

  // /api/search?q=paris
  if (endpoint.startsWith('search')) {
    const url = new URL(path);
    const query = url.searchParams.get('q');
    const results = await searchCities(query, env);

    return new Response(JSON.stringify(results), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }

  // /api/national/trends
  if (endpoint === 'national/trends') {
    const trends = await env.STATS_KV.get('national:trends', 'json');
    return new Response(JSON.stringify(trends), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=86400' // 24h
      }
    });
  }

  return new Response('API endpoint not found', { status: 404 });
}

// Update data via webhook (triggered by GitHub Actions)
async function handleDataUpdate(request, env) {
  // Verify webhook secret
  const authHeader = request.headers.get('Authorization');
  if (authHeader !== `Bearer ${env.WEBHOOK_SECRET}`) {
    return new Response('Unauthorized', { status: 401 });
  }

  const data = await request.json();
  const { cities, stats, transactions } = data;

  // Batch update KV store
  const updates = [];

  for (const city of cities) {
    // Update stats in KV
    updates.push(
      env.STATS_KV.put(
        `stats:${city.code}`,
        JSON.stringify(city.stats),
        { expirationTtl: 2592000 } // 30 days
      )
    );

    // Invalidate HTML cache
    updates.push(
      env.PAGES_KV.delete(`city:${city.code}`)
    );
  }

  // Update D1 database with new transactions
  if (transactions && transactions.length > 0) {
    await updateD1Transactions(transactions, env);
  }

  await Promise.all(updates);

  // Update global stats
  await updateNationalStats(env);

  return new Response(JSON.stringify({
    success: true,
    updated_cities: cities.length,
    new_transactions: transactions?.length || 0
  }), {
    headers: { 'Content-Type': 'application/json' }
  });
}

// Homepage avec carte interactive
async function handleHomepage(env) {
  const html = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImmoStats France - Analyse du Marché Immobilier</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <style>
        body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }
        h1 { margin: 0; font-size: 2.5rem; }
        .subtitle { opacity: 0.9; margin-top: 0.5rem; }
        #map { height: 600px; }
        .search-box { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); z-index: 1000; background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .search-input { padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 6px; width: 400px; font-size: 1rem; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; padding: 3rem 2rem; max-width: 1200px; margin: 0 auto; }
        .stat-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .stat-value { font-size: 2rem; font-weight: bold; color: #111827; }
        .stat-label { color: #6b7280; margin-top: 0.5rem; }
    </style>
</head>
<body>
    <header class="header">
        <h1>ImmoStats France</h1>
        <p class="subtitle">Analyse temps réel du marché immobilier - ${await getTotalCities(env)} communes</p>
    </header>

    <div style="position: relative;">
        <div class="search-box">
            <input type="text" class="search-input" placeholder="Rechercher une ville..." id="citySearch">
        </div>
        <div id="map"></div>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">${await getAveragePriceNational(env)} €/m²</div>
            <div class="stat-label">Prix moyen national (appartement)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${await getTotalTransactions2024(env)}</div>
            <div class="stat-label">Transactions en 2024</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">+${await getNationalEvolution(env)}%</div>
            <div class="stat-label">Évolution sur 1 an</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${await getLastUpdateDate(env)}</div>
            <div class="stat-label">Dernière mise à jour</div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const map = L.map('map').setView([46.603354, 1.888334], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        // Load cities data
        fetch('/api/cities/major')
            .then(r => r.json())
            .then(cities => {
                cities.forEach(city => {
                    const color = city.evolution > 0 ? '#10b981' : '#ef4444';
                    L.circleMarker([city.lat, city.lon], {
                        radius: Math.sqrt(city.volume) * 2,
                        color: color,
                        fillOpacity: 0.6
                    }).addTo(map)
                    .bindPopup(\`
                        <b>\${city.name}</b><br>
                        Prix: \${city.prix_m2} €/m²<br>
                        Évolution: \${city.evolution}%<br>
                        <a href="/ville/\${city.code}/\${city.slug}">Voir détails →</a>
                    \`);
                });
            });

        // Search autocomplete
        let searchTimeout;
        document.getElementById('citySearch').addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (e.target.value.length > 2) {
                    fetch(\`/api/search?q=\${e.target.value}\`)
                        .then(r => r.json())
                        .then(showSearchResults);
                }
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

// D1 SQL operations
async function computeStatsFromD1(cityCode, env) {
  const db = env.D1_DATABASE;

  const stats = await db.prepare(`
    SELECT
      AVG(CASE WHEN type_local = 'Appartement' THEN prix_m2 END) as prix_m2_appartement,
      AVG(CASE WHEN type_local = 'Maison' THEN prix_m2 END) as prix_m2_maison,
      COUNT(*) as volume_2024,
      AVG(surface_reelle) as surface_moyenne
    FROM transactions
    WHERE code_postal = ?
    AND date_mutation >= '2024-01-01'
  `).bind(cityCode).first();

  const evolution = await db.prepare(`
    SELECT
      strftime('%Y-%m', date_mutation) as month,
      AVG(prix_m2) as prix_moyen,
      COUNT(*) as volume
    FROM transactions
    WHERE code_postal = ?
    AND date_mutation >= date('now', '-2 years')
    GROUP BY month
    ORDER BY month
  `).bind(cityCode).all();

  return {
    ...stats,
    evolution: evolution.results,
    last_update: new Date().toISOString()
  };
}

// Analytics tracking in D1
async function trackPageView(cityCode, env) {
  const db = env.D1_DATABASE;

  await db.prepare(`
    INSERT INTO analytics (city_code, views, date)
    VALUES (?, 1, date('now'))
    ON CONFLICT(city_code, date)
    DO UPDATE SET views = views + 1
  `).bind(cityCode).run();
}

// City search
async function searchCities(query, env) {
  const db = env.D1_DATABASE;

  const results = await db.prepare(`
    SELECT DISTINCT
      code_postal as code,
      commune as name,
      slug,
      lat, lon
    FROM cities
    WHERE commune LIKE ?
    OR code_postal LIKE ?
    LIMIT 10
  `).bind(`%${query}%`, `${query}%`).all();

  return results.results;
}

// Update D1 with new transactions
async function updateD1Transactions(transactions, env) {
  const db = env.D1_DATABASE;
  const stmt = db.prepare(`
    INSERT OR REPLACE INTO transactions (
      id_mutation, date_mutation, code_postal, commune,
      type_local, surface_reelle, prix, prix_m2, lat, lon
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  const batch = [];
  for (const t of transactions) {
    batch.push(
      stmt.bind(
        t.id_mutation, t.date_mutation, t.code_postal, t.commune,
        t.type_local, t.surface_reelle, t.prix, t.prix_m2, t.lat, t.lon
      )
    );
  }

  await db.batch(batch);
}

// Helper functions
async function getTotalCities(env) {
  const count = await env.STATS_KV.get('global:city_count');
  return parseInt(count || '36000').toLocaleString('fr-FR');
}

async function getAveragePriceNational(env) {
  const price = await env.STATS_KV.get('global:avg_price_m2');
  return parseInt(price || '3500').toLocaleString('fr-FR');
}

async function getTotalTransactions2024(env) {
  const total = await env.STATS_KV.get('global:transactions_2024');
  return parseInt(total || '850000').toLocaleString('fr-FR');
}

async function getNationalEvolution(env) {
  const evolution = await env.STATS_KV.get('global:evolution_1y');
  return evolution || '3.2';
}

async function getLastUpdateDate(env) {
  const date = await env.STATS_KV.get('global:last_update');
  return new Date(date || Date.now()).toLocaleDateString('fr-FR');
}

async function updateNationalStats(env) {
  const db = env.D1_DATABASE;

  const stats = await db.prepare(`
    SELECT
      COUNT(DISTINCT code_postal) as city_count,
      AVG(prix_m2) as avg_price,
      COUNT(*) as total_transactions
    FROM transactions
    WHERE date_mutation >= '2024-01-01'
  `).first();

  await Promise.all([
    env.STATS_KV.put('global:city_count', stats.city_count.toString()),
    env.STATS_KV.put('global:avg_price_m2', Math.round(stats.avg_price).toString()),
    env.STATS_KV.put('global:transactions_2024', stats.total_transactions.toString()),
    env.STATS_KV.put('global:last_update', new Date().toISOString())
  ]);
}

function generateTransactionsTable(transactions) {
  if (!transactions || transactions.length === 0) {
    return '<p>Aucune transaction récente</p>';
  }

  const rows = transactions.map(t => `
    <tr>
      <td>${new Date(t.date).toLocaleDateString('fr-FR')}</td>
      <td><span class="type-badge type-${t.type.toLowerCase()}">${t.type}</span></td>
      <td>${t.surface} m²</td>
      <td>${t.prix.toLocaleString('fr-FR')} €</td>
      <td>${t.prix_m2.toLocaleString('fr-FR')} €</td>
      <td>${t.adresse || 'Non communiquée'}</td>
    </tr>
  `).join('');

  return rows;
}

async function getCityInfo(cityCode, env) {
  const db = env.D1_DATABASE;

  const city = await db.prepare(`
    SELECT commune as name, lat, lon, departement, region
    FROM cities
    WHERE code_postal = ?
  `).bind(cityCode).first();

  return {
    name: city?.name || 'Commune',
    coordinates: [city?.lat || 46.603354, city?.lon || 1.888334],
    department: city?.departement,
    region: city?.region
  };
}

// Serve static assets from R2
async function serveStaticAsset(path, env) {
  const object = await env.R2_BUCKET.get(path.slice(1)); // Remove leading /

  if (!object) {
    return new Response('Not found', { status: 404 });
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set('Cache-Control', 'public, max-age=31536000'); // 1 year for assets

  return new Response(object.body, { headers });
}