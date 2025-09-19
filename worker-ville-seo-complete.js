// Worker avec pages villes ultra-optimisées SEO (800-1000 mots)
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Exemple pour Paris 8ème avec contenu SEO complet
    if (path === '/ville/75008' || path === '/ville/75008/') {
      return renderCityPageSEO();
    }

    return new Response('404', { status: 404 });
  }
}

function renderCityPageSEO() {
  const city = {
    name: "Paris 8ème",
    code: "75008",
    prix_m2_appartement: 11450,
    prix_m2_maison: 15000,
    evolution_1y: 2.8,
    evolution_5y: 11.5,
    volume_2024: 512,
    volume_2023: 478,
    surface_moyenne: 82,
    delai_vente: 38,
    tension: 8.8,
    roi_locatif: 2.9,
    prix_median: 939000
  };

  return new Response(`<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prix Immobilier Paris 8ème (75008) - ${city.prix_m2_appartement}€/m² en 2024 | ImmoStats</title>
  <meta name="description" content="Prix immobilier Paris 8ème arrondissement : ${city.prix_m2_appartement}€/m² pour un appartement. ✓ ${city.volume_2024} transactions en 2024 ✓ Évolution +${city.evolution_1y}% ✓ Données DVF officielles mises à jour">

  <!-- Schema.org LocalBusiness -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Place",
    "name": "Paris 8ème arrondissement",
    "address": {
      "@type": "PostalAddress",
      "postalCode": "75008",
      "addressLocality": "Paris",
      "addressRegion": "Île-de-France",
      "addressCountry": "FR"
    }
  }
  </script>

  <!-- Schema.org FAQ -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Quel est le prix moyen au m² à Paris 8ème ?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Le prix moyen au m² pour un appartement dans le 8ème arrondissement de Paris est de ${city.prix_m2_appartement}€ en 2024, avec une évolution de +${city.evolution_1y}% sur un an."
        }
      },
      {
        "@type": "Question",
        "name": "Combien de temps pour vendre dans le 8ème arrondissement ?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Le délai moyen de vente dans le 8ème arrondissement est de ${city.delai_vente} jours, ce qui est inférieur à la moyenne parisienne."
        }
      }
    ]
  }
  </script>

  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.7;
      color: #111827;
      background: #f9fafb;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 1rem;
    }

    /* Breadcrumb */
    .breadcrumb {
      padding: 1rem 0;
      font-size: 0.875rem;
      background: white;
      border-bottom: 1px solid #e5e7eb;
    }

    .breadcrumb a {
      color: #2563eb;
      text-decoration: none;
    }

    .breadcrumb span {
      color: #6b7280;
      margin: 0 0.5rem;
    }

    /* Hero */
    .hero {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 3rem 0;
    }

    .hero h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }

    .hero-price {
      font-size: 3rem;
      font-weight: bold;
      margin: 1rem 0;
    }

    .hero-evolution {
      font-size: 1.25rem;
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    /* KPIs */
    .kpis {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin: -2rem 0 3rem 0;
      padding: 1.5rem;
      background: white;
      border-radius: 0.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .kpi-item {
      text-align: center;
      padding: 1rem;
      border-right: 1px solid #e5e7eb;
    }

    .kpi-item:last-child {
      border-right: none;
    }

    .kpi-value {
      font-size: 2rem;
      font-weight: bold;
      color: #2563eb;
    }

    .kpi-label {
      font-size: 0.875rem;
      color: #6b7280;
      margin-top: 0.25rem;
    }

    /* Content sections */
    .content-section {
      background: white;
      padding: 2rem;
      margin: 2rem 0;
      border-radius: 0.5rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    h2 {
      color: #1f2937;
      font-size: 1.875rem;
      margin-bottom: 1.5rem;
      padding-bottom: 0.75rem;
      border-bottom: 2px solid #2563eb;
    }

    h3 {
      color: #374151;
      font-size: 1.25rem;
      margin: 1.5rem 0 1rem 0;
    }

    p {
      margin-bottom: 1rem;
      color: #4b5563;
      line-height: 1.8;
    }

    /* Quartiers grid */
    .quartiers-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 1rem;
      margin: 1.5rem 0;
    }

    .quartier-card {
      padding: 1rem;
      background: #f3f4f6;
      border-radius: 0.5rem;
      border-left: 4px solid #2563eb;
    }

    .quartier-name {
      font-weight: 600;
      color: #1f2937;
    }

    .quartier-price {
      color: #2563eb;
      font-size: 1.25rem;
      font-weight: bold;
    }

    /* Villes voisines */
    .villes-voisines {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
      margin: 1.5rem 0;
    }

    .ville-link {
      display: block;
      padding: 1rem;
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 0.5rem;
      text-decoration: none;
      color: inherit;
      transition: all 0.2s;
    }

    .ville-link:hover {
      border-color: #2563eb;
      transform: translateY(-2px);
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* FAQ */
    .faq-item {
      padding: 1.5rem;
      margin: 1rem 0;
      background: #f9fafb;
      border-left: 4px solid #2563eb;
      border-radius: 0.5rem;
    }

    .faq-question {
      font-weight: 600;
      color: #1f2937;
      margin-bottom: 0.5rem;
    }

    .faq-answer {
      color: #4b5563;
      line-height: 1.8;
    }

    /* Table */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
    }

    th {
      background: #f3f4f6;
      padding: 0.75rem;
      text-align: left;
      font-weight: 600;
      color: #374151;
      border-bottom: 2px solid #e5e7eb;
    }

    td {
      padding: 0.75rem;
      border-bottom: 1px solid #e5e7eb;
    }

    tr:hover {
      background: #f9fafb;
    }

    /* Footer */
    .footer {
      background: #111827;
      color: white;
      padding: 3rem 0;
      margin-top: 4rem;
    }

    .footer-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 2rem;
      margin-bottom: 2rem;
    }

    .footer h3 {
      margin-bottom: 1rem;
    }

    .footer a {
      color: #9ca3af;
      text-decoration: none;
      display: block;
      padding: 0.25rem 0;
    }

    .footer a:hover {
      color: white;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .hero h1 { font-size: 1.875rem; }
      .hero-price { font-size: 2.5rem; }
      .kpis { grid-template-columns: 1fr; }
      .kpi-item { border-right: none; border-bottom: 1px solid #e5e7eb; }
    }
  </style>
</head>
<body>
  <!-- Breadcrumb -->
  <nav class="breadcrumb">
    <div class="container">
      <a href="/">🏠 Accueil</a>
      <span>›</span>
      <a href="/region/ile-de-france">Île-de-France</a>
      <span>›</span>
      <a href="/dept/75">Paris (75)</a>
      <span>›</span>
      <strong>Paris 8ème arrondissement</strong>
    </div>
  </nav>

  <!-- Hero -->
  <section class="hero">
    <div class="container">
      <h1>Prix Immobilier Paris 8ème Arrondissement (75008)</h1>
      <div class="hero-price">${city.prix_m2_appartement.toLocaleString('fr-FR')} €/m²</div>
      <div class="hero-evolution">
        <span>↑ +${city.evolution_1y}% sur 1 an</span>
        <span style="opacity: 0.8">• +${city.evolution_5y}% sur 5 ans</span>
      </div>
    </div>
  </section>

  <!-- KPIs principaux -->
  <div class="container">
    <div class="kpis">
      <div class="kpi-item">
        <div class="kpi-value">${city.volume_2024}</div>
        <div class="kpi-label">Transactions en 2024</div>
      </div>
      <div class="kpi-item">
        <div class="kpi-value">${city.surface_moyenne} m²</div>
        <div class="kpi-label">Surface moyenne</div>
      </div>
      <div class="kpi-item">
        <div class="kpi-value">${city.delai_vente} j</div>
        <div class="kpi-label">Délai de vente</div>
      </div>
      <div class="kpi-item">
        <div class="kpi-value">${city.tension}/10</div>
        <div class="kpi-label">Tension du marché</div>
      </div>
      <div class="kpi-item">
        <div class="kpi-value">${city.roi_locatif}%</div>
        <div class="kpi-label">Rentabilité locative</div>
      </div>
    </div>

    <!-- Introduction longue et optimisée SEO -->
    <section class="content-section">
      <h2>Le Marché Immobilier du 8ème Arrondissement de Paris en 2024</h2>

      <p>
        Le <strong>8ème arrondissement de Paris</strong> demeure l'un des quartiers les plus prestigieux et recherchés de la capitale française.
        Avec un <strong>prix moyen de ${city.prix_m2_appartement}€ au mètre carré pour un appartement</strong>, ce secteur emblématique
        qui englobe les Champs-Élysées, l'Avenue Montaigne et le Parc Monceau, maintient sa position parmi les zones immobilières
        les plus valorisées de France.
      </p>

      <p>
        En 2024, le marché immobilier du 8ème arrondissement affiche une <strong>progression de +${city.evolution_1y}%</strong> sur un an,
        témoignant de la résilience et de l'attractivité constante de ce secteur auprès des acquéreurs français et internationaux.
        Cette croissance s'inscrit dans une tendance plus large avec une <strong>hausse de +${city.evolution_5y}% sur les cinq dernières années</strong>,
        confirmant le statut du 8ème comme valeur refuge dans l'immobilier parisien de prestige.
      </p>

      <p>
        Avec <strong>${city.volume_2024} transactions enregistrées depuis le début de l'année 2024</strong>, le marché reste dynamique
        malgré la hausse des prix. Le délai moyen de vente de <strong>${city.delai_vente} jours</strong> est significativement
        inférieur à la moyenne parisienne, illustrant la forte demande pour les biens de ce secteur. La surface moyenne
        des biens vendus s'établit à <strong>${city.surface_moyenne} m²</strong>, reflétant le caractère haussmannien
        et les volumes généreux caractéristiques de l'arrondissement.
      </p>
    </section>

    <!-- Analyse détaillée par type de bien -->
    <section class="content-section">
      <h2>Prix de l'Immobilier par Type de Bien dans le 8ème</h2>

      <h3>Appartements dans le 8ème arrondissement</h3>
      <p>
        Les appartements représentent l'essentiel du marché immobilier du 8ème arrondissement avec un prix moyen de
        <strong>${city.prix_m2_appartement}€/m²</strong>. Les biens les plus recherchés sont les appartements haussmanniens
        avec leurs caractéristiques d'époque : moulures, parquets en point de Hongrie, cheminées en marbre et hauteur
        sous plafond exceptionnelle. Les appartements avec vue sur les monuments emblématiques comme l'Arc de Triomphe
        ou la Tour Eiffel peuvent atteindre des prix sensiblement supérieurs à la moyenne.
      </p>

      <h3>Maisons et hôtels particuliers</h3>
      <p>
        Les maisons et hôtels particuliers, bien que rares dans le 8ème, affichent des prix moyens de
        <strong>${city.prix_m2_maison}€/m²</strong>. Ces biens d'exception, souvent situés dans les rues calmes
        près du Parc Monceau ou dans le quartier de la Plaine Monceau, attirent une clientèle fortunée à la
        recherche d'espaces uniques avec jardins privatifs, une rareté absolue dans ce secteur de Paris.
      </p>

      <h3>Investissement locatif et rentabilité</h3>
      <p>
        Avec une rentabilité locative moyenne de <strong>${city.roi_locatif}%</strong>, l'investissement dans le 8ème
        arrondissement reste attractif malgré les prix élevés à l'achat. La demande locative est soutenue par la
        présence de nombreux sièges sociaux d'entreprises internationales, d'ambassades et d'institutions prestigieuses.
        Les locations meublées de courte durée, particulièrement prisées par une clientèle d'affaires et touristique
        haut de gamme, peuvent offrir des rendements supérieurs à la moyenne.
      </p>
    </section>

    <!-- Quartiers du 8ème -->
    <section class="content-section">
      <h2>Les Quartiers du 8ème Arrondissement</h2>

      <p>
        Le 8ème arrondissement se compose de quatre quartiers administratifs distincts, chacun avec ses caractéristiques
        propres et ses variations de prix :
      </p>

      <div class="quartiers-grid">
        <div class="quartier-card">
          <div class="quartier-name">🏛️ Champs-Élysées</div>
          <div class="quartier-price">12 500 €/m²</div>
          <p>L'avenue la plus célèbre du monde, commerces de luxe et bureaux prestigieux</p>
        </div>
        <div class="quartier-card">
          <div class="quartier-name">🌳 Faubourg-du-Roule</div>
          <div class="quartier-price">11 200 €/m²</div>
          <p>Quartier résidentiel calme, proche du Parc Monceau</p>
        </div>
        <div class="quartier-card">
          <div class="quartier-name">🏢 Madeleine</div>
          <div class="quartier-price">11 800 €/m²</div>
          <p>Centre d'affaires, grands magasins et Place de la Madeleine</p>
        </div>
        <div class="quartier-card">
          <div class="quartier-name">🌟 Europe</div>
          <div class="quartier-price">10 900 €/m²</div>
          <p>Quartier familial autour de la gare Saint-Lazare</p>
        </div>
      </div>

      <p>
        Les prix varient sensiblement selon la localisation exacte : les biens situés sur l'Avenue Montaigne,
        rue du Faubourg Saint-Honoré ou Avenue George V atteignent régulièrement des sommets, tandis que les
        rues plus éloignées des axes principaux offrent des opportunités à des prix légèrement plus accessibles.
      </p>
    </section>

    <!-- Comparaison avec arrondissements voisins -->
    <section class="content-section">
      <h2>Comparer avec les Arrondissements Voisins</h2>

      <p>
        Le 8ème arrondissement se positionne dans la fourchette haute des prix parisiens. Voici comment il se
        compare aux arrondissements limitrophes :
      </p>

      <div class="villes-voisines">
        <a href="/ville/75001" class="ville-link">
          <strong>Paris 1er</strong><br>
          12 200 €/m²<br>
          <span style="color: #ef4444">+6.6% vs 8ème</span>
        </a>
        <a href="/ville/75002" class="ville-link">
          <strong>Paris 2ème</strong><br>
          10 800 €/m²<br>
          <span style="color: #10b981">-5.7% vs 8ème</span>
        </a>
        <a href="/ville/75009" class="ville-link">
          <strong>Paris 9ème</strong><br>
          9 850 €/m²<br>
          <span style="color: #10b981">-14.0% vs 8ème</span>
        </a>
        <a href="/ville/75016" class="ville-link">
          <strong>Paris 16ème</strong><br>
          10 500 €/m²<br>
          <span style="color: #10b981">-8.3% vs 8ème</span>
        </a>
        <a href="/ville/75017" class="ville-link">
          <strong>Paris 17ème</strong><br>
          9 200 €/m²<br>
          <span style="color: #10b981">-19.7% vs 8ème</span>
        </a>
        <a href="/ville/92200" class="ville-link">
          <strong>Neuilly-sur-Seine</strong><br>
          10 200 €/m²<br>
          <span style="color: #10b981">-10.9% vs 8ème</span>
        </a>
      </div>
    </section>

    <!-- Évolution historique -->
    <section class="content-section">
      <h2>Évolution Historique des Prix dans le 8ème</h2>

      <table>
        <thead>
          <tr>
            <th>Année</th>
            <th>Prix moyen/m²</th>
            <th>Évolution annuelle</th>
            <th>Nombre de ventes</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>2024</td>
            <td><strong>11 450 €</strong></td>
            <td style="color: #10b981">+2.8%</td>
            <td>512</td>
          </tr>
          <tr>
            <td>2023</td>
            <td>11 100 €</td>
            <td style="color: #10b981">+2.3%</td>
            <td>478</td>
          </tr>
          <tr>
            <td>2022</td>
            <td>10 850 €</td>
            <td style="color: #10b981">+4.3%</td>
            <td>445</td>
          </tr>
          <tr>
            <td>2021</td>
            <td>10 400 €</td>
            <td style="color: #10b981">+1.5%</td>
            <td>398</td>
          </tr>
          <tr>
            <td>2020</td>
            <td>10 250 €</td>
            <td style="color: #ef4444">-0.5%</td>
            <td>352</td>
          </tr>
        </tbody>
      </table>

      <p>
        L'analyse sur cinq ans montre une progression constante et soutenue des prix, avec une accélération
        notable depuis 2022. Cette tendance s'explique par plusieurs facteurs : le retour des investisseurs
        internationaux post-pandémie, la rareté de l'offre dans ce secteur prisé, et l'attrait renouvelé
        pour les biens de prestige parisiens.
      </p>
    </section>

    <!-- FAQ détaillée -->
    <section class="content-section">
      <h2>Questions Fréquentes sur l'Immobilier dans le 8ème</h2>

      <div class="faq-item">
        <div class="faq-question">Quel est le prix moyen d'un appartement de 100m² dans le 8ème arrondissement ?</div>
        <div class="faq-answer">
          Un appartement de 100m² dans le 8ème arrondissement coûte en moyenne 1 145 000€ (base : 11 450€/m²).
          Cependant, ce prix peut varier considérablement selon l'étage, l'état du bien, la présence d'un ascenseur,
          et surtout la localisation exacte dans l'arrondissement.
        </div>
      </div>

      <div class="faq-item">
        <div class="faq-question">Quels sont les meilleurs quartiers pour investir dans le 8ème ?</div>
        <div class="faq-answer">
          Pour l'investissement locatif, le quartier Europe offre le meilleur rapport qualité-prix avec des biens
          légèrement moins chers mais une forte demande locative grâce à la proximité de Saint-Lazare. Pour la
          valorisation long terme, les abords du Parc Monceau restent une valeur sûre.
        </div>
      </div>

      <div class="faq-item">
        <div class="faq-question">Quelle est la plus-value moyenne sur 5 ans dans le 8ème ?</div>
        <div class="faq-answer">
          La plus-value moyenne sur 5 ans s'établit à +${city.evolution_5y}%, soit environ 1 175€/m² de gain.
          Un appartement acheté 970 000€ en 2019 vaut aujourd'hui environ 1 080 000€, générant une plus-value
          brute de 110 000€ avant frais et taxes.
        </div>
      </div>

      <div class="faq-item">
        <div class="faq-question">Est-il préférable d'acheter ou de louer dans le 8ème arrondissement ?</div>
        <div class="faq-answer">
          Avec un prix d'achat moyen de 11 450€/m² et des loyers autour de 38-42€/m²/mois, l'achat devient
          intéressant pour une durée de détention supérieure à 7-8 ans. La décision dépend de votre situation
          personnelle, de votre capacité d'emprunt et de vos projets à long terme.
        </div>
      </div>

      <div class="faq-item">
        <div class="faq-question">Quels sont les frais de notaire pour un achat dans le 8ème ?</div>
        <div class="faq-answer">
          Les frais de notaire représentent environ 7-8% du prix d'achat pour l'ancien (la majorité du parc
          du 8ème). Pour un appartement à 1 million d'euros, comptez environ 75 000€ de frais de notaire,
          incluant les droits de mutation, les émoluments du notaire et les frais divers.
        </div>
      </div>
    </section>

    <!-- Conseils pratiques -->
    <section class="content-section">
      <h2>Conseils pour Acheter dans le 8ème Arrondissement</h2>

      <h3>🔍 Bien préparer sa recherche</h3>
      <p>
        Le marché du 8ème est très compétitif. Préparez votre dossier de financement en amont, obtenez une
        pré-approbation bancaire et soyez réactif lors des visites. Les biens de qualité partent généralement
        en moins de ${city.delai_vente} jours.
      </p>

      <h3>💰 Budget et financement</h3>
      <p>
        Prévoyez un budget minimum de 900 000€ pour un 2 pièces et 1.5 million d'euros pour un 3 pièces.
        Les banques exigent généralement un apport de 20% minimum pour ce type de bien. N'oubliez pas
        d'inclure les frais de notaire (7-8%) et d'éventuels travaux dans votre budget global.
      </p>

      <h3>🏗️ Attention aux charges</h3>
      <p>
        Les charges de copropriété dans le 8ème sont parmi les plus élevées de Paris, souvent entre
        40 et 60€/m²/an pour les immeubles avec gardien et prestations de standing. Vérifiez
        systématiquement le montant des charges et les travaux votés ou à prévoir.
      </p>

      <h3>📈 Potentiel de valorisation</h3>
      <p>
        Privilégiez les biens avec des éléments de valorisation : étages élevés avec ascenseur,
        balcons ou terrasses, vue dégagée, proximité immédiate du métro. Ces caractéristiques
        garantissent une meilleure liquidité et une valorisation supérieure à long terme.
      </p>
    </section>

    <!-- Transport et commodités -->
    <section class="content-section">
      <h2>Vivre dans le 8ème Arrondissement</h2>

      <h3>🚇 Transports et accessibilité</h3>
      <p>
        Le 8ème arrondissement est exceptionnellement bien desservi avec 11 stations de métro
        (lignes 1, 2, 3, 8, 9, 12, 13, 14), la gare Saint-Lazare (2ème gare d'Europe), et de
        nombreuses lignes de bus. Cette excellente desserte contribue significativement aux
        prix élevés de l'immobilier dans le secteur.
      </p>

      <h3>🛍️ Commerces et services</h3>
      <p>
        L'arrondissement abrite les commerces les plus prestigieux de Paris : les Champs-Élysées,
        l'Avenue Montaigne, le Faubourg Saint-Honoré. Les résidents bénéficient également de
        marchés de proximité, notamment le marché de la Madeleine et celui d'Aguesseau.
      </p>

      <h3>🎓 Établissements scolaires</h3>
      <p>
        Le 8ème compte plusieurs établissements scolaires réputés, publics et privés, dont le
        Lycée Chaptal et le Collège Condorcet. Cette offre éducative de qualité attire de
        nombreuses familles malgré les prix élevés de l'immobilier.
      </p>

      <h3>🌳 Espaces verts</h3>
      <p>
        Le Parc Monceau, joyau du 8ème avec ses 8 hectares, offre un havre de verdure rare
        dans ce quartier dense. Les jardins des Champs-Élysées et le square Marcel-Pagnol
        complètent l'offre d'espaces verts, très recherchés par les familles.
      </p>
    </section>

    <!-- Conclusion et perspectives -->
    <section class="content-section">
      <h2>Perspectives du Marché Immobilier dans le 8ème</h2>

      <p>
        Le marché immobilier du 8ème arrondissement de Paris continue d'afficher une remarquable
        résilience. Avec une progression de +${city.evolution_1y}% en 2024 et +${city.evolution_5y}%
        sur cinq ans, l'arrondissement confirme son statut de valeur refuge dans l'immobilier
        parisien de prestige.
      </p>

      <p>
        Les perspectives pour 2025 restent positives, soutenues par plusieurs facteurs : le retour
        des investisseurs internationaux, les Jeux Olympiques de Paris 2024 qui ont renforcé
        l'attractivité de la capitale, et la rareté structurelle de l'offre dans ce secteur prisé.
        La tension du marché, évaluée à ${city.tension}/10, reste élevée avec une demande
        largement supérieure à l'offre disponible.
      </p>

      <p>
        Pour les investisseurs et acquéreurs potentiels, le 8ème arrondissement représente un
        placement patrimonial de premier ordre, combinant prestige de l'adresse, qualité de vie
        exceptionnelle et potentiel de valorisation à long terme. Malgré des prix d'entrée élevés,
        la liquidité du marché et la demande constante garantissent la pérennité de l'investissement.
      </p>
    </section>
  </div>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h3>ImmoStats France</h3>
          <p style="color: #9ca3af;">
            Données immobilières officielles DVF<br>
            36 000 communes analysées<br>
            Mise à jour mensuelle
          </p>
        </div>
        <div>
          <h3>Paris - Arrondissements</h3>
          <a href="/ville/75001">Paris 1er - Louvre</a>
          <a href="/ville/75002">Paris 2ème - Bourse</a>
          <a href="/ville/75003">Paris 3ème - Temple</a>
          <a href="/ville/75004">Paris 4ème - Hôtel-de-Ville</a>
          <a href="/ville/75005">Paris 5ème - Panthéon</a>
        </div>
        <div>
          <h3>Villes Île-de-France</h3>
          <a href="/ville/92200">Neuilly-sur-Seine</a>
          <a href="/ville/92100">Boulogne-Billancourt</a>
          <a href="/ville/92300">Levallois-Perret</a>
          <a href="/ville/78000">Versailles</a>
          <a href="/ville/93100">Montreuil</a>
        </div>
        <div>
          <h3>Ressources</h3>
          <a href="/methodologie">Méthodologie</a>
          <a href="/donnees-dvf">Données DVF</a>
          <a href="/api">API Développeurs</a>
          <a href="/blog">Blog Immobilier</a>
          <a href="/contact">Contact</a>
        </div>
      </div>
      <div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #374151; color: #6b7280;">
        © 2024 ImmoStats France - Données publiques DVF - Dernière mise à jour : Novembre 2024
      </div>
    </div>
  </footer>

  <script>
    // Schema.org BreadcrumbList
    const breadcrumbSchema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Accueil",
          "item": "https://immostats.fr/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Île-de-France",
          "item": "https://immostats.fr/region/ile-de-france"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Paris",
          "item": "https://immostats.fr/dept/75"
        },
        {
          "@type": "ListItem",
          "position": 4,
          "name": "Paris 8ème",
          "item": "https://immostats.fr/ville/75008"
        }
      ]
    };

    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(breadcrumbSchema);
    document.head.appendChild(script);
  </script>
</body>
</html>`, {
    headers: {
      'Content-Type': 'text/html;charset=UTF-8',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}