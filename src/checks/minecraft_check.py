"""
Minecraft Server Check Module
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import asyncio
import logging
from typing import Dict, Optional
from mcstatus import JavaServer

logger = logging.getLogger(__name__)


async def check_minecraft(host: str, port: int, timeout: float = 5.0) -> Dict:
    """
    Prüft Minecraft Server Status via Server List Ping
    
    Args:
        host: Server IP
        port: Server Port
        timeout: Timeout in Sekunden
        
    Returns:
        Dict mit Status, Spieleranzahl, MOTD, Version
    """
    result = {
        "status": "unknown",
        "players_online": 0,
        "players_max": 0,
        "version": None,
        "motd": None,
        "latency_ms": None,
        "error": None
    }
    
    try:
        # Minecraft Server Objekt erstellen
        server = JavaServer.lookup(f"{host}:{port}")
        
        # Status abrufen (async)
        status = await asyncio.wait_for(
            asyncio.to_thread(server.status),
            timeout=timeout
        )
        
        result["status"] = "online"
        result["players_online"] = status.players.online
        result["players_max"] = status.players.max
        result["version"] = status.version.name
        result["motd"] = status.description if hasattr(status, 'description') else "N/A"
        result["latency_ms"] = round(status.latency, 2)
        
        logger.debug(
            f"MC Server {host}:{port} - "
            f"{result['players_online']}/{result['players_max']} Spieler, "
            f"Version: {result['version']}"
        )
        
    except asyncio.TimeoutError:
        result["status"] = "offline"
        result["error"] = "Server antwortet nicht (Timeout)"
        logger.warning(f"MC Server {host}:{port} Timeout")
        
    except ConnectionRefusedError:
        result["status"] = "offline"
        result["error"] = "Port geschlossen"
        logger.warning(f"MC Server {host}:{port} Port geschlossen")
        
    except OSError as e:
        result["status"] = "offline"
        result["error"] = f"Netzwerkfehler: {str(e)}"
        logger.warning(f"MC Server {host}:{port} Netzwerkfehler: {e}")
        
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        logger.error(f"MC Check Fehler für {host}:{port}: {e}")
    
    return result
