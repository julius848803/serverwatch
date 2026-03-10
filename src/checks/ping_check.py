"""
Ping Check Module - ICMP Ping für vServer Host
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import asyncio
import logging
from typing import Dict, Optional

try:
    import aioping
except ImportError:
    aioping = None

logger = logging.getLogger(__name__)


async def check_ping(host: str, timeout: float = 5.0) -> Dict:
    """
    Führt einen ICMP Ping auf den Host aus
    
    Args:
        host: IP-Adresse oder Hostname
        timeout: Timeout in Sekunden
        
    Returns:
        Dict mit Status, Latenz und Fehler
    """
    result = {
        "status": "unknown",
        "latency_ms": None,
        "error": None
    }
    
    if aioping is None:
        result["status"] = "error"
        result["error"] = "aioping nicht installiert"
        return result
    
    try:
        # Ping ausführen
        delay = await aioping.ping(host, timeout=timeout)
        
        if delay is not None:
            result["status"] = "online"
            result["latency_ms"] = round(delay * 1000, 2)  # Convert to ms
            logger.debug(f"Ping zu {host}: {result['latency_ms']}ms")
        else:
            result["status"] = "offline"
            result["error"] = "Keine Antwort"
            
    except asyncio.TimeoutError:
        result["status"] = "offline"
        result["error"] = "Timeout"
        logger.warning(f"Ping Timeout zu {host}")
        
    except PermissionError:
        # ICMP benötigt root - fallback zu TCP
        result["status"] = "error"
        result["error"] = "Keine ICMP Berechtigung (root benötigt)"
        logger.error(f"ICMP Ping benötigt root-Rechte für {host}")
        
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        logger.error(f"Ping Fehler für {host}: {e}")
    
    return result
