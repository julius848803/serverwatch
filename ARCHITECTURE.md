# 🏗️ ServerWatch - System-Architektur

## Übersicht

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING SERVER                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  ServerWatch v1.5.0                      │  │
│  │                 (Python + AsyncIO)                       │  │
│  └───┬──────────────────────────────────────────────────┬───┘  │
│      │                                                  │      │
│      ▼                                                  ▼      │
│  ┌─────────────────┐                          ┌──────────────┐ │
│  │  Monitor Loop   │                          │  Dashboard   │ │
│  │  (alle 7 Sek)   │                          │  (FastAPI)   │ │
│  └────┬────────────┘                          └──────┬───────┘ │
│       │                                              │         │
│       │  ┌──────────────────────────────────────────┤         │
│       │  │                                           │         │
│       ▼  ▼                                           ▼         │
│  ┌─────────────┐  ┌──────────────┐          ┌────────────┐   │
│  │   Checks    │  │   Alerting   │          │ WebSocket  │   │
│  │  - Ping     │  │   Manager    │          │  Clients   │   │
│  │  - TCP      │  │              │          │  (Browser) │   │
│  │  - MC       │  │ ┌──────────┐ │          └────────────┘   │
│  │  - Docker   │  │ │ Discord  │ │                            │
│  └──────┬──────┘  │ │ Telegram │ │                            │
│         │         │ └──────────┘ │                            │
│         ▼         └──────────────┘                            │
│  ┌─────────────┐                                              │
│  │  SQLite DB  │                                              │
│  │  Historie   │                                              │
│  └─────────────┘                                              │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ TCP/IP
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                          ▼                                       │
│                   vSERVER (Ziel)                                │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │         Docker Engine (Port 2376 - Remote API)          │  │
│  └────┬────────────────────────────────────────────────┬───┘  │
│       │                                                │       │
│       ▼                                                ▼       │
│  ┌──────────────────┐                       ┌───────────────┐ │
│  │  lobby-server    │                       │ citybuild-    │ │
│  │  (Port 25565)    │                       │  server       │ │
│  │  Minecraft       │                       │ (Port 25566)  │ │
│  └──────────────────┘                       └───────────────┘ │
│                                                                │
│  ┌──────────────────┐                       ┌───────────────┐ │
│  │  MySQL           │                       │ phpMyAdmin    │ │
│  │  (Port 3306)     │                       │ (Port 80)     │ │
│  └──────────────────┘                       └───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📡 Check-Flow (Minecraft Server)

```
Start Check
    │
    ├─► 1. TCP Port-Check (25565)
    │        ├─ Offen? → Weiter
    │        └─ Zu?    → Port-Status: OFFLINE
    │
    ├─► 2. Server List Ping (mcstatus)
    │        ├─ Erfolg → Spieleranzahl, MOTD, Version
    │        └─ Fehler → MC-Status: OFFLINE
    │
    ├─► 3. Docker API Query
    │        ├─ Container: running  → Docker: OK
    │        ├─ Container: exited   → Docker: DOWN
    │        └─ Container: fehlt    → Docker: MISSING
    │
    └─► 4. Kombinierte Bewertung
             │
             ├─ running + Port offen   → ✅ ONLINE
             ├─ running + Port zu      → ⚠️  WARNING (startet)
             ├─ exited  + Port zu      → 🔴 CRITICAL
             └─ fehlt                  → 🔴 CRITICAL
```

---

## 🔔 Alert-Flow

```
Check-Ergebnis
    │
    ├─► Statuswechsel erkannt?
    │        │
    │        ├─ ONLINE → OFFLINE
    │        │     │
    │        │     ├─► Severity bestimmen (CRITICAL/WARNING)
    │        │     ├─► Outage in DB starten
    │        │     ├─► Discord Embed senden
    │        │     ├─► Telegram Nachricht senden
    │        │     └─► WebSocket Broadcast
    │        │
    │        └─ OFFLINE → ONLINE
    │              │
    │              ├─► Outage beenden in DB
    │              ├─► Ausfallzeit berechnen
    │              ├─► Recovery-Benachrichtigung
    │              └─► WebSocket Broadcast
    │
    └─► Kein Statuswechsel
             └─► Nur Status-Historie updaten (kein Alert)
```

---

## 💾 Datenbank-Schema

### Outages Tabelle
```sql
CREATE TABLE outages (
    id                  INTEGER PRIMARY KEY,
    target_name         TEXT,
    target_type         TEXT,
    severity            TEXT,        -- CRITICAL, WARNING
    started_at          REAL,        -- Unix timestamp
    ended_at            REAL,        -- Unix timestamp oder NULL
    duration_seconds    INTEGER,     -- Berechnet bei Beendigung
    error_message       TEXT,
    docker_state        TEXT
);
```

### Status History Tabelle
```sql
CREATE TABLE status_history (
    id              INTEGER PRIMARY KEY,
    target_name     TEXT,
    timestamp       REAL,
    status          TEXT,           -- ONLINE, OFFLINE, WARNING
    latency_ms      REAL,
    players_online  INTEGER,
    players_max     INTEGER,
    docker_state    TEXT
);
```

---

## 🌐 WebSocket-Protokoll

### Client → Server
```json
{
  "type": "ping"
}
```

### Server → Client

**Initial Status:**
```json
{
  "type": "initial",
  "data": {
    "targets": { ... },
    "summary": { ... }
  }
}
```

**Status Update:**
```json
{
  "type": "status_update",
  "timestamp": "2024-03-10T20:15:00Z",
  "data": {
    "targets": { ... },
    "summary": { ... }
  }
}
```

**Outage Alert:**
```json
{
  "type": "outage",
  "data": {
    "target_name": "lobby-server",
    "severity": "CRITICAL",
    "docker_state": "exited"
  }
}
```

---

## 🔐 Sicherheits-Schichten

```
┌─────────────────────────────────────┐
│  1. Firewall (ufw)                  │
│     → Nur Monitoring-IP → Port 2376 │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  2. Docker TLS (optional)           │
│     → Zertifikatsbasierte Auth      │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  3. Read-Only Docker Access         │
│     → Nur Status abrufen            │
│     → Keine Container-Steuerung     │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  4. Environment Variables           │
│     → Credentials nicht in Git      │
└─────────────────────────────────────┘
```

---

## 📊 Performance-Metriken

**Check-Latenz:**
- Ping Check: ~10-50ms
- TCP Check: ~20-100ms
- Minecraft Check: ~100-300ms
- Docker API: ~50-150ms

**Parallel Checks:**
- Alle Targets gleichzeitig (asyncio.gather)
- Gesamtdauer: ~500ms für 5 Targets

**Dashboard Updates:**
- WebSocket Push: <10ms
- Keine Polling nötig
- Real-time ohne Verzögerung

**Datenbank:**
- SQLite mit Indices
- Cleanup: Alte Daten >30 Tage automatisch

---

## 🔄 Lifecycle

```
Start
  │
  ├─► Konfiguration laden
  ├─► Docker verbinden
  ├─► SQLite initialisieren
  ├─► Test-Benachrichtigung senden
  │
  ├─► Dashboard-Server starten (Port 8080)
  │     └─► WebSocket-Endpoint /ws
  │
  └─► Monitor-Loop starten
        │
        └─► Alle 7 Sekunden:
              │
              ├─► Parallel Checks für alle Targets
              ├─► Ergebnisse an AlertManager
              ├─► Status-Historie in DB
              ├─► Dashboard via WebSocket updaten
              │
              └─► Sleep bis nächster Zyklus
```

---

**Entwickelt von xXLuckyGamer04Xx**
