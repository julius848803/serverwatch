"""
Docker Container Check Module
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import logging
from typing import Dict, Optional
import docker
from docker.errors import DockerException, NotFound, APIError

logger = logging.getLogger(__name__)


class DockerChecker:
    """Docker Remote API Client für Container-Status"""
    
    def __init__(self, docker_host: str):
        """
        Args:
            docker_host: Docker Host URL (z.B. tcp://123.456.789.0:2376)
        """
        self.docker_host = docker_host
        self.client: Optional[docker.DockerClient] = None
        self._connect()
    
    def _connect(self):
        """Verbindung zur Docker API herstellen"""
        try:
            self.client = docker.DockerClient(base_url=self.docker_host)
            # Test-Ping
            self.client.ping()
            logger.info(f"Docker API verbunden: {self.docker_host}")
        except DockerException as e:
            logger.error(f"Docker API Verbindung fehlgeschlagen: {e}")
            self.client = None
        except Exception as e:
            logger.error(f"Unerwarteter Fehler bei Docker-Verbindung: {e}")
            self.client = None
    
    async def check_container(self, container_name: str) -> Dict:
        """
        Prüft Container-Status
        
        Args:
            container_name: Name des Containers
            
        Returns:
            Dict mit Status, State, Health
        """
        result = {
            "status": "unknown",
            "container_state": None,
            "container_health": None,
            "uptime_seconds": None,
            "error": None
        }
        
        if self.client is None:
            result["status"] = "error"
            result["error"] = "Docker API nicht verbunden"
            return result
        
        try:
            # Container abrufen
            container = self.client.containers.get(container_name)
            
            # Status auslesen
            container.reload()  # Aktualisiere Status
            state = container.attrs['State']
            
            result["container_state"] = state['Status']  # running, exited, restarting, etc.
            
            # Health Check (falls vorhanden)
            if 'Health' in state:
                result["container_health"] = state['Health']['Status']
            
            # Uptime berechnen (falls running)
            if state['Status'] == 'running' and 'StartedAt' in state:
                from datetime import datetime
                started = datetime.fromisoformat(state['StartedAt'].replace('Z', '+00:00'))
                uptime = (datetime.now(started.tzinfo) - started).total_seconds()
                result["uptime_seconds"] = int(uptime)
            
            # Gesamtstatus bestimmen
            if state['Status'] == 'running':
                if result["container_health"] == 'unhealthy':
                    result["status"] = "warning"
                else:
                    result["status"] = "online"
            elif state['Status'] in ['exited', 'dead']:
                result["status"] = "offline"
            elif state['Status'] == 'restarting':
                result["status"] = "warning"
            else:
                result["status"] = "unknown"
            
            logger.debug(
                f"Container {container_name}: {result['container_state']} "
                f"(Health: {result['container_health']})"
            )
            
        except NotFound:
            result["status"] = "critical"
            result["error"] = "Container nicht gefunden"
            logger.error(f"Container {container_name} existiert nicht")
            
        except APIError as e:
            result["status"] = "error"
            result["error"] = f"Docker API Error: {str(e)}"
            logger.error(f"Docker API Fehler für {container_name}: {e}")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f"Docker Check Fehler für {container_name}: {e}")
        
        return result
    
    def close(self):
        """Schließt die Docker Client Verbindung"""
        if self.client:
            self.client.close()
            logger.info("Docker Client geschlossen")
