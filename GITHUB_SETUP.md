# 🚀 GitHub Repository Setup für ServerWatch

## Schritt 1: GitHub Repository erstellen

1. Gehe zu [github.com](https://github.com) und logge dich ein
2. Klicke auf das **+** Symbol oben rechts → **New repository**
3. Repository Name: `serverwatch`
4. Description: `Advanced Minecraft Server Monitoring with Docker Integration`
5. **Public** oder **Private** (deine Wahl)
6. ⚠️ **NICHT** "Initialize with README" ankreuzen!
7. Klicke **Create repository**

## Schritt 2: Repository URL kopieren

Nach der Erstellung siehst du eine URL wie:
```
https://github.com/DEIN-USERNAME/serverwatch.git
```

Kopiere diese URL!

## Schritt 3: Lokales Projekt hochladen

### Option A: Automatisches Setup-Script

```bash
cd serverwatch
./setup_git.sh
```

Das Script fragt nach der Repository URL - füge deine kopierte URL ein.

### Option B: Manuell

```bash
cd serverwatch

# Git initialisieren
git init

# Alle Dateien hinzufügen
git add .

# Initial Commit
git commit -m "Initial commit: ServerWatch v1.2.0"

# Branch umbenennen
git branch -M main

# Remote hinzufügen (ersetze URL!)
git remote add origin https://github.com/DEIN-USERNAME/serverwatch.git

# Hochladen
git push -u origin main
```

## Schritt 4: GitHub Repository konfigurieren

### Secrets für CI/CD (Optional)

Falls du GitHub Actions nutzen willst:

1. Gehe zu **Settings** → **Secrets and variables** → **Actions**
2. Klicke **New repository secret**
3. Füge hinzu:
   - `DISCORD_WEBHOOK_URL` (für Tests)
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### Branch Protection (Empfohlen für Teams)

1. **Settings** → **Branches** → **Add rule**
2. Branch name pattern: `main`
3. Aktiviere:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging

## Schritt 5: README Badges hinzufügen

Füge am Anfang der README.md hinzu:

```markdown
[![CI](https://github.com/DEIN-USERNAME/serverwatch/actions/workflows/ci.yml/badge.svg)](https://github.com/DEIN-USERNAME/serverwatch/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

## Schritt 6: Weitere Verbesserungen

### Topics hinzufügen

Auf der Repository-Startseite:
- Klicke auf das Zahnrad bei "About"
- Füge Topics hinzu: `minecraft`, `monitoring`, `docker`, `discord`, `telegram`, `python`

### Social Preview Image

Erstelle ein cooles Banner-Bild und lade es hoch:
- Settings → General → Social Preview → Upload an image

## 🎉 Fertig!

Dein ServerWatch Repository ist jetzt live auf GitHub!

### Nächste Schritte:

- ⭐ Gib dem Projekt einen Star
- 📢 Teile es mit Freunden
- 🐛 Erstelle Issues für Bugs/Features
- 🔀 Akzeptiere Pull Requests von Contributors

---

**Viel Erfolg mit deinem ServerWatch Repository!** 🚀

_Developed by xXLuckyGamer04Xx_
