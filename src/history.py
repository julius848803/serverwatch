"""
SQLite Ausfallhistorie
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import sqlite3
import logging
from typing import List, Dict, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class HistoryDB:
    """SQLite Datenbank für Ausfallhistorie"""
    
    def __init__(self, db_path: str = "serverwatch.db"):
        """
        Args:
            db_path: Pfad zur SQLite Datei
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._init_db()
    
    def _init_db(self):
        """Erstellt Datenbank und Tabellen"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            cursor = self.conn.cursor()
            
            # Incidents Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    previous_status TEXT,
                    severity TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    resolved_at TEXT,
                    duration_seconds INTEGER,
                    details TEXT,
                    error_message TEXT
                )
            """)
            
            # Status History Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS status_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    latency_ms REAL,
                    players_online INTEGER,
                    details TEXT
                )
            """)
            
            # Indizes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_incidents_target 
                ON incidents(target_name)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_incidents_started 
                ON incidents(started_at)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_history_target 
                ON status_history(target_name)
            """)
            
            self.conn.commit()
            logger.info(f"Datenbank initialisiert: {self.db_path}")
            
        except Exception as e:
            logger.error(f"DB Init Fehler: {e}")
            raise
    
    def log_incident(self, alert: Dict):
        """Speichert Incident in DB"""
        if not self.conn:
            return
        
        try:
            cursor = self.conn.cursor()
            
            details_str = str(alert.get("details", {}))
            error = alert.get("details", {}).get("error")
            
            cursor.execute("""
                INSERT INTO incidents 
                (target_name, status, previous_status, severity, started_at, details, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                alert["target"],
                alert["status"],
                alert.get("previous_status"),
                alert["severity"],
                alert["timestamp"],
                details_str,
                error
            ))
            
            self.conn.commit()
            logger.debug(f"Incident gespeichert: {alert['target']}")
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern des Incidents: {e}")
    
    def log_status(self, target_name: str, status: str, details: Dict):
        """Speichert Status-Check in History"""
        if not self.conn:
            return
        
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                INSERT INTO status_history 
                (target_name, status, timestamp, latency_ms, players_online, details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                target_name,
                status,
                datetime.now().isoformat(),
                details.get("latency_ms") or details.get("response_time_ms"),
                details.get("players_online"),
                str(details)
            ))
            
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Status-History: {e}")
    
    def get_recent_incidents(self, target_name: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Lädt letzte Incidents"""
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor()
            
            if target_name:
                cursor.execute("""
                    SELECT * FROM incidents 
                    WHERE target_name = ?
                    ORDER BY started_at DESC 
                    LIMIT ?
                """, (target_name, limit))
            else:
                cursor.execute("""
                    SELECT * FROM incidents 
                    ORDER BY started_at DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Fehler beim Laden der Incidents: {e}")
            return []
    
    def get_status_history(self, target_name: str, limit: int = 100) -> List[Dict]:
        """Lädt Status-Historie für ein Target"""
        if not self.conn:
            return []
        
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT * FROM status_history 
                WHERE target_name = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (target_name, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Fehler beim Laden der History: {e}")
            return []
    
    def close(self):
        """Schließt DB Verbindung"""
        if self.conn:
            self.conn.close()
            logger.info("Datenbank geschlossen")
