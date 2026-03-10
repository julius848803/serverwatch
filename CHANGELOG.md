# Changelog

Alle wichtigen Änderungen an ServerWatch werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

## [1.2.0] - 2025-03-10

### ✨ Added
- Live Dashboard mit WebSocket-Updates alle 2 Sekunden
- Docker Remote API Integration für Container-Status
- Kombinierte Minecraft + Docker Status-Logik
- Discord Webhook Benachrichtigungen mit Embeds
- Telegram Bot Integration
- SQLite Ausfallhistorie mit Incidents & Status-History
- HTTP/HTTPS Check für phpMyAdmin
- Comprehensive Error Handling in allen Modulen
- Automatisches Reconnect für WebSocket Clients
- Systemd Service File für Production Deployment
- Installation Scripts (install.sh, setup_git.sh)

### 🎨 Features
- Responsive Dashboard Design mit Gradient Background
- Status-Karten mit Live-Updates
- Spieleranzahl-Anzeige für Minecraft-Server
- Container-State-Anzeige (running/exited/restarting)
- Overall System Status (healthy/degraded/critical)
- Latenz- und Antwortzeit-Metriken
- Emoji-basierte Status-Indikatoren
- WebSocket Connection Status Indicator

### 🔧 Configuration
- Flexibles `servers.json` Format
- Environment Variables via `.env`
- Konfigurierbares Check-Intervall (Standard: 7s)
- Critical Threshold für Alarmierung (Standard: 75%)

### 📊 Monitoring Capabilities
- ICMP Ping Checks
- TCP Port Checks
- Minecraft Server Protocol (mcstatus)
- Docker Container Health
- HTTP/HTTPS Endpoints
- Multi-Target parallel Checking

### 🔔 Alerting
- Nur bei Statuswechsel (nicht bei jedem Check)
- Severity-Levels: INFO, WARNING, CRITICAL, RECOVERY
- Downtime-Tracking mit automatischer Berechnung
- Discord Embeds mit strukturierten Fields
- Telegram HTML-formatierte Nachrichten

### 📦 Dependencies
- FastAPI + Uvicorn (Dashboard Backend)
- mcstatus (Minecraft Protocol)
- Docker SDK for Python
- python-telegram-bot
- aiohttp, aioping
- SQLite3 (built-in)

### 🐳 Docker Support
- Remote API Client (TCP/TLS)
- Container Status (running/exited/restarting)
- Health Check Integration
- Uptime Tracking

### 📝 Documentation
- Comprehensive README
- Installation Guide
- Configuration Examples
- systemd Service Setup
- Contributing Guidelines
- MIT License

---

## Entwickler
**xXLuckyGamer04Xx** - Initial Development

## Lizenz
Dieses Projekt ist unter der MIT Lizenz lizenziert.
