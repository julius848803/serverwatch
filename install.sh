#!/bin/bash
# ServerWatch Quick Start Installation
# Author: xXLuckyGamer04Xx
# Version: 1.2.0

echo "================================================"
echo "ServerWatch v1.2.0 - Quick Start Installation"
echo "================================================"
echo ""

# Check Python Version
echo "1. Prüfe Python Version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nicht gefunden!"
    echo "Installation: sudo apt install python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo "✅ Python $PYTHON_VERSION gefunden"

# Install Dependencies
echo ""
echo "2. Installiere Python Dependencies..."
pip3 install -r requirements.txt --break-system-packages

if [ $? -ne 0 ]; then
    echo "⚠️  Fehler bei pip install, versuche ohne --break-system-packages..."
    pip3 install -r requirements.txt
fi

# Create .env from example
echo ""
echo "3. Erstelle .env Datei..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env erstellt - BITTE AUSFÜLLEN!"
    echo ""
    echo "WICHTIG: Öffne .env und trage deine Credentials ein:"
    echo "  - Discord Webhook URL"
    echo "  - Telegram Bot Token: 8628295908:AAGGlAZE1UJ4IGYIFNWyzx0Z2Y5MdWld6dQ"
    echo "  - Telegram Chat ID"
    echo "  - vServer IP"
    echo ""
else
    echo "ℹ️  .env existiert bereits"
fi

# Check Config
echo ""
echo "4. Prüfe Konfiguration..."
if [ ! -f config/servers.json ]; then
    echo "❌ config/servers.json nicht gefunden!"
    exit 1
fi
echo "✅ config/servers.json gefunden"

# Create logs directory
echo ""
echo "5. Erstelle logs Verzeichnis..."
mkdir -p logs
touch logs/.gitkeep
echo "✅ logs/ erstellt"

# Test Run
echo ""
echo "================================================"
echo "Installation abgeschlossen!"
echo "================================================"
echo ""
echo "Nächste Schritte:"
echo ""
echo "1. Konfiguriere .env mit deinen Credentials:"
echo "   nano .env"
echo ""
echo "2. Passe config/servers.json an deine Server an:"
echo "   nano config/servers.json"
echo ""
echo "3. Teste die Installation:"
echo "   python3 main.py"
echo ""
echo "4. Für Production (systemd Service):"
echo "   sudo cp serverwatch.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable serverwatch"
echo "   sudo systemctl start serverwatch"
echo ""
echo "Dashboard verfügbar unter: http://localhost:8000"
echo ""
