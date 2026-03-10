"""
Main Monitoring Loop
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional
from datetime import datetime

from checks.ping_check import check_ping
from checks.tcp_check import check_tcp
from checks.minecraft_check import check_minecraft
from checks.docker_check import DockerChecker
from checks.http_check import check_http

from alerting import AlertManager
from notifier_discord import DiscordNotifier
from notifier_telegram import TelegramNotifier
from history import HistoryDB

logger = logging.getLogger(__name__)


class ServerMonitor:
    """Haupt-Monitoring Klasse"""
    
    def __init__(self, config_path: str, env: Dict):
        """
        Args:
            config_path: Pfad zur servers.json
            env: Environment Variablen
        """
        self.config_path = config_path
        self.env = env
        self.config: Dict = {}
        self.running = False
        
        # Components
        self.docker_checker: Optional[DockerChecker] = None
        self.alert_manager: Optional[AlertManager] = None
        self.discord: Optional[DiscordNotifier] = None
        self.telegram: Optional[TelegramNotifier] = None
        self.history: Optional[HistoryDB] = None
        
        # Status Cache für Dashboard
        self.current_status: Dict[str, Dict] = {}
        
        self._load_config()
        self._init_components()
    
    def _load_config(self):
        """Lädt Konfiguration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Konfiguration geladen: {len(self.config.get('targets', []))} Targets")
        except Exception as e:
            logger.error(f"Fehler beim Laden der Config: {e}")
            raise
    
    def _init_components(self):
        """Initialisiert alle Komponenten"""
        
        # Alert Manager
        threshold = self.config.get("critical_threshold_percent", 75)
        self.alert_manager = AlertManager(threshold)
        
        # Docker Checker
        docker_host = self.env.get("DOCKER_HOST") or self.config.get("docker_host")
        if docker_host:
            self.docker_checker = DockerChecker(docker_host)
        
        # Notifiers
        discord_webhook = self.env.get("DISCORD_WEBHOOK_URL")
        if discord_webhook:
            self.discord = DiscordNotifier(discord_webhook)
        
        telegram_token = self.env.get("TELEGRAM_BOT_TOKEN")
        telegram_chat = self.env.get("TELEGRAM_CHAT_ID")
        if telegram_token and telegram_chat:
            self.telegram = TelegramNotifier(telegram_token, telegram_chat)
        
        # History DB
        self.history = HistoryDB()
        
        logger.info("Alle Komponenten initialisiert")
    
    async def check_target(self, target: Dict) -> Dict:
        """Führt Check für ein Target aus"""
        target_type = target.get("type")
        name = target.get("name")
        host = target.get("host")
        port = target.get("port")
        
        result = {
            "name": name,
            "type": target_type,
            "status": "unknown",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            if target_type == "ping":
                check_result = await check_ping(host)
                result.update(check_result)
            
            elif target_type == "tcp":
                check_result = await check_tcp(host, port)
                result.update(check_result)
            
            elif target_type == "http":
                use_https = port == 443
                check_result = await check_http(host, port, use_https)
                result.update(check_result)
            
            elif target_type == "minecraft":
                mc_result = await check_minecraft(host, port)
                result.update(mc_result)
                
                container_name = target.get("docker_container")
                if container_name and self.docker_checker:
                    docker_result = await self.docker_checker.check_container(container_name)
                    result.update({
                        "container_state": docker_result.get("container_state"),
                        "container_health": docker_result.get("container_health"),
                        "uptime_seconds": docker_result.get("uptime_seconds")
                    })
                    
                    result["status"] = self._combine_minecraft_status(
                        mc_result.get("status"),
                        docker_result.get("container_state")
                    )
            
            result["host"] = host
            if port:
                result["port"] = port
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f"Check Fehler für {name}: {e}")
        
        return result
    
    def _combine_minecraft_status(self, mc_status: str, container_state: Optional[str]) -> str:
        """Kombiniert Minecraft + Docker Status"""
        if not container_state:
            return mc_status
        
        if container_state == "running" and mc_status == "online":
            return "online"
        
        if container_state == "running" and mc_status == "offline":
            return "warning"
        
        if container_state in ["exited", "dead"]:
            return "offline"
        
        if container_state == "restarting":
            return "warning"
        
        return "critical"
    
    async def check_all_targets(self) -> List[Dict]:
        """Prüft alle Targets parallel"""
        targets = self.config.get("targets", [])
        tasks = [self.check_target(target) for target in targets]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        for r in results:
            if isinstance(r, Exception):
                logger.error(f"Check Exception: {r}")
            else:
                valid_results.append(r)
        
        return valid_results
    
    async def process_results(self, results: List[Dict]):
        """Verarbeitet Check-Ergebnisse"""
        for result in results:
            target_name = result["name"]
            status = result["status"]
            
            # Status Cache aktualisieren
            self.current_status[target_name] = result
            
            # Alert Check
            alert = self.alert_manager.check_and_alert(
                target_name,
                status,
                result
            )
            
            # Bei Statuswechsel
            if alert:
                # DB speichern
                if self.history:
                    self.history.log_incident(alert)
                
                # Benachrichtigungen
                await self._send_notifications(alert)
            
            # Status History
            if self.history:
                self.history.log_status(target_name, status, result)
    
    async def _send_notifications(self, alert: Dict):
        """Sendet Benachrichtigungen"""
        # Discord
        if self.discord:
            try:
                self.discord.send_alert(alert)
            except Exception as e:
                logger.error(f"Discord Fehler: {e}")
        
        # Telegram
        if self.telegram:
            try:
                await self.telegram.send_alert(alert)
            except Exception as e:
                logger.error(f"Telegram Fehler: {e}")
    
    async def run_loop(self):
        """Haupt-Monitor-Loop"""
        interval = self.config.get("interval_seconds", 7)
        self.running = True
        
        logger.info(f"Monitor-Loop gestartet (Intervall: {interval}s)")
        
        while self.running:
            try:
                # Checks ausführen
                results = await self.check_all_targets()
                
                # Results verarbeiten
                await self.process_results(results)
                
                # Warten
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Loop Fehler: {e}", exc_info=True)
                await asyncio.sleep(interval)
    
    def stop(self):
        """Stoppt Monitoring"""
        self.running = False
        
        if self.docker_checker:
            self.docker_checker.close()
        
        if self.history:
            self.history.close()
        
        logger.info("Monitor gestoppt")
