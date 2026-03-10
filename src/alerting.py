"""
ServerWatch - Alerting Manager
Author: xXLuckyGamer04Xx
Version: 1.4.0
"""

import asyncio
from typing import Dict, Any, Set
from datetime import datetime


class AlertManager:
    """
    Verwaltet Statuswechsel und sendet nur bei Änderungen Benachrichtigungen
    """
    
    def __init__(self, discord_notifier, telegram_notifier, history_manager):
        """
        Args:
            discord_notifier: DiscordNotifier Instanz
            telegram_notifier: TelegramNotifier Instanz
            history_manager: HistoryManager Instanz
        """
        self.discord = discord_notifier
        self.telegram = telegram_notifier
        self.history = history_manager
        
        # Status-Tracking: {target_name: {'status': str, 'docker_state': str, 'outage_id': int}}
        self.last_states: Dict[str, Dict[str, Any]] = {}
        
        # Aktive Ausfälle: {target_name: outage_id}
        self.active_outages: Dict[str, int] = {}
    
    async def process_check_result(self, target: Dict[str, Any], 
                                   check_result: Dict[str, Any],
                                   docker_status: Dict[str, Any] = None):
        """
        Check-Ergebnis verarbeiten und ggf. Alert senden
        
        Args:
            target: Target-Konfiguration
            check_result: Ergebnis des Checks
            docker_status: Optional Docker Container Status
        """
        target_name = target['name']
        target_type = target['type']
        
        current_status = check_result.get('status', 'UNKNOWN')
        current_docker_state = docker_status.get('state', None) if docker_status else None
        
        # Letzter bekannter Status
        last_state = self.last_states.get(target_name, {})
        last_status = last_state.get('status', None)
        last_docker_state = last_state.get('docker_state', None)
        
        # Status-Historie speichern
        self.history.record_status(
            target_name=target_name,
            status=current_status,
            latency_ms=check_result.get('latency_ms') or check_result.get('response_time_ms'),
            players_online=check_result.get('players_online'),
            players_max=check_result.get('players_max'),
            docker_state=current_docker_state
        )
        
        # Statuswechsel erkennen
        status_changed = (last_status != current_status)
        docker_changed = (last_docker_state != current_docker_state)
        
        # OFFLINE oder ERROR → Alert senden
        if current_status in ['OFFLINE', 'ERROR'] and status_changed:
            await self._handle_outage(target, check_result, docker_status)
        
        # RECOVERY → Wiederherstellung
        elif current_status == 'ONLINE' and last_status in ['OFFLINE', 'ERROR']:
            await self._handle_recovery(target, check_result, docker_status)
        
        # Docker-Zustandsänderung bei laufendem Service
        elif docker_changed and current_docker_state and last_docker_state:
            # z.B. Container restart
            if current_docker_state != 'running' and last_docker_state == 'running':
                await self._handle_docker_issue(target, check_result, docker_status)
        
        # Aktuellen Status speichern
        self.last_states[target_name] = {
            'status': current_status,
            'docker_state': current_docker_state,
            'timestamp': datetime.now()
        }
    
    async def _handle_outage(self, target: Dict[str, Any], 
                            check_result: Dict[str, Any],
                            docker_status: Dict[str, Any] = None):
        """
        Ausfall behandeln
        """
        target_name = target['name']
        target_type = target['type']
        
        # Severity bestimmen
        severity = self._determine_severity(target, check_result, docker_status)
        
        # In Historie aufnehmen
        outage_id = self.history.record_outage_start(
            target_name=target_name,
            target_type=target_type,
            severity=severity,
            error_message=check_result.get('error'),
            docker_state=docker_status.get('state') if docker_status else None
        )
        
        self.active_outages[target_name] = outage_id
        
        # Benachrichtigungen senden
        if target_type == 'minecraft':
            # Spezialisierte Minecraft-Benachrichtigung
            await self.discord.send_minecraft_alert(
                severity=severity,
                target=check_result,
                docker_status=docker_status
            )
            
            await self.telegram.send_minecraft_alert(
                severity=severity,
                target=check_result,
                docker_status=docker_status
            )
        else:
            # Generische Benachrichtigung
            details = {
                'Status': check_result.get('status'),
                'Fehler': check_result.get('error', 'Unknown'),
                'Host': target.get('host'),
                'Port': target.get('port', '–')
            }
            
            await self.discord.send_alert(
                severity=severity,
                target_name=target_name,
                message=f"{target_type.upper()} nicht erreichbar",
                details=details
            )
            
            await self.telegram.send_alert(
                severity=severity,
                target_name=target_name,
                message=f"{target_type.upper()} nicht erreichbar",
                details=details
            )
        
        print(f"[{severity}] {target_name} ausgefallen - Outage ID: {outage_id}")
    
    async def _handle_recovery(self, target: Dict[str, Any],
                              check_result: Dict[str, Any],
                              docker_status: Dict[str, Any] = None):
        """
        Wiederherstellung behandeln
        """
        target_name = target['name']
        target_type = target['type']
        
        # Ausfall beenden
        outage_id = self.active_outages.pop(target_name, None)
        
        if outage_id:
            self.history.record_outage_end(outage_id)
            
            # Ausfallzeit ermitteln
            recent_outages = self.history.get_recent_outages(target_name, limit=1)
            outage_duration = recent_outages[0]['duration_seconds'] if recent_outages else None
        else:
            outage_duration = None
        
        # Recovery-Benachrichtigung
        if target_type == 'minecraft':
            await self.discord.send_minecraft_alert(
                severity='RECOVERY',
                target=check_result,
                docker_status=docker_status,
                outage_duration=outage_duration
            )
            
            await self.telegram.send_minecraft_alert(
                severity='RECOVERY',
                target=check_result,
                docker_status=docker_status,
                outage_duration=outage_duration
            )
        else:
            duration_str = self._format_duration(outage_duration) if outage_duration else 'unbekannt'
            
            details = {
                'Status': 'ONLINE',
                'Ausfallzeit': duration_str,
                'Host': target.get('host')
            }
            
            await self.discord.send_alert(
                severity='RECOVERY',
                target_name=target_name,
                message=f"{target_type.upper()} wieder erreichbar",
                details=details
            )
            
            await self.telegram.send_alert(
                severity='RECOVERY',
                target_name=target_name,
                message=f"{target_type.upper()} wieder erreichbar",
                details=details
            )
        
        print(f"[RECOVERY] {target_name} wieder online - Ausfallzeit: {outage_duration}s")
    
    async def _handle_docker_issue(self, target: Dict[str, Any],
                                   check_result: Dict[str, Any],
                                   docker_status: Dict[str, Any]):
        """
        Docker-spezifische Probleme (z.B. Container-Restart)
        """
        target_name = target['name']
        
        # Nur WARNING senden, kein CRITICAL
        await self.discord.send_alert(
            severity='WARNING',
            target_name=target_name,
            message="Docker Container Status geändert",
            details={
                'Container': docker_status.get('state'),
                'Service': check_result.get('status'),
                'Restarts': docker_status.get('restart_count', 0)
            }
        )
    
    def _determine_severity(self, target: Dict[str, Any],
                           check_result: Dict[str, Any],
                           docker_status: Dict[str, Any] = None) -> str:
        """
        Severity Level bestimmen
        
        Returns:
            'CRITICAL' oder 'WARNING'
        """
        # Ping-Check auf vServer → immer CRITICAL
        if target['type'] == 'ping':
            return 'CRITICAL'
        
        # MySQL down → CRITICAL
        if target['name'] == 'MySQL':
            return 'CRITICAL'
        
        # Minecraft mit Docker-Info
        if target['type'] == 'minecraft' and docker_status:
            docker_state = docker_status.get('state')
            
            # Container läuft noch, aber Port antwortet nicht → WARNING (startet evtl. noch)
            if docker_state == 'running' and check_result.get('status') == 'OFFLINE':
                return 'WARNING'
            
            # Container exited oder fehlt → CRITICAL
            if docker_state in ['exited', 'dead'] or not docker_status.get('exists'):
                return 'CRITICAL'
        
        # Standard: CRITICAL bei kompletten Ausfall
        if check_result.get('status') in ['OFFLINE', 'ERROR']:
            return 'CRITICAL'
        
        return 'WARNING'
    
    async def check_vserver_status(self, vserver_ping_result: Dict[str, Any],
                                   all_targets: list):
        """
        Spezielle Prüfung: Wenn vServer komplett down ist
        """
        if vserver_ping_result.get('status') == 'OFFLINE':
            # Alle betroffenen Services sammeln
            affected = [t['name'] for t in all_targets if t['type'] != 'ping']
            
            await self.discord.send_vserver_critical(
                vserver_ip=vserver_ping_result.get('name'),
                affected_services=affected
            )
            
            await self.telegram.send_vserver_critical(
                vserver_ip=vserver_ping_result.get('name'),
                affected_services=affected
            )
    
    def _format_duration(self, seconds: int) -> str:
        """Dauer formatieren"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Aktuellen Status-Überblick zurückgeben
        
        Returns:
            Summary mit allen Stati
        """
        total = len(self.last_states)
        online = sum(1 for s in self.last_states.values() if s.get('status') == 'ONLINE')
        offline = len(self.active_outages)
        
        return {
            'total_targets': total,
            'online': online,
            'offline': offline,
            'active_outages': list(self.active_outages.keys()),
            'overall_status': 'CRITICAL' if offline > 0 else 'ONLINE'
        }
