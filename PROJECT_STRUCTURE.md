# 📁 ServerWatch - Projektstruktur

```
serverwatch/
├── 📄 README.md                    # Hauptdokumentation
├── 📄 CHANGELOG.md                 # Versionshistorie
├── 📄 CONTRIBUTING.md              # Contribution Guidelines
├── 📄 LICENSE                      # MIT Lizenz
├── 📄 GITHUB_SETUP.md              # GitHub Repository Setup
│
├── 🔧 main.py                      # Entry Point (Start hier!)
├── 🔧 requirements.txt             # Python Dependencies
├── 🔧 .env.example                 # Environment Variablen Template
├── 🔧 .gitignore                   # Git Ignore Rules
│
├── 🚀 install.sh                   # Automatische Installation
├── 🚀 setup_git.sh                 # Git Repository Setup
│
├── 🐳 serverwatch.service          # systemd Service File
│
├── 📁 config/
│   └── servers.json                # Monitoring Targets Konfiguration
│
├── 📁 src/                         # Source Code
│   ├── __init__.py
│   ├── monitor.py                  # Haupt-Monitor Loop
│   ├── api.py                      # FastAPI Dashboard Backend
│   ├── alerting.py                 # Alert Manager & Logic
│   ├── history.py                  # SQLite Datenbank
│   ├── notifier_discord.py         # Discord Webhook
│   ├── notifier_telegram.py        # Telegram Bot
│   │
│   └── 📁 checks/                  # Check Module
│       ├── __init__.py
│       ├── ping_check.py           # ICMP Ping
│       ├── tcp_check.py            # TCP Port Check
│       ├── http_check.py           # HTTP/HTTPS Check
│       ├── minecraft_check.py      # Minecraft Protocol
│       └── docker_check.py         # Docker Remote API
│
├── 📁 dashboard/                   # Frontend
│   └── index.html                  # Live Dashboard (HTML+CSS+JS)
│
├── 📁 logs/                        # Log Files
│   ├── .gitkeep
│   └── monitor.log                 # (wird automatisch erstellt)
│
└── 📁 .github/                     # GitHub Actions
    └── workflows/
        └── ci.yml                  # CI/CD Pipeline
```

## 🔑 Wichtige Dateien

### Core Application

| Datei | Beschreibung |
|-------|-------------|
| `main.py` | Einstiegspunkt - startet Monitor & Dashboard |
| `src/monitor.py` | Haupt-Loop mit parallelen Checks |
| `src/api.py` | FastAPI + WebSocket Server |
| `src/alerting.py` | Alert-Logik & Statuswechsel-Erkennung |

### Checks

| Datei | Typ | Beschreibung |
|-------|-----|-------------|
| `ping_check.py` | ICMP | vServer Ping mit aioping |
| `tcp_check.py` | TCP | Port-Erreichbarkeit |
| `http_check.py` | HTTP | phpMyAdmin, Web-Services |
| `minecraft_check.py` | MC Protocol | Spieleranzahl, MOTD, Version |
| `docker_check.py` | Docker API | Container Status (running/exited) |

### Notifications

| Datei | Platform | Features |
|-------|----------|----------|
| `notifier_discord.py` | Discord | Rich Embeds, Farbcodierung |
| `notifier_telegram.py` | Telegram | HTML-Formatierung, Async |

### Configuration

| Datei | Zweck |
|-------|-------|
| `config/servers.json` | Targets, Intervall, Schwellenwerte |
| `.env` | Secrets (Webhooks, Tokens) |

## 📊 Datenfluss

```
main.py
  └─> ServerMonitor
        ├─> Check-Module (parallel)
        │     ├─> ping_check
        │     ├─> tcp_check
        │     ├─> minecraft_check
        │     │     └─> docker_check
        │     └─> http_check
        │
        ├─> AlertManager
        │     └─> Status-Wechsel?
        │           ├─> Discord
        │           └─> Telegram
        │
        ├─> HistoryDB (SQLite)
        │
        └─> DashboardAPI
              └─> WebSocket Broadcast
```

## 🚀 Start-Reihenfolge

1. `load_dotenv()` - Lädt .env
2. `ServerMonitor()` - Init Checker, Notifiers, DB
3. `DashboardAPI()` - FastAPI Server Setup
4. `asyncio.gather()` - Parallele Tasks:
   - Monitor Loop (alle 7s)
   - Dashboard Server (Port 8000)
   - WebSocket Broadcast (alle 2s)

## 💾 Datenbank-Schema

**incidents** - Ausfälle
- target_name, status, severity
- started_at, resolved_at, duration_seconds
- details, error_message

**status_history** - Alle Checks
- target_name, status, timestamp
- latency_ms, players_online, details

## 🎨 Dashboard-Architektur

**Frontend:** Vanilla JS + WebSocket
- Auto-Reconnect bei Disconnect
- Live Status-Updates alle 2s
- Responsive Grid Layout

**Backend:** FastAPI
- `/` - Dashboard HTML
- `/api/status` - REST Endpoint
- `/ws` - WebSocket für Live-Updates

## 📝 Logging

- **Console:** INFO Level
- **File:** `logs/monitor.log` (INFO+)
- **systemd:** `journalctl -u serverwatch -f`

---

**Entwickelt von xXLuckyGamer04Xx**
