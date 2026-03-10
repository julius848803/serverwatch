# 🚀 ServerWatch - Schnellstart

## 📦 In 5 Minuten startklar

### 1️⃣ Installation (30 Sekunden)

```bash
cd serverwatch
bash install.sh
```

### 2️⃣ Konfiguration (2 Minuten)

**Discord Webhook erstellen:**
- Discord → Server-Einstellungen → Integrationen → Webhook erstellen
- URL kopieren

**Telegram Bot erstellen:**
- Mit @BotFather chatten → `/newbot`
- Bot-Token kopieren
- Bot zur Gruppe hinzufügen
- Chat-ID mit: `curl https://api.telegram.org/bot<TOKEN>/getUpdates`

**.env anpassen:**
```bash
nano .env
```

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/DEINE_ID/DEIN_TOKEN
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF...
TELEGRAM_CHAT_ID=-1001234567890
VSERVER_IP=123.456.789.0
DOCKER_HOST=tcp://123.456.789.0:2376
```

**config/servers.json anpassen:**
```bash
nano config/servers.json
```

Ersetze `123.456.789.0` mit deiner vServer-IP!

### 3️⃣ Docker Remote API aktivieren (1 Minute)

**Auf dem vServer:**

```bash
# Docker Remote API aktivieren
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/override.conf
```

Einfügen:
```ini
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376
```

```bash
# Anwenden
sudo systemctl daemon-reload
sudo systemctl restart docker

# Firewall (NUR Monitoring-Server erlauben!)
sudo ufw allow from MONITORING_IP to any port 2376 proto tcp
```

### 4️⃣ Starten! (10 Sekunden)

**Option A: Manuell**
```bash
source venv/bin/activate
python3 main.py
```

**Option B: Als Service**
```bash
sudo systemctl start serverwatch
sudo systemctl enable serverwatch

# Logs ansehen:
sudo journalctl -u serverwatch -f
```

### 5️⃣ Dashboard öffnen

```
http://DEIN_MONITORING_SERVER:8080
```

---

## ✅ Testen

```bash
# Konfiguration testen
python3 test_config.py

# Kurzer Test (manuelle Ausführung)
python3 main.py
# STRG+C zum Beenden

# Service-Logs
sudo journalctl -u serverwatch -f
```

---

## 🔧 Troubleshooting 1-Minute Fixes

### "Docker connection failed"
```bash
# Auf vServer prüfen:
sudo netstat -tlnp | grep 2376
sudo systemctl restart docker
```

### "Discord Webhook error"
```bash
# Webhook testen:
curl -X POST "DEINE_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content":"Test von ServerWatch"}'
```

### "Dashboard nicht erreichbar"
```bash
# Port öffnen:
sudo ufw allow 8080/tcp

# Läuft das Programm?
ps aux | grep python
```

---

## 📱 Erste Benachrichtigung testen

1. Stoppe einen Minecraft-Container:
   ```bash
   docker stop lobby-server
   ```

2. Warte 7-14 Sekunden

3. Du solltest eine Discord + Telegram Benachrichtigung erhalten! 🎉

4. Container wieder starten:
   ```bash
   docker start lobby-server
   ```

5. Nach 7 Sekunden → Recovery-Benachrichtigung ✅

---

## 🎯 Was wird überwacht?

Nach dem Start überwacht ServerWatch automatisch:

✅ vServer-Erreichbarkeit (Ping)  
✅ Minecraft-Server (Spieleranzahl + Docker Status)  
✅ MySQL-Datenbank  
✅ phpMyAdmin  

**Alle 7 Sekunden!**

Benachrichtigungen nur bei Statuswechsel (kein Spam).

---

## 📊 Dashboard Features

- 🟢 Echtzeit-Status aller Services
- 📈 Spieleranzahl live
- 🐳 Docker Container Status
- 📉 Ausfall-Historie
- ⚡ WebSocket Updates (keine Seitenreload nötig)

---

## 🆘 Support

Probleme? Prüfe:
1. `python3 test_config.py` - Alles grün?
2. `.env` - Credentials korrekt?
3. `config/servers.json` - IP richtig?
4. Docker Remote API - Port 2376 offen?

---

**Viel Erfolg! 🚀**

*Entwickelt von xXLuckyGamer04Xx*
