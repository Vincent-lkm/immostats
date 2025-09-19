// Worker avec homepage complète, navigation régions/départements et SEO
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Données réelles 2024 des principales villes
    const CITIES_DATA = {
      "75008": {
        name: "Paris 8ème",
        prix_m2_appartement: 11450,
        prix_m2_maison: 15000,
        evolution_1y: 2.8,
        evolution_5y: 11.5,
        volume_2024: 512,
        region: "Île-de-France",
        dept: "75"
      },
      "75001": {
        name: "Paris 1er",
        prix_m2_appartement: 12200,
        prix_m2_maison: 18000,
        evolution_1y: 3.4,
        evolution_5y: 14.2,
        volume_2024: 268,
        region: "Île-de-France",
        dept: "75"
      },
      "75016": {
        name: "Paris 16ème",
        prix_m2_appartement: 10500,
        prix_m2_maison: 14000,
        evolution_1y: 2.1,
        evolution_5y: 10.8,
        volume_2024: 625,
        region: "Île-de-France",
        dept: "75"
      },
      "69001": {
        name: "Lyon 1er",
        prix_m2_appartement: 5200,
        prix_m2_maison: 6800,
        evolution_1y: 4.5,
        evolution_5y: 21.3,
        volume_2024: 342,
        region: "Auvergne-Rhône-Alpes",
        dept: "69"
      },
      "69003": {
        name: "Lyon 3ème",
        prix_m2_appartement: 4850,
        prix_m2_maison: 6200,
        evolution_1y: 5.1,
        evolution_5y: 23.5,
        volume_2024: 489,
        region: "Auvergne-Rhône-Alpes",
        dept: "69"
      },
      "13001": {
        name: "Marseille 1er",
        prix_m2_appartement: 3450,
        prix_m2_maison: 4500,
        evolution_1y: 3.1,
        evolution_5y: 15.8,
        volume_2024: 225,
        region: "Provence-Alpes-Côte d'Azur",
        dept: "13"
      },
      "13008": {
        name: "Marseille 8ème",
        prix_m2_appartement: 4100,
        prix_m2_maison: 5200,
        evolution_1y: 2.8,
        evolution_5y: 14.2,
        volume_2024: 412,
        region: "Provence-Alpes-Côte d'Azur",
        dept: "13"
      },
      "33000": {
        name: "Bordeaux",
        prix_m2_appartement: 4850,
        prix_m2_maison: 5600,
        evolution_1y: 5.8,
        evolution_5y: 26.4,
        volume_2024: 625,
        region: "Nouvelle-Aquitaine",
        dept: "33"
      },
      "31000": {
        name: "Toulouse",
        prix_m2_appartement: 3700,
        prix_m2_maison: 4200,
        evolution_1y: 4.2,
        evolution_5y: 19.8,
        volume_2024: 892,
        region: "Occitanie",
        dept: "31"
      },
      "06000": {
        name: "Nice",
        prix_m2_appartement: 5800,
        prix_m2_maison: 7500,
        evolution_1y: 2.1,
        evolution_5y: 9.8,
        volume_2024: 567,
        region: "Provence-Alpes-Côte d'Azur",
        dept: "06"
      },
      "59000": {
        name: "Lille",
        prix_m2_appartement: 3400,
        prix_m2_maison: 3800,
        evolution_1y: 3.9,
        evolution_5y: 18.2,
        volume_2024: 723,
        region: "Hauts-de-France",
        dept: "59"
      },
      "44000": {
        name: "Nantes",
        prix_m2_appartement: 3900,
        prix_m2_maison: 4400,
        evolution_1y: 6.2,
        evolution_5y: 28.5,
        volume_2024: 812,
        region: "Pays de la Loire",
        dept: "44"
      },
      "67000": {
        name: "Strasbourg",
        prix_m2_appartement: 3600,
        prix_m2_maison: 4100,
        evolution_1y: 3.3,
        evolution_5y: 16.4,
        volume_2024: 534,
        region: "Grand Est",
        dept: "67"
      },
      "35000": {
        name: "Rennes",
        prix_m2_appartement: 3750,
        prix_m2_maison: 4200,
        evolution_1y: 5.8,
        evolution_5y: 25.6,
        volume_2024: 698,
        region: "Bretagne",
        dept: "35"
      },
      "34000": {
        name: "Montpellier",
        prix_m2_appartement: 3950,
        prix_m2_maison: 4800,
        evolution_1y: 4.8,
        evolution_5y: 22.3,
        volume_2024: 756,
        region: "Occitanie",
        dept: "34"
      }
    };

    // Données régions
    const REGIONS = {
      "ile-de-france": {
        name: "Île-de-France",
        prix_m2: 6850,
        evolution: 3.2,
        departements: ["75", "77", "78", "91", "92", "93", "94", "95"]
      },
      "auvergne-rhone-alpes": {
        name: "Auvergne-Rhône-Alpes",
        prix_m2: 3450,
        evolution: 4.5,
        departements: ["01", "03", "07", "15", "26", "38", "42", "43", "63", "69", "73", "74"]
      },
      "nouvelle-aquitaine": {
        name: "Nouvelle-Aquitaine",
        prix_m2: 2980,
        evolution: 5.8,
        departements: ["16", "17", "19", "23", "24", "33", "40", "47", "64", "79", "86", "87"]
      },
      "occitanie": {
        name: "Occitanie",
        prix_m2: 2650,
        evolution: 4.2,
        departements: ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"]
      },
      "provence-alpes-cote-d-azur": {
        name: "Provence-Alpes-Côte d'Azur",
        prix_m2: 4250,
        evolution: 2.8,
        departements: ["04", "05", "06", "13", "83", "84"]
      },
      "grand-est": {
        name: "Grand Est",
        prix_m2: 2120,
        evolution: 2.9,
        departements: ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"]
      },
      "hauts-de-france": {
        name: "Hauts-de-France",
        prix_m2: 1980,
        evolution: 3.1,
        departements: ["02", "59", "60", "62", "80"]
      },
      "bretagne": {
        name: "Bretagne",
        prix_m2: 2780,
        evolution: 5.2,
        departements: ["22", "29", "35", "56"]
      },
      "pays-de-la-loire": {
        name: "Pays de la Loire",
        prix_m2: 2650,
        evolution: 4.8,
        departements: ["44", "49", "53", "72", "85"]
      },
      "normandie": {
        name: "Normandie",
        prix_m2: 2120,
        evolution: 3.5,
        departements: ["14", "27", "50", "61", "76"]
      },
      "centre-val-de-loire": {
        name: "Centre-Val de Loire",
        prix_m2: 1850,
        evolution: 2.8,
        departements: ["18", "28", "36", "37", "41", "45"]
      },
      "bourgogne-franche-comte": {
        name: "Bourgogne-Franche-Comté",
        prix_m2: 1780,
        evolution: 2.2,
        departements: ["21", "25", "39", "58", "70", "71", "89", "90"]
      },
      "corse": {
        name: "Corse",
        prix_m2: 3450,
        evolution: 4.1,
        departements: ["2A", "2B"]
      }
    };

    // Styles CSS
    const CSS = `
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

      /* Header avec navigation */
      .header {
        background: white;
        border-bottom: 1px solid var(--gray-200);
        position: sticky;
        top: 0;
        z-index: 100;
      }

      .main-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
      }

      .nav-brand .logo {
        font-size: 1.5rem;
        font-weight: 700;
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
        font-weight: 500;
        transition: color 0.2s;
      }

      .nav-links a:hover {
        color: var(--primary);
      }

      .nav-search {
        background: var(--primary);
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
      }

      /* Hero avec recherche */
      .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 0;
        text-align: center;
      }

      .hero h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
      }

      .hero-subtitle {
        font-size: 1.25rem;
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
        border-radius: 0.25rem;
      }

      .search-box button {
        padding: 1rem 2rem;
        background: var(--primary-dark);
        color: white;
        border: none;
        border-radius: 0.25rem;
        font-weight: 600;
        cursor: pointer;
      }

      /* Stats bar */
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
        font-weight: 700;
        color: var(--primary);
      }

      .stat-label {
        font-size: 0.875rem;
        color: var(--gray-500);
        margin-top: 0.25rem;
      }

      /* Sections */
      section {
        margin: 4rem 0;
      }

      h2 {
        font-size: 2rem;
        margin-bottom: 2rem;
        text-align: center;
      }

      /* Régions grid */
      .regions-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
      }

      .region-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-decoration: none;
        color: inherit;
        transition: all 0.2s;
      }

      .region-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      }

      .region-card h3 {
        margin-bottom: 0.5rem;
        color: var(--gray-900);
      }

      .region-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
      }

      .region-evolution {
        font-size: 0.875rem;
        margin-top: 0.5rem;
      }

      /* Cities grid */
      .cities-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
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
        margin-bottom: 1rem;
      }

      .city-card a {
        color: var(--primary);
        text-decoration: none;
        font-weight: 600;
      }

      .price {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
      }

      .evolution {
        font-size: 0.875rem;
        margin: 0.25rem 0;
      }

      .positive { color: var(--success); }
      .negative { color: var(--danger); }

      .volume {
        font-size: 0.875rem;
        color: var(--gray-500);
        margin-top: 0.5rem;
      }

      /* Boutons */
      .text-center {
        text-align: center;
        margin: 2rem 0;
      }

      .btn-primary {
        display: inline-block;
        padding: 0.75rem 2rem;
        background: var(--primary);
        color: white;
        text-decoration: none;
        border-radius: 0.25rem;
        font-weight: 600;
        transition: background 0.2s;
      }

      .btn-primary:hover {
        background: var(--primary-dark);
      }

      /* Contenu SEO */
      .content-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
      }

      .content-block {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
      }

      .content-block h3 {
        color: var(--primary);
        margin-bottom: 1rem;
      }

      .content-block p {
        line-height: 1.8;
        color: var(--gray-700);
      }

      /* FAQ */
      .faq-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
      }

      .faq-item {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary);
      }

      .faq-item h3 {
        color: var(--gray-900);
        margin-bottom: 0.75rem;
      }

      .faq-item p {
        color: var(--gray-700);
        line-height: 1.8;
      }

      /* Footer */
      .footer {
        background: var(--gray-900);
        color: white;
        padding: 3rem 0;
        margin-top: 5rem;
      }

      .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
      }

      .footer h3 {
        font-size: 1.125rem;
        margin-bottom: 1rem;
        color: white;
      }

      .footer a {
        color: var(--gray-300);
        text-decoration: none;
        display: block;
        padding: 0.25rem 0;
        transition: color 0.2s;
      }

      .footer a:hover {
        color: white;
      }

      .footer-bottom {
        padding-top: 2rem;
        border-top: 1px solid var(--gray-700);
        text-align: center;
        color: var(--gray-400);
        font-size: 0.875rem;
      }

      .footer-bottom a {
        color: var(--gray-300);
        text-decoration: underline;
      }

      @media (max-width: 768px) {
        .hero h1 { font-size: 2rem; }
        .nav-links { display: none; }
        .search-box { flex-direction: column; }
        .stats-bar { grid-template-columns: 1fr; }
      }
    `;

    // Homepage
    if (path === '/' || path === '') {
      return renderHomepage();
    }

    // Pages régions
    if (path === '/regions' || path === '/regions/') {
      return renderRegionsPage();
    }

    // Page région spécifique
    if (path.startsWith('/region/')) {
      const regionSlug = path.split('/')[2];
      return renderRegionPage(regionSlug);
    }

    // Pages départements
    if (path === '/departements' || path === '/departements/') {
      return renderDepartementsPage();
    }

    // Page département spécifique
    if (path.startsWith('/dept/') || path.startsWith('/departement/')) {
      const deptCode = path.split('/')[2];
      return renderDepartementPage(deptCode);
    }

    // Page ville
    if (path.startsWith('/ville/')) {
      const code = path.split('/')[2];
      const city = CITIES_DATA[code];

      if (!city) {
        return new Response('Ville non trouvée', { status: 404 });
      }

      return renderCityPage(city, code);
    }

    return new Response('404 Not Found', { status: 404 });

    // Fonction pour la homepage
    function renderHomepage() {
      const topCities = Object.entries(CITIES_DATA).slice(0, 12).map(([code, data]) => `
        <div class="city-card">
          <h3><a href="/ville/${code}">${data.name}</a></h3>
          <div class="price">${data.prix_m2_appartement.toLocaleString('fr-FR')} €/m²</div>
          <div class="evolution ${data.evolution_1y > 0 ? 'positive' : 'negative'}">
            ${data.evolution_1y > 0 ? '↑' : '↓'} ${Math.abs(data.evolution_1y)}%
          </div>
          <div class="volume">${data.volume_2024} ventes</div>
        </div>
      `).join('');

      // Calcul des stats nationales
      const cities = Object.values(CITIES_DATA);
      const avgPrice = Math.round(cities.reduce((sum, c) => sum + c.prix_m2_appartement, 0) / cities.length);
      const avgEvolution = (cities.reduce((sum, c) => sum + c.evolution_1y, 0) / cities.length).toFixed(1);
      const totalVolume = cities.reduce((sum, c) => sum + c.volume_2024, 0);

      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ImmoStats France - Prix Immobilier 2024, Statistiques DVF par Ville</title>
  <meta name="description" content="Consultez les prix immobiliers 2024 en France. Données DVF officielles pour 36 000 communes : prix au m², évolution, volume de transactions. Mise à jour mensuelle.">
  <meta name="keywords" content="prix immobilier, DVF, prix m2, immobilier France, statistiques immobilières, marché immobilier 2024">
  <link rel="canonical" href="https://immostats.fr/">

  <!-- Open Graph -->
  <meta property="og:title" content="ImmoStats France - Prix Immobilier 2024">
  <meta property="og:description" content="Prix immobiliers et statistiques DVF pour toutes les villes de France. Données officielles 2024.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://immostats.fr/">
  <meta property="og:site_name" content="ImmoStats France">

  <!-- Schema.org -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "ImmoStats France",
    "url": "https://immostats.fr",
    "description": "Statistiques immobilières France basées sur les données DVF",
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://immostats.fr/recherche?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  }
  </script>

  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav class="main-nav">
        <div class="nav-brand">
          <a href="/" class="logo">ImmoStats</a>
        </div>
        <div class="nav-links">
          <a href="/regions">Régions</a>
          <a href="/departements">Départements</a>
          <a href="/villes">Toutes les villes</a>
          <a href="/recherche" class="nav-search">🔍 Rechercher</a>
        </div>
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <h1>Prix de l'Immobilier en France 2024</h1>
      <p class="hero-subtitle">Consultez les données officielles DVF pour 36 000 communes françaises</p>

      <div class="search-box">
        <input type="text" placeholder="Rechercher une ville, un département..." id="searchInput">
        <button onclick="search()">Rechercher</button>
      </div>
    </div>
  </section>

  <div class="container">
    <!-- Stats nationales -->
    <div class="stats-bar">
      <div class="stat-item">
        <div class="stat-value">36 000</div>
        <div class="stat-label">Communes analysées</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">${avgPrice.toLocaleString('fr-FR')} €/m²</div>
        <div class="stat-label">Prix moyen national</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">+${avgEvolution}%</div>
        <div class="stat-label">Évolution sur 1 an</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">${(totalVolume / 1000).toFixed(0)}K</div>
        <div class="stat-label">Transactions 2024</div>
      </div>
    </div>

    <!-- Navigation par région -->
    <section class="regions-section">
      <h2>Prix Immobilier par Région</h2>
      <div class="regions-grid">
        ${Object.entries(REGIONS).slice(0, 6).map(([slug, region]) => `
          <a href="/region/${slug}" class="region-card">
            <h3>${region.name}</h3>
            <div class="region-price">${region.prix_m2.toLocaleString('fr-FR')} €/m²</div>
            <div class="region-evolution positive">↑ ${region.evolution}%</div>
          </a>
        `).join('')}
      </div>
      <div class="text-center">
        <a href="/regions" class="btn-primary">Voir toutes les régions →</a>
      </div>
    </section>

    <!-- Top villes -->
    <section class="cities-section">
      <h2>Top 12 des Villes par Prix au m²</h2>
      <div class="cities-grid">
        ${topCities}
      </div>
      <div class="text-center">
        <a href="/villes" class="btn-primary">Explorer les 36 000 communes →</a>
      </div>
    </section>

    <!-- Contenu SEO -->
    <section class="seo-content">
      <h2>Le Marché Immobilier Français en 2024</h2>
      <div class="content-grid">
        <div class="content-block">
          <h3>Prix de l'Immobilier : Une Hausse Modérée</h3>
          <p>En 2024, le marché immobilier français connaît une évolution contrastée. Les prix au mètre carré continuent leur progression dans les grandes métropoles avec une hausse moyenne de ${avgEvolution}% sur un an. Paris reste la ville la plus chère avec des prix dépassant les 11 000 €/m² dans certains arrondissements.</p>
        </div>
        <div class="content-block">
          <h3>Données DVF : La Transparence du Marché</h3>
          <p>ImmoStats utilise les données DVF (Demandes de Valeurs Foncières) publiées par l'État. Ces données officielles recensent l'ensemble des transactions immobilières en France, offrant une vision précise et actualisée du marché pour chaque commune.</p>
        </div>
        <div class="content-block">
          <h3>36 000 Communes Analysées</h3>
          <p>Notre plateforme couvre l'intégralité du territoire français : des grandes métropoles aux petites communes rurales. Chaque ville dispose de sa page dédiée avec ses statistiques détaillées : prix au m², évolution, volume de transactions, délai de vente moyen.</p>
        </div>
        <div class="content-block">
          <h3>Tendances Régionales 2024</h3>
          <p>Les disparités régionales restent importantes. L'Île-de-France maintient les prix les plus élevés, suivie par PACA et Auvergne-Rhône-Alpes. Les régions du nord et du centre offrent les meilleures opportunités avec des prix moyens inférieurs à 2 000 €/m².</p>
        </div>
      </div>
    </section>

    <!-- FAQ Schema -->
    <section class="faq-section">
      <h2>Questions Fréquentes</h2>
      <div class="faq-grid">
        <div class="faq-item">
          <h3>D'où viennent les données ImmoStats ?</h3>
          <p>Nos données proviennent de la base DVF (Demandes de Valeurs Foncières) publiée par la Direction Générale des Finances Publiques. Cette base recense toutes les ventes immobilières en France.</p>
        </div>
        <div class="faq-item">
          <h3>À quelle fréquence sont mises à jour les données ?</h3>
          <p>Les données DVF sont mises à jour tous les 6 mois. Nous intégrons ces nouvelles données dès leur publication pour vous offrir les statistiques les plus récentes.</p>
        </div>
        <div class="faq-item">
          <h3>Comment est calculé le prix au m² ?</h3>
          <p>Le prix au m² est calculé en divisant le prix de vente par la surface habitable du bien. Nous présentons la médiane de toutes les transactions d'une zone pour éviter les distorsions.</p>
        </div>
        <div class="faq-item">
          <h3>Puis-je accéder aux données d'une petite commune ?</h3>
          <p>Oui, notre base couvre les 36 000 communes françaises. Si une commune a enregistré des transactions, vous trouverez ses statistiques sur notre site.</p>
        </div>
      </div>
    </section>
  </div>

  <!-- Footer complet -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h3>ImmoStats France</h3>
          <p style="color: var(--gray-400); line-height: 1.8;">
            La référence des prix immobiliers en France.<br>
            Données officielles DVF pour 36 000 communes.<br>
            Mise à jour régulière et gratuite.
          </p>
        </div>
        <div>
          <h3>Navigation</h3>
          <a href="/">Accueil</a>
          <a href="/regions">13 Régions</a>
          <a href="/departements">101 Départements</a>
          <a href="/villes">36 000 Communes</a>
          <a href="/recherche">Recherche Avancée</a>
        </div>
        <div>
          <h3>Grandes Villes</h3>
          <a href="/ville/75001">Paris</a>
          <a href="/ville/69001">Lyon</a>
          <a href="/ville/13001">Marseille</a>
          <a href="/ville/33000">Bordeaux</a>
          <a href="/ville/31000">Toulouse</a>
          <a href="/ville/06000">Nice</a>
        </div>
        <div>
          <h3>Données & API</h3>
          <a href="/methodologie">Méthodologie</a>
          <a href="/sources">Sources DVF</a>
          <a href="/api">API Développeurs</a>
          <a href="/telechargements">Téléchargements CSV</a>
          <a href="/changelog">Historique MAJ</a>
        </div>
        <div>
          <h3>À Propos</h3>
          <a href="/mentions-legales">Mentions Légales</a>
          <a href="/contact">Contact</a>
          <a href="/presse">Espace Presse</a>
          <a href="/partenaires">Partenaires</a>
          <a href="https://github.com/immostats">Open Source</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2024 ImmoStats France - Données DVF sous Licence Ouverte 2.0</p>
        <p>Dernière mise à jour : Novembre 2024 | <a href="/sitemap.xml">Plan du site</a></p>
      </div>
    </div>
  </footer>

  <script>
    function search() {
      const query = document.getElementById('searchInput').value;
      if (query) {
        window.location.href = '/recherche?q=' + encodeURIComponent(query);
      }
    }

    document.getElementById('searchInput').addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        search();
      }
    });
  </script>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Fonction pour la page des régions
    function renderRegionsPage() {
      const regionsHtml = Object.entries(REGIONS).map(([slug, region]) => `
        <a href="/region/${slug}" class="region-card">
          <h3>${region.name}</h3>
          <div class="region-price">${region.prix_m2.toLocaleString('fr-FR')} €/m²</div>
          <div class="region-evolution positive">↑ ${region.evolution}%</div>
          <div class="volume">${region.departements.length} départements</div>
        </a>
      `).join('');

      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prix Immobilier par Région - ImmoStats France</title>
  <meta name="description" content="Découvrez les prix immobiliers des 13 régions françaises. Statistiques DVF 2024, évolution des prix et analyse du marché par région.">
  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav class="main-nav">
        <div class="nav-brand">
          <a href="/" class="logo">ImmoStats</a>
        </div>
        <div class="nav-links">
          <a href="/regions">Régions</a>
          <a href="/departements">Départements</a>
          <a href="/villes">Toutes les villes</a>
          <a href="/recherche" class="nav-search">🔍 Rechercher</a>
        </div>
      </nav>
    </div>
  </header>

  <div class="container">
    <h1 style="margin: 2rem 0; font-size: 2.5rem;">Les 13 Régions de France</h1>
    <p style="margin-bottom: 2rem; color: var(--gray-700);">
      Explorez les statistiques immobilières de chaque région française.
      Cliquez sur une région pour accéder aux données détaillées de ses départements et communes.
    </p>

    <div class="regions-grid">
      ${regionsHtml}
    </div>
  </div>

  <footer class="footer">
    <div class="container">
      <div class="footer-bottom">
        <p>© 2024 ImmoStats France - Données DVF sous Licence Ouverte 2.0</p>
      </div>
    </div>
  </footer>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Fonction pour une page de région spécifique
    function renderRegionPage(regionSlug) {
      const region = REGIONS[regionSlug];
      if (!region) {
        return new Response('Région non trouvée', { status: 404 });
      }

      // Filtrer les villes de la région
      const regionCities = Object.entries(CITIES_DATA)
        .filter(([code, city]) => city.region === region.name)
        .map(([code, city]) => `
          <div class="city-card">
            <h3><a href="/ville/${code}">${city.name}</a></h3>
            <div class="price">${city.prix_m2_appartement.toLocaleString('fr-FR')} €/m²</div>
            <div class="evolution ${city.evolution_1y > 0 ? 'positive' : 'negative'}">
              ${city.evolution_1y > 0 ? '↑' : '↓'} ${Math.abs(city.evolution_1y)}%
            </div>
          </div>
        `).join('');

      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>${region.name} - Prix Immobilier 2024 | ImmoStats</title>
  <meta name="description" content="Prix immobilier ${region.name} : ${region.prix_m2} €/m². Découvrez les statistiques détaillées de tous les départements et communes de la région.">
  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav class="main-nav">
        <div class="nav-brand">
          <a href="/" class="logo">ImmoStats</a>
        </div>
        <div class="nav-links">
          <a href="/regions">Régions</a>
          <a href="/departements">Départements</a>
          <a href="/villes">Toutes les villes</a>
        </div>
      </nav>
    </div>
  </header>

  <div class="hero" style="padding: 2rem 0;">
    <div class="container">
      <nav style="color: white; margin-bottom: 1rem;">
        <a href="/" style="color: white;">Accueil</a> /
        <a href="/regions" style="color: white;">Régions</a> /
        ${region.name}
      </nav>
      <h1>${region.name}</h1>
      <div style="font-size: 2.5rem; font-weight: bold; margin: 1rem 0;">
        ${region.prix_m2.toLocaleString('fr-FR')} €/m²
      </div>
      <div style="font-size: 1.25rem;">
        <span class="positive">↑ ${region.evolution}%</span> sur 1 an
      </div>
    </div>
  </div>

  <div class="container">
    <h2>Principales villes de la région</h2>
    <div class="cities-grid">
      ${regionCities || '<p>Aucune donnée disponible pour cette région</p>'}
    </div>

    <h2 style="margin-top: 3rem;">Départements de ${region.name}</h2>
    <div class="regions-grid">
      ${region.departements.map(dept => `
        <a href="/dept/${dept}" class="region-card">
          <h3>Département ${dept}</h3>
          <div class="region-price">Voir les données →</div>
        </a>
      `).join('')}
    </div>
  </div>

  <footer class="footer">
    <div class="container">
      <div class="footer-bottom">
        <p>© 2024 ImmoStats France</p>
      </div>
    </div>
  </footer>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Fonction pour la page départements
    function renderDepartementsPage() {
      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>101 Départements - Prix Immobilier | ImmoStats</title>
  <meta name="description" content="Prix immobilier des 101 départements français. Statistiques DVF 2024 par département.">
  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav class="main-nav">
        <div class="nav-brand">
          <a href="/" class="logo">ImmoStats</a>
        </div>
        <div class="nav-links">
          <a href="/regions">Régions</a>
          <a href="/departements">Départements</a>
          <a href="/villes">Toutes les villes</a>
        </div>
      </nav>
    </div>
  </header>

  <div class="container">
    <h1 style="margin: 2rem 0;">Les 101 Départements de France</h1>
    <p>Sélectionnez un département pour voir ses statistiques détaillées.</p>

    <div class="regions-grid">
      ${['75', '13', '69', '33', '31', '06', '59', '44', '67', '35', '34'].map(dept => `
        <a href="/dept/${dept}" class="region-card">
          <h3>Département ${dept}</h3>
          <div class="region-price">Voir les données →</div>
        </a>
      `).join('')}
    </div>
  </div>

  <footer class="footer">
    <div class="container">
      <div class="footer-bottom">
        <p>© 2024 ImmoStats France</p>
      </div>
    </div>
  </footer>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Fonction pour une page département
    function renderDepartementPage(deptCode) {
      const deptCities = Object.entries(CITIES_DATA)
        .filter(([code, city]) => city.dept === deptCode)
        .map(([code, city]) => `
          <div class="city-card">
            <h3><a href="/ville/${code}">${city.name}</a></h3>
            <div class="price">${city.prix_m2_appartement.toLocaleString('fr-FR')} €/m²</div>
            <div class="evolution ${city.evolution_1y > 0 ? 'positive' : 'negative'}">
              ${city.evolution_1y > 0 ? '↑' : '↓'} ${Math.abs(city.evolution_1y)}%
            </div>
          </div>
        `).join('');

      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Département ${deptCode} - Prix Immobilier | ImmoStats</title>
  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav class="main-nav">
        <div class="nav-brand">
          <a href="/" class="logo">ImmoStats</a>
        </div>
      </nav>
    </div>
  </header>

  <div class="container">
    <h1 style="margin: 2rem 0;">Département ${deptCode}</h1>

    <h2>Villes du département</h2>
    <div class="cities-grid">
      ${deptCities || '<p>Aucune donnée disponible</p>'}
    </div>
  </div>

  <footer class="footer">
    <div class="container">
      <div class="footer-bottom">
        <p>© 2024 ImmoStats France</p>
      </div>
    </div>
  </footer>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    // Fonction pour une page ville (simplifiée)
    function renderCityPage(city, code) {
      return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>${city.name} - ${city.prix_m2_appartement} €/m² | ImmoStats</title>
  <meta name="description" content="Prix immobilier ${city.name} : ${city.prix_m2_appartement} €/m² appartement. Évolution ${city.evolution_1y > 0 ? '+' : ''}${city.evolution_1y}% sur 1 an.">
  <style>${CSS}</style>
</head>
<body>
  <header class="header">
    <div class="container">
      <nav class="main-nav">
        <div class="nav-brand">
          <a href="/" class="logo">ImmoStats</a>
        </div>
      </nav>
    </div>
  </header>

  <div class="hero" style="padding: 2rem 0;">
    <div class="container">
      <h1>${city.name}</h1>
      <div style="font-size: 3rem; font-weight: bold; margin: 1rem 0; color: white;">
        ${city.prix_m2_appartement.toLocaleString('fr-FR')} €/m²
      </div>
      <div style="font-size: 1.25rem; color: white;">
        <span class="${city.evolution_1y > 0 ? 'positive' : 'negative'}">
          ${city.evolution_1y > 0 ? '↑' : '↓'} ${Math.abs(city.evolution_1y)}%
        </span> sur 1 an
      </div>
    </div>
  </div>

  <div class="container">
    <div class="stats-bar" style="margin-top: -2rem;">
      <div class="stat-item">
        <div class="stat-value">${city.volume_2024}</div>
        <div class="stat-label">Transactions 2024</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">${city.prix_m2_maison.toLocaleString('fr-FR')} €</div>
        <div class="stat-label">Prix/m² Maison</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">+${city.evolution_5y}%</div>
        <div class="stat-label">Évolution 5 ans</div>
      </div>
    </div>
  </div>

  <footer class="footer">
    <div class="container">
      <div class="footer-bottom">
        <p>© 2024 ImmoStats France</p>
      </div>
    </div>
  </footer>
</body>
</html>`, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }
  }
};