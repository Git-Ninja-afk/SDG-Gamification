"""WebSocket manager for real-time features"""
from fastapi import WebSocket
from typing import Dict, Set
import json
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.user_locations: Dict[int, str] = {}  # user_id -> location

    async def connect(self, user_id: int, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        """Remove disconnected user"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_locations:
            del self.user_locations[user_id]

    async def broadcast_leaderboard_update(self, leaderboard_data: dict):
        """Broadcast leaderboard updates to all connected users"""
        message = {
            "type": "leaderboard_update",
            "data": leaderboard_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self._broadcast(message)

    async def send_real_time_notification(self, user_id: int, notification: dict):
        """Send notification to specific user"""
        if user_id in self.active_connections:
            message = {
                "type": "notification",
                "data": notification,
                "timestamp": datetime.utcnow().isoformat()
            }
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception as e:
                print(f"Error sending notification: {e}")
                self.disconnect(user_id)

    async def broadcast_achievement_unlocked(self, user_id: int, achievement: dict):
        """Broadcast achievement to relevant users"""
        message = {
            "type": "achievement_unlocked",
            "user_id": user_id,
            "achievement": achievement,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self._broadcast(message)

    async def broadcast_game_update(self, game_id: int, game_data: dict):
        """Broadcast multiplayer game updates"""
        message = {
            "type": "game_update",
            "game_id": game_id,
            "data": game_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self._broadcast(message)

    async def send_game_notification(self, user_ids: list, notification: dict):
        """Send notification to game participants"""
        message = {
            "type": "game_notification",
            "data": notification,
            "timestamp": datetime.utcnow().isoformat()
        }
        for user_id in user_ids:
            if user_id in self.active_connections:
                try:
                    await self.active_connections[user_id].send_json(message)
                except Exception as e:
                    print(f"Error sending game notification: {e}")
                    self.disconnect(user_id)

    async def broadcast_location_update(self, user_id: int, location: str):
        """Broadcast user location for nearby tasks"""
        self.user_locations[user_id] = location
        
        message = {
            "type": "location_update",
            "user_id": user_id,
            "location": location,
            "timestamp": datetime.utcnow().isoformat()
        }
        # Broadcast to nearby users only
        await self._broadcast(message, exclude={user_id})

    async def _broadcast(self, message: dict, exclude: Set[int] = None):
        """Internal broadcast method"""
        if exclude is None:
            exclude = set()
        
        disconnected_users = []
        for user_id, connection in self.active_connections.items():
            if user_id not in exclude:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error broadcasting to user {user_id}: {e}")
                    disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            self.disconnect(user_id)

    def get_online_users(self) -> list:
        """Get list of online users"""
        return list(self.active_connections.keys())

    def get_online_count(self) -> int:
        """Get count of online users"""
        return len(self.active_connections)

# Global connection manager instance
manager = ConnectionManager()
