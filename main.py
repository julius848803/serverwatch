#!/usr/bin/env python3
"""
ServerWatch - Main Entry Point
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Python Path Setup
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.monitor import ServerMonitor
from src.api import DashboardAPI

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Hauptfunktion"""
    logger.info("=" * 60)
    logger.info("ServerWatch v1.2.0 by xXLuckyGamer04Xx")
    logger.info("=" * 60)
    
    # Environment laden
    load_dotenv()
    
    env = {
        "DISCORD_WEBHOOK_URL": os.getenv("DISCORD_WEBHOOK_URL"),
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "DOCKER_HOST": os.getenv("DOCKER_HOST"),
        "VSERVER_IP": os.getenv("VSERVER_IP"),
        "DASHBOARD_PORT": int(os.getenv("DASHBOARD_PORT", 8000))
    }
    
    # Config Path
    config_path = Path(__file__).parent / "config" / "servers.json"
    
    if not config_path.exists():
        logger.error(f"Konfiguration nicht gefunden: {config_path}")
        return
    
    # Monitor initialisieren
    try:
        monitor = ServerMonitor(str(config_path), env)
        logger.info("Monitor initialisiert")
    except Exception as e:
        logger.error(f"Monitor Init Fehler: {e}", exc_info=True)
        return
    
    # Dashboard API
    dashboard = DashboardAPI(monitor, port=env["DASHBOARD_PORT"])
    
    # Telegram Test
    if monitor.telegram:
        logger.info("Teste Telegram Verbindung...")
        await monitor.telegram.test_connection()
    
    # Tasks starten
    try:
        # Monitor Loop & Dashboard parallel
        monitor_task = asyncio.create_task(monitor.run_loop())
        dashboard_task = asyncio.create_task(dashboard.run())
        
        # Broadcast Loop für WebSocket
        async def broadcast_loop():
            while True:
                await asyncio.sleep(2)
                await dashboard.broadcast_status()
        
        broadcast_task = asyncio.create_task(broadcast_loop())
        
        logger.info("Alle Services gestartet")
        
        # Auf Tasks warten
        await asyncio.gather(
            monitor_task,
            dashboard_task,
            broadcast_task
        )
        
    except KeyboardInterrupt:
        logger.info("Shutdown durch Benutzer...")
    except Exception as e:
        logger.error(f"Kritischer Fehler: {e}", exc_info=True)
    finally:
        monitor.stop()
        logger.info("ServerWatch beendet")


if __name__ == "__main__":
    asyncio.run(main())
