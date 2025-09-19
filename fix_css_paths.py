#!/usr/bin/env python3
import os
import re

def fix_css_paths():
    count = 0

    # Parcourir tous les fichiers HTML
    for root, dirs, files in os.walk('.'):
        # Ignorer les dossiers git et node_modules
        if '.git' in root or 'node_modules' in root:
            continue

        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Remplacer les chemins CSS relatifs par des chemins absolus
                    updated_content = content.replace('href="styles.css"', 'href="/styles.css"')

                    if content != updated_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        count += 1
                        if count % 1000 == 0:
                            print(f"Mis à jour: {count} fichiers...")

                except Exception as e:
                    print(f"Erreur avec {filepath}: {e}")

    print(f"\n✅ Total: {count} fichiers HTML mis à jour avec le bon chemin CSS")

if __name__ == "__main__":
    fix_css_paths()