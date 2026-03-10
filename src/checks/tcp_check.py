"""
TCP Port Check Module
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import asyncio
import logging
import time
from typing import Dict

logger = logging.getLogger(__name__)


async def check_tcp(host: str, port: int, timeout: float = 5.0) -> Dict:
    """
    Prüft ob ein TCP Port erreichbar ist
    
    Args:
        host: IP-Adresse oder Hostname
        port: TCP Port
        timeout: Timeout in Sekunden
        
    Returns:
        Dict mit Status, Antwortzeit und Fehler
    """
    result = {
        "status": "unknown",
        "response_time_ms": None,
        "error": None
    }
    
    start_time = time.time()
    
    try:
        # TCP Connection versuchen
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        
        response_time = (time.time() - start_time) * 1000
        
        result["status"] = "online"
        result["response_time_ms"] = round(response_time, 2)
        
        # Verbindung sauber schließen
        writer.close()
        await writer.wait_closed()
        
        logger.debug(f"TCP {host}:{port} erreichbar in {result['response_time_ms']}ms")
        
    except asyncio.TimeoutError:
        result["status"] = "offline"
        result["error"] = "Connection Timeout"
        logger.warning(f"TCP Timeout zu {host}:{port}")
        
    except ConnectionRefusedError:
        result["status"] = "offline"
        result["error"] = "Connection refused"
        logger.warning(f"TCP Connection refused zu {host}:{port}")
        
    except OSError as e:
        result["status"] = "offline"
        result["error"] = f"OS Error: {str(e)}"
        logger.warning(f"TCP OS Error zu {host}:{port}: {e}")
        
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        logger.error(f"TCP Check Fehler für {host}:{port}: {e}")
    
    return result
