"""
Discord Webhook Notifier
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import logging
import requests
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class DiscordNotifier:
    """Discord Webhook Integration"""
    
    def __init__(self, webhook_url: str):
        """
        Args:
            webhook_url: Discord Webhook URL
        """
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url and webhook_url.startswith("https://"))
        
        if not self.enabled:
            logger.warning("Discord Webhook nicht konfiguriert oder ungültig")
    
    def send_alert(self, alert: Dict) -> bool:
        """
        Sendet Alert als Discord Embed
        
        Args:
            alert: Alert Dict von AlertManager
            
        Returns:
            True bei Erfolg
        """
        if not self.enabled:
            return False
        
        try:
            embed = self._create_embed(alert)
            
            payload = {
                "embeds": [embed],
                "username": "ServerWatch"
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204:
                logger.info(f"Discord Alert gesendet: {alert['target']}")
                return True
            else:
                logger.error(
                    f"Discord Fehler {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            logger.error(f"Discord Send Error: {e}")
            return False
    
    def _create_embed(self, alert: Dict) -> Dict:
        """Erstellt Discord Embed aus Alert"""
        
        # Farbe basierend auf Severity
        color_map = {
            "CRITICAL": 0xFF0000,  # Rot
            "WARNING": 0xFFA500,   # Orange
            "RECOVERY": 0x00FF00,  # Grün
            "INFO": 0x0099FF       # Blau
        }
        
        color = color_map.get(alert["severity"], 0x808080)
        
        # Titel
        emoji_map = {
            "CRITICAL": "🔴",
            "WARNING": "⚠️",
            "RECOVERY": "🟢",
            "INFO": "ℹ️"
        }
        emoji = emoji_map.get(alert["severity"], "❓")
        
        title = f"{emoji} {alert['severity']} - {alert['target']}"
        
        # Beschreibung
        description_parts = []
        
        if alert.get("previous_status") != "unknown":
            description_parts.append(
                f"Status: **{alert['previous_status']}** → **{alert['status']}**"
            )
        else:
            description_parts.append(f"Status: **{alert['status']}**")
        
        description = "\n".join(description_parts)
        
        # Fields
        fields = []
        details = alert.get("details", {})
        
        # Docker Status
        if "container_state" in details:
            fields.append({
                "name": "🐳 Container",
                "value": details["container_state"],
                "inline": True
            })
        
        # Port Status
        if "response_time_ms" in details:
            fields.append({
                "name": "🔌 Antwortzeit",
                "value": f"{details['response_time_ms']}ms",
                "inline": True
            })
        
        if "latency_ms" in details:
            fields.append({
                "name": "📡 Latenz",
                "value": f"{details['latency_ms']}ms",
                "inline": True
            })
        
        # Minecraft Spieler
        if "players_online" in details:
            fields.append({
                "name": "👥 Spieler",
                "value": f"{details['players_online']}/{details['players_max']}",
                "inline": True
            })
        
        # Version
        if details.get("version"):
            fields.append({
                "name": "📦 Version",
                "value": details["version"],
                "inline": True
            })
        
        # HTTP Code
        if "http_code" in details:
            fields.append({
                "name": "📡 HTTP",
                "value": str(details["http_code"]),
                "inline": True
            })
        
        # Fehler
        if details.get("error"):
            fields.append({
                "name": "❌ Fehler",
                "value": f"```{details['error']}```",
                "inline": False
            })
        
        # Downtime
        if alert.get("downtime_duration"):
            minutes = alert["downtime_duration"] // 60
            seconds = alert["downtime_duration"] % 60
            fields.append({
                "name": "⏱️ Ausfallzeit",
                "value": f"{minutes}min {seconds}s",
                "inline": True
            })
        
        # Host Info
        if details.get("host") and details.get("port"):
            fields.append({
                "name": "📍 Adresse",
                "value": f"{details['host']}:{details['port']}",
                "inline": False
            })
        
        # Embed zusammenbauen
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "fields": fields,
            "timestamp": alert["timestamp"],
            "footer": {
                "text": "ServerWatch v1.2.0 by xXLuckyGamer04Xx"
            }
        }
        
        return embed
