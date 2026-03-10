# 🖥️ ServerWatch - Server Monitoring System

**Version:** 1.5.0  
**Author:** xXLuckyGamer04Xx

Professionelles Monitoring-System für vServer, Docker Container, Minecraft-Server, MySQL und mehr.

---

## 📋 Features

### ✅ Monitoring
- **vServer Ping** - ICMP/TCP Erreichbarkeit
- **Minecraft Server** - Spieleranzahl, MOTD, Version via Server List Ping
- **Docker Container** - Container-Status via Remote API
- **MySQL/TCP** - Port-Checks für Datenbanken
- **HTTP/HTTPS** - Webserver-Monitoring (phpMyAdmin, etc.)

### 🔔 Benachrichtigungen
- **Discord** - Rich Embeds mit Farbcodierung
- **Telegram** - Markdown-formatierte Nachrichten
- **Smart Alerting** - Nur bei Statuswechsel, nicht bei jedem Check

### 📊 Dashboard
- **Live WebSocket** - Echtzeit-Updates alle 7 Sekunden
- **Responsive Design** - Desktop & Mobile
- **Status-Historie** - Letzte Ausfälle mit Dauer
- **Dark Theme** - Moderne UI

### 🐳 Docker Integration
- **Kombinierte Checks** - Port + Container-Status
- **Smart Detection** - Unterscheidet zwischen "Server startet" und "Container crashed"

---

## 🚀 Schnellstart

### 1. Installation

```bash
# Dependencies installieren
pip install -r requirements.txt

# .env konfigurieren
cp .env.example .env
nano .env

# config/servers.json anpassen
nano config/servers.json

# Starten
python3 main.py
```

### 2. Als Service (systemd)

```bash
sudo cp serverwatch.service /etc/systemd/system/
sudo systemctl enable --now serverwatch
```

### 3. Dashboard öffnen

```
http://localhost:8080
```

---

## ⚙️ Konfiguration

### .env Datei

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-100123456789
DOCKER_HOST=tcp://123.456.789.0:2376
VSERVER_IP=123.456.789.0
DASHBOARD_PORT=8080
```

### config/servers.json

```json
{
  "interval_seconds": 7,
  "vserver_ip": "123.456.789.0",
  "docker_host": "tcp://123.456.789.0:2376",
  "targets": [
    {
      "name": "lobby-server",
      "host": "123.456.789.0",
      "port": 25565,
      "type": "minecraft",
      "docker_container": "lobby-server"
    }
  ]
}
```

---

## 📡 Check-Typen

### Ping Check
```json
{
  "name": "vServer Host",
  "host": "123.456.789.0",
  "type": "ping"
}
```

### Minecraft Check (mit Docker)
```json
{
  "name": "CitybuildServer",
  "host": "123.456.789.0",
  "port": 25566,
  "type": "minecraft",
  "docker_container": "citybuild-server"
}
```

### TCP Check
```json
{
  "name": "MySQL",
  "host": "123.456.789.0",
  "port": 3306,
  "type": "tcp"
}
```

### HTTP Check
```json
{
  "name": "phpMyAdmin",
  "host": "123.456.789.0",
  "port": 80,
  "type": "http"
}
```

---

## 🐳 Docker Remote API Setup

**Auf dem vServer:**

```bash
# Option 1: Via systemd
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/override.conf
```

Inhalt:
```ini
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker

# Firewall (wichtig!)
sudo ufw allow from MONITORING_IP to any port 2376 proto tcp
```

---

## 🔔 Benachrichtigungen

### Discord Webhook

1. Server-Einstellungen → Integrationen
2. Webhook erstellen
3. URL kopieren → `.env`

### Telegram Bot

```bash
# 1. Mit @BotFather chatten
/newbot

# 2. Token kopieren

# 3. Chat-ID abrufen
curl https://api.telegram.org/bot<TOKEN>/getUpdates
```

---

## 📊 API Endpoints

```
GET  /api/status              - Aktueller Status
GET  /api/outages             - Ausfall-Historie
GET  /api/outages/active      - Laufende Ausfälle
GET  /api/history/{target}    - Status-Verlauf
WS   /ws                      - Live-Updates
```

---

## 🔧 Fehlerbehebung

### Docker Connection Failed
```bash
# Auf vServer:
sudo netstat -tlnp | grep 2376
sudo systemctl status docker
```

### Keine Benachrichtigungen
```bash
# Webhook testen:
curl -X POST <DISCORD_WEBHOOK> \
  -H 'Content-Type: application/json' \
  -d '{"content":"Test"}'
```

### Dashboard lädt nicht
```bash
# Logs prüfen:
sudo journalctl -u serverwatch -f
```

---

## 📝 Projekt-Autor

Entwickelt von **xXLuckyGamer04Xx**  
Minecraft-Server: Kr3pp1 hat volle Rechte & Immunität

---

## 📄 Lizenz

Siehe LICENSE Datei
