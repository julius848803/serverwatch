#!/bin/bash
# Git Setup Script für ServerWatch
# Author: xXLuckyGamer04Xx
# Version: 1.2.0

echo "================================================"
echo "ServerWatch - Git Repository Setup"
echo "================================================"
echo ""

# Repository URL (anpassen!)
REPO_URL="https://github.com/IhrUsername/serverwatch.git"

echo "1. Git initialisieren..."
git init

echo "2. Dateien zum Staging hinzufügen..."
git add .

echo "3. Initial Commit erstellen..."
git commit -m "Initial commit: ServerWatch v1.2.0

- Complete monitoring system für Minecraft Docker Server
- Discord & Telegram Benachrichtigungen
- Live Dashboard mit WebSocket
- Docker Remote API Integration
- SQLite Ausfallhistorie
- Comprehensive error handling

Developed by xXLuckyGamer04Xx"

echo "4. Branch auf 'main' umbenennen..."
git branch -M main

echo "5. Remote Repository hinzufügen..."
echo "WICHTIG: Passe die Repository URL an!"
echo "Aktuell: $REPO_URL"
read -p "Möchtest du eine andere URL verwenden? (y/n): " CHANGE_URL

if [ "$CHANGE_URL" = "y" ]; then
    read -p "Gib die GitHub Repository URL ein: " CUSTOM_URL
    REPO_URL=$CUSTOM_URL
fi

git remote add origin $REPO_URL

echo "6. Push zum Remote Repository..."
git push -u origin main

echo ""
echo "================================================"
echo "✅ Git Setup abgeschlossen!"
echo "================================================"
echo ""
echo "Repository: $REPO_URL"
echo ""
echo "Nächste Schritte:"
echo "1. Öffne GitHub und prüfe das Repository"
echo "2. Füge eine .env Datei hinzu (nicht in Git!)"
echo "3. Konfiguriere config/servers.json für deine Server"
echo ""
