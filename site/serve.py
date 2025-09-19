#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir('site')
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🚀 Serveur démarré sur http://localhost:{PORT}")
    print("   Appuyez sur Ctrl+C pour arrêter")
    httpd.serve_forever()
