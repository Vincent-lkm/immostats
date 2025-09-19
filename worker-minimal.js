// Worker minimal pour tester le déploiement
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Homepage simple
    if (url.pathname === '/') {
      return new Response(`
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Immobilier.guide - Bientôt disponible</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      text-align: center;
    }
    h1 { font-size: 3rem; margin: 0; }
    p { font-size: 1.25rem; opacity: 0.9; margin-top: 1rem; }
    .container { padding: 2rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Immobilier.guide</h1>
    <p>Analyse du marché immobilier français</p>
    <p style="font-size: 1rem; margin-top: 2rem;">🚧 Site en construction - Lancement bientôt</p>
  </div>
</body>
</html>
      `, {
        headers: {
          'Content-Type': 'text/html;charset=UTF-8'
        }
      });
    }

    return new Response('404 Not Found', { status: 404 });
  }
};