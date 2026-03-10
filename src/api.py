"""
FastAPI Dashboard + WebSocket
Author: xXLuckyGamer04Xx
Version: 1.2.0
"""

import asyncio
import logging
from typing import Dict, List, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class DashboardAPI:
    """FastAPI Dashboard Server"""
    
    def __init__(self, monitor, port: int = 8000):
        """
        Args:
            monitor: ServerMonitor Instance
            port: HTTP Port
        """
        self.monitor = monitor
        self.port = port
        self.app = FastAPI(title="ServerWatch Dashboard")
        
        # WebSocket Clients
        self.active_connections: Set[WebSocket] = set()
        
        # Routes registrieren
        self._setup_routes()
    
    def _setup_routes(self):
        """Registriert API Endpoints"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def get_index():
            """Dashboard HTML"""
            html_path = Path(__file__).parent.parent / "dashboard" / "index.html"
            if html_path.exists():
                return FileResponse(html_path)
            return HTMLResponse("<h1>Dashboard nicht gefunden</h1>")
        
        @self.app.get("/api/status")
        async def get_status():
            """Aktueller Status aller Targets"""
            return {
                "targets": list(self.monitor.current_status.values()),
                "overall": self.monitor.alert_manager.get_overall_status(
                    list(self.monitor.current_status.values())
                )
            }
        
        @self.app.get("/api/history/{target_name}")
        async def get_history(target_name: str):
            """Historie für ein Target"""
            if not self.monitor.history:
                return {"error": "History nicht verfügbar"}
            
            incidents = self.monitor.history.get_recent_incidents(target_name, limit=20)
            history = self.monitor.history.get_status_history(target_name, limit=100)
            
            return {
                "incidents": incidents,
                "history": history
            }
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket für Live-Updates"""
            await self.connect_websocket(websocket)
            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                self.disconnect_websocket(websocket)
    
    async def connect_websocket(self, websocket: WebSocket):
        """Neuer WebSocket Client"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket Client verbunden ({len(self.active_connections)} aktiv)")
        await self.broadcast_status()
    
    def disconnect_websocket(self, websocket: WebSocket):
        """WebSocket Client getrennt"""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket Client getrennt ({len(self.active_connections)} aktiv)")
    
    async def broadcast_status(self):
        """Sendet Status an alle Clients"""
        if not self.active_connections:
            return
        
        status_data = {
            "type": "status_update",
            "targets": list(self.monitor.current_status.values()),
            "overall": self.monitor.alert_manager.get_overall_status(
                list(self.monitor.current_status.values())
            )
        }
        
        message = json.dumps(status_data)
        
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"WebSocket Send Error: {e}")
                disconnected.add(connection)
        
        self.active_connections -= disconnected
    
    async def run(self):
        """Startet FastAPI Server"""
        import uvicorn
        
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        logger.info(f"Dashboard gestartet auf http://0.0.0.0:{self.port}")
        await server.serve()
