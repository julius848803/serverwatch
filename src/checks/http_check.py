"""
HTTP/HTTPS Check Module
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import asyncio
import logging
import time
from typing import Dict
import aiohttp

logger = logging.getLogger(__name__)


async def check_http(host: str, port: int, use_https: bool = False, timeout: float = 10.0) -> Dict:
    """
    Prüft HTTP(S) Endpoint
    
    Args:
        host: Server IP/Hostname
        port: Port
        use_https: True für HTTPS, False für HTTP
        timeout: Timeout in Sekunden
        
    Returns:
        Dict mit Status, HTTP Code, Antwortzeit
    """
    result = {
        "status": "unknown",
        "http_code": None,
        "response_time_ms": None,
        "error": None
    }
    
    protocol = "https" if use_https else "http"
    url = f"{protocol}://{host}:{port}"
    
    start_time = time.time()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=timeout),
                ssl=False  # SSL Verification deaktivieren für self-signed certs
            ) as response:
                response_time = (time.time() - start_time) * 1000
                
                result["http_code"] = response.status
                result["response_time_ms"] = round(response_time, 2)
                
                # Status basierend auf HTTP Code
                if 200 <= response.status < 400:
                    result["status"] = "online"
                elif 400 <= response.status < 500:
                    result["status"] = "warning"
                    result["error"] = f"HTTP {response.status}"
                else:
                    result["status"] = "offline"
                    result["error"] = f"HTTP {response.status}"
                
                logger.debug(
                    f"HTTP {url} - Code {result['http_code']}, "
                    f"{result['response_time_ms']}ms"
                )
                
    except asyncio.TimeoutError:
        result["status"] = "offline"
        result["error"] = "Timeout"
        logger.warning(f"HTTP Timeout zu {url}")
        
    except aiohttp.ClientConnectorError as e:
        result["status"] = "offline"
        result["error"] = "Connection refused"
        logger.warning(f"HTTP Connection Error zu {url}: {e}")
        
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        logger.error(f"HTTP Check Fehler für {url}: {e}")
    
    return result
