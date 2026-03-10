"""
Telegram Bot Notifier
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import logging
import asyncio
from typing import Dict, Optional
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Telegram Bot Integration"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Args:
            bot_token: Telegram Bot Token
            chat_id: Chat ID für Benachrichtigungen
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot: Optional[Bot] = None
        self.enabled = False
        
        if bot_token and chat_id:
            try:
                self.bot = Bot(token=bot_token)
                self.enabled = True
                logger.info("Telegram Bot initialisiert")
            except Exception as e:
                logger.error(f"Telegram Bot Init Fehler: {e}")
        else:
            logger.warning("Telegram Bot nicht konfiguriert")
    
    async def send_alert(self, alert: Dict) -> bool:
        """
        Sendet Alert via Telegram
        
        Args:
            alert: Alert Dict von AlertManager
            
        Returns:
            True bei Erfolg
        """
        if not self.enabled or not self.bot:
            return False
        
        try:
            message = self._format_message(alert)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            
            logger.info(f"Telegram Alert gesendet: {alert['target']}")
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram API Fehler: {e}")
            return False
        except Exception as e:
            logger.error(f"Telegram Send Error: {e}")
            return False
    
    def _format_message(self, alert: Dict) -> str:
        """Formatiert Alert als Telegram-Nachricht (HTML)"""
        
        emoji_map = {
            "CRITICAL": "🔴",
            "WARNING": "⚠️",
            "RECOVERY": "🟢",
            "INFO": "ℹ️"
        }
        
        emoji = emoji_map.get(alert["severity"], "❓")
        
        lines = [
            f"{emoji} <b>{alert['severity']}</b> – {alert['target']}",
            ""
        ]
        
        details = alert.get("details", {})
        
        # Docker
        if "container_state" in details:
            lines.append(f"🐳 Container: <code>{details['container_state']}</code>")
        
        # Port/Latenz
        if "response_time_ms" in details:
            lines.append(f"🔌 Port: ✅ ({details['response_time_ms']}ms)")
        elif "latency_ms" in details:
            lines.append(f"📡 Latenz: {details['latency_ms']}ms")
        
        # Minecraft
        if "players_online" in details:
            lines.append(
                f"👥 Spieler: {details['players_online']}/{details['players_max']}"
            )
        
        if details.get("version"):
            lines.append(f"📦 Version: {details['version']}")
        
        # HTTP
        if "http_code" in details:
            lines.append(f"📡 HTTP: {details['http_code']}")
        
        # Fehler
        if details.get("error"):
            lines.append(f"❌ {details['error']}")
        
        # Downtime
        if alert.get("downtime_duration"):
            minutes = alert["downtime_duration"] // 60
            seconds = alert["downtime_duration"] % 60
            lines.append(f"⏱️ Ausfall: {minutes}min {seconds}s")
        
        # Timestamp
        from datetime import datetime
        timestamp = datetime.fromisoformat(alert["timestamp"]).strftime("%H:%M:%S")
        lines.append(f"🕐 {timestamp}")
        
        return "\n".join(lines)
    
    async def test_connection(self) -> bool:
        """Testet Telegram Bot Verbindung"""
        if not self.enabled or not self.bot:
            return False
        
        try:
            me = await self.bot.get_me()
            logger.info(f"Telegram Bot aktiv: @{me.username}")
            return True
        except Exception as e:
            logger.error(f"Telegram Test fehlgeschlagen: {e}")
            return False
