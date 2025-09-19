#!/usr/bin/env python3
import os
import re

def fix_css_paths():
    count = 0
    fixed = 0

    # Parcourir tous les fichiers HTML
    for root, dirs, files in os.walk('.'):
        # Ignorer les dossiers git et node_modules
        if '.git' in root or 'node_modules' in root or '__pycache__' in root:
            continue

        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                count += 1

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Remplacer TOUTES les références CSS possibles
                    original = content

                    # Cas 1: href="styles.css"
                    content = re.sub(r'href="styles\.css"', 'href="/styles.css"', content)
                    # Cas 2: href="../styles.css"
                    content = re.sub(r'href="\.\.\/styles\.css"', 'href="/styles.css"', content)
                    # Cas 3: href="../../styles.css"
                    content = re.sub(r'href="\.\.\/\.\.\/styles\.css"', 'href="/styles.css"', content)
                    # Cas 4: href="../../../styles.css"
                    content = re.sub(r'href="\.\.\/\.\.\/\.\.\/styles\.css"', 'href="/styles.css"', content)
                    # Cas 5: href="./styles.css"
                    content = re.sub(r'href="\.\/styles\.css"', 'href="/styles.css"', content)

                    if content != original:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        fixed += 1
                        if fixed % 1000 == 0:
                            print(f"Corrigé: {fixed}/{count} fichiers...")

                except Exception as e:
                    print(f"Erreur avec {filepath}: {e}")

    print(f"\n✅ Résultat:")
    print(f"  - Total fichiers HTML: {count}")
    print(f"  - Fichiers corrigés: {fixed}")

if __name__ == "__main__":
    fix_css_paths()