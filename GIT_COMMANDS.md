# 🎯 ServerWatch - Git Commands Cheat Sheet

## Erstes Setup (einmalig)

```bash
# 1. Repository auf GitHub erstellen (siehe GITHUB_SETUP.md)

# 2. Lokales Projekt initialisieren
cd serverwatch
git init
git add .
git commit -m "Initial commit: ServerWatch v1.2.0"
git branch -M main

# 3. Mit GitHub verbinden (DEINE URL einsetzen!)
git remote add origin https://github.com/DEIN-USERNAME/serverwatch.git
git push -u origin main
```

## Täglicher Workflow

### Änderungen hochladen

```bash
# Status prüfen
git status

# Dateien zum Commit hinzufügen
git add .                          # Alle Dateien
git add src/monitor.py             # Einzelne Datei

# Commit erstellen
git commit -m "Add: Neue Funktion X"

# Hochladen
git push
```

### Änderungen herunterladen

```bash
# Aktualisieren
git pull
```

## Commit Message Guidelines

Verwende klare Präfixe:

```bash
git commit -m "Add: WebSocket reconnect feature"
git commit -m "Fix: Docker connection timeout"
git commit -m "Update: Discord embed formatting"
git commit -m "Docs: Add installation guide"
git commit -m "Refactor: Simplify alert logic"
```

## Branches (für Features)

```bash
# Neuen Branch erstellen
git checkout -b feature/discord-v2

# Zum Branch wechseln
git checkout feature/discord-v2

# Branch hochladen
git push -u origin feature/discord-v2

# Zurück zu main
git checkout main

# Branch mergen
git merge feature/discord-v2

# Branch löschen (lokal)
git branch -d feature/discord-v2

# Branch löschen (remote)
git push origin --delete feature/discord-v2
```

## Versionen & Tags

```bash
# Tag erstellen
git tag -a v1.2.0 -m "Release 1.2.0"

# Tags hochladen
git push --tags

# Alle Tags anzeigen
git tag
```

## Nützliche Befehle

```bash
# Commit History
git log --oneline --graph --all

# Letzte Änderungen
git diff

# Datei rückgängig machen
git checkout -- datei.py

# Letzten Commit rückgängig (behält Änderungen)
git reset --soft HEAD~1

# Remote URL prüfen
git remote -v

# Remote URL ändern
git remote set-url origin https://neue-url.git
```

## .gitignore erweitern

Füge in `.gitignore` hinzu:

```
# Secrets
.env
*.env

# Logs
logs/*.log
*.log

# Database
*.db
serverwatch.db

# Python
__pycache__/
*.pyc
```

## Pull Requests (GitHub)

1. Fork auf GitHub
2. Clone deinen Fork:
   ```bash
   git clone https://github.com/DEIN-USERNAME/serverwatch.git
   ```
3. Branch erstellen:
   ```bash
   git checkout -b fix/bug-description
   ```
4. Änderungen machen & committen
5. Push zu deinem Fork:
   ```bash
   git push origin fix/bug-description
   ```
6. Pull Request auf GitHub erstellen

## Probleme beheben

### Merge Conflict

```bash
# Konflikt-Dateien manuell bearbeiten
nano datei-mit-konflikt.py

# Nach Bearbeitung
git add datei-mit-konflikt.py
git commit -m "Resolve merge conflict"
```

### Falscher Commit

```bash
# Letzten Commit rückgängig
git reset --soft HEAD~1

# Änderungen neu commiten
git add .
git commit -m "Korrekte Message"
```

### Datei aus Git entfernen (aber lokal behalten)

```bash
# Aus Git entfernen, lokal behalten
git rm --cached .env

# Commit
git commit -m "Remove .env from tracking"
git push
```

## GitHub Actions prüfen

```bash
# Nach Push automatisch ausgeführt
# Status auf GitHub: Actions Tab

# Lokal testen (Syntax)
python -m py_compile main.py
```

## Tipps

✅ **Häufig committen** - Kleine, logische Commits
✅ **Klare Messages** - Beschreibe was & warum
✅ **Vor Push testen** - `python main.py` lokal ausführen
✅ **Branch Protection** - Für main Branch aktivieren
✅ **Pull Requests** - Bei Teams nutzen

❌ **Nicht** `.env` committen - Secrets geheim halten!
❌ **Nicht** große Binaries - Nur Code & Config
❌ **Nicht** `git push -f` - Force Push vermeiden

---

**Happy Coding! 🚀**

_by xXLuckyGamer04Xx_
