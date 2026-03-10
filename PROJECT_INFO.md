# 🖥️ ServerWatch v1.2.0 - Projekt-Information

## 📊 Statistiken

- **Entwickler:** xXLuckyGamer04Xx
- **Version:** 1.2.0
- **Lizenz:** MIT
- **Sprache:** Python 3.9+
- **Codezeilen:** ~1.934 Zeilen Python
- **Dateien:** 38 Dateien
- **Module:** 15 Python-Module

## 🎯 Projektbeschreibung

ServerWatch ist ein professionelles Monitoring-System speziell entwickelt für Minecraft-Server in Docker-Umgebungen. Es kombiniert leistungsstarke Überwachungsfunktionen mit einem benutzerfreundlichen Live-Dashboard und intelligenten Benachrichtigungen.

## ✨ Hauptfunktionen

### Monitoring
- ✅ **Minecraft Server Protocol** - Spieleranzahl, MOTD, Version
- ✅ **Docker Container Status** - running, exited, restarting
- ✅ **ICMP Ping** - vServer Erreichbarkeit
- ✅ **TCP Port Checks** - MySQL, Custom Ports
- ✅ **HTTP/HTTPS** - phpMyAdmin, Web-Services
- ✅ **Kombinierte Logik** - Docker + TCP für Smart Alerts

### Alerting
- 🔔 **Discord Webhooks** - Rich Embeds mit Farbcodierung
- 📱 **Telegram Bot** - HTML-formatierte Nachrichten
- 🎯 **Intelligente Auslösung** - Nur bei Statuswechsel
- ⏱️ **Downtime Tracking** - Automatische Ausfallzeit-Berechnung
- 📊 **Severity Levels** - INFO, WARNING, CRITICAL, RECOVERY

### Dashboard
- 📺 **Live Updates** - WebSocket alle 2 Sekunden
- 🎨 **Responsive Design** - Modern Gradient UI
- 🔄 **Auto-Reconnect** - Automatische WebSocket-Wiederverbindung
- 📈 **Status-Karten** - Pro Server/Service
- 🟢🟡🔴 **Ampelsystem** - Visueller Gesamtstatus

### Datenbank
- 💾 **SQLite** - Eingebettete Datenbank
- 📝 **Incident Logging** - Alle Ausfälle dokumentiert
- 📊 **Status History** - Komplette Check-Historie
- ⏰ **Timestamps** - ISO 8601 Format

## 🏗️ Architektur

### Backend
- **FastAPI** - Modernes Python Web Framework
- **asyncio** - Asynchrone I/O für Performance
- **WebSockets** - Bidirektionale Echtzeit-Kommunikation
- **Docker SDK** - Remote API Integration

### Frontend
- **Vanilla JavaScript** - Keine Frameworks, pure Performance
- **WebSocket Client** - Auto-Reconnect Logik
- **CSS Grid** - Responsive Layout
- **Font Awesome** - Icons

## 📁 Modul-Übersicht

```
src/
├── monitor.py          (267 Zeilen) - Haupt-Loop & Orchestrierung
├── api.py              (134 Zeilen) - FastAPI + WebSocket
├── alerting.py         (182 Zeilen) - Alert-Logik & Severity
├── history.py          (184 Zeilen) - SQLite Datenbank
├── notifier_discord.py (194 Zeilen) - Discord Integration
├── notifier_telegram.py(147 Zeilen) - Telegram Integration
└── checks/
    ├── ping_check.py   ( 71 Zeilen) - ICMP Ping
    ├── tcp_check.py    ( 77 Zeilen) - TCP Port
    ├── http_check.py   ( 94 Zeilen) - HTTP/HTTPS
    ├── minecraft_check.py (78 Zeilen) - MC Protocol
    └── docker_check.py (159 Zeilen) - Docker API
```

## 🔧 Technologie-Stack

### Core
- Python 3.9+
- asyncio (async/await)
- FastAPI 0.109+
- Uvicorn (ASGI Server)

### Monitoring
- mcstatus 11.1+
- docker-py 7.0+
- aioping 0.3+
- aiohttp 3.9+

### Notifications
- requests 2.31+
- python-telegram-bot 20.7+

### Database
- sqlite3 (built-in)

## 🚀 Performance

- **Parallele Checks:** Alle Targets gleichzeitig
- **Non-Blocking I/O:** Asynchrone Architektur
- **Minimale Latenz:** ~7-10ms pro Check
- **Ressourcen:** <50MB RAM, <1% CPU

## 🌟 Besonderheiten

- **Kombinierte Docker+TCP Logik** - Container running aber Port zu = WARNING
- **Smart Alerts** - Nur bei Änderung, nicht bei jedem Check
- **Auto-Reconnect** - WebSocket Client verbindet automatisch neu
- **Gradient UI** - Modernes, professionelles Design
- **systemd Integration** - Production-ready Service
- **GitHub Actions** - CI/CD Pipeline included

---

**Entwickelt mit ❤️ von xXLuckyGamer04Xx**

Speziell für die Minecraft- und Gaming-Community!
