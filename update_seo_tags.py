#!/usr/bin/env python3
"""
Met à jour les balises SEO importantes pour toutes les pages
- Title optimisé
- Canonical
- Meta descriptions améliorées
"""

import os
import re
from glob import glob
from unidecode import unidecode

print("🔍 Mise à jour des balises SEO pour toutes les pages...")

def update_seo_tags(filepath):
    """Met à jour les balises SEO d'une page"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraire le nom de la ville depuis le title actuel
    title_match = re.search(r'<title>([^-]+) - ([^€]+)€/m² \| ImmoStats France</title>', content)
    if not title_match:
        return False

    ville_nom = title_match.group(1).strip()
    prix = title_match.group(2).strip()

    # Extraire le code INSEE
    code_match = re.search(r'<span class="badge">(\d+)</span>', content)
    code_insee = code_match.group(1) if code_match else '00000'

    # Créer l'URL canonical
    # Extraire le chemin depuis le filepath
    path_parts = filepath.replace('/Users/vincent/Documents/Projets/Immo/site/', '').replace('.html', '')
    canonical_url = f"https://www.immostats.fr/{path_parts}.html"

    # Nouveau title optimisé SEO
    new_title = f"Prix Immobilier {ville_nom} ({code_insee}) - {prix}€/m² | ImmoStats.fr"

    # Remplacer le title
    content = re.sub(
        r'<title>[^<]+</title>',
        f'<title>{new_title}</title>',
        content
    )

    # Ajouter canonical si pas présent
    if 'rel="canonical"' not in content:
        # Insérer après la balise meta description
        content = re.sub(
            r'(<meta name="description"[^>]+>)',
            f'\\1\n    <link rel="canonical" href="{canonical_url}">',
            content
        )

    # Améliorer la meta description
    old_desc_pattern = r'<meta name="description" content="[^"]+">'
    new_desc = f'<meta name="description" content="Prix immobilier {ville_nom} 2024 : {prix}€/m² ✓ Évolution des prix ✓ Statistiques détaillées ✓ Carte interactive ✓ Données officielles DVF - ImmoStats.fr">'
    content = re.sub(old_desc_pattern, new_desc, content)

    # Ajouter meta keywords
    if 'name="keywords"' not in content:
        keywords = f'<meta name="keywords" content="prix immobilier {ville_nom}, prix m2 {ville_nom}, immobilier {ville_nom}, {ville_nom} {prix} euros, statistiques immobilières {ville_nom}">'
        content = re.sub(
            r'(<meta name="description"[^>]+>)',
            f'\\1\n    {keywords}',
            content
        )

    # Ajouter og:url
    if 'property="og:url"' not in content:
        og_url = f'<meta property="og:url" content="{canonical_url}">'
        content = re.sub(
            r'(<meta property="og:type"[^>]+>)',
            f'\\1\n    {og_url}',
            content
        )

    # Ajouter Twitter Card
    if 'name="twitter:card"' not in content:
        twitter_tags = f'''    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Prix Immobilier {ville_nom} - {prix}€/m²">
    <meta name="twitter:description" content="Découvrez les prix immobiliers de {ville_nom} : {prix}€/m² en 2024. Statistiques complètes et évolution des prix.">
    <meta name="twitter:site" content="@ImmoStatsFr">'''

        content = re.sub(
            r'(</script>\n\n    <!-- Chart\.js)',
            f'</script>\n\n    <!-- Twitter Card -->\n{twitter_tags}\n\n    <!-- Chart.js',
            content
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

# Traiter toutes les pages
updated = 0
errors = 0

# Chercher toutes les pages HTML
all_files = glob('*/*/*.html')
total = len(all_files)

print(f"📝 Mise à jour de {total} pages...")

for filepath in all_files:
    try:
        if update_seo_tags(filepath):
            updated += 1

            if updated % 1000 == 0:
                print(f"  ✓ {updated}/{total} pages mises à jour...")
    except Exception as e:
        errors += 1
        if errors < 10:
            print(f"  ❌ Erreur pour {filepath}: {str(e)}")

print(f"\n✅ Mise à jour SEO terminée!")
print(f"  • {updated} pages mises à jour")
print(f"  • {errors} erreurs")
print(f"\nBalises ajoutées:")
print("  • Title optimisé SEO")
print("  • Canonical URL")
print("  • Meta description améliorée")
print("  • Meta keywords")
print("  • Open Graph URL")
print("  • Twitter Card")