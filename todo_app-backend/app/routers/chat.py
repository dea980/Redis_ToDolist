from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
from datetime import datetime
import json
from app.redis import get_redis_client

router = APIRouter()
redis_client = get_redis_client()

# Store connected chat clients
chat_clients: Dict[str, Set[WebSocket]] = {}

@router.websocket("/ws/chat/{room_id}")
async def chat_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    # Initialize room if it doesn't exist
    if room_id not in chat_clients:
        chat_clients[room_id] = set()
    chat_clients[room_id].add(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Add timestamp to message
            message_data["timestamp"] = datetime.now().isoformat()
            
            # Store message in Redis
            message_key = f"chat:{room_id}:{message_data['timestamp']}"
            redis_client.set(message_key, json.dumps(message_data))
            
            # Get recent messages
            message_keys = redis_client.keys(f"chat:{room_id}:*")
            recent_messages = []
            for key in sorted(message_keys)[-50:]:  # Keep last 50 messages
                msg = redis_client.get(key)
                if msg:
                    recent_messages.append(json.loads(msg))
            
            # Broadcast to all clients in the room
            disconnected = set()
            for client in chat_clients[room_id]:
                try:
                    await client.send_json({
                        "type": "messages",
                        "messages": recent_messages
                    })
                except Exception:
                    disconnected.add(client)
            
            # Remove disconnected clients
            for client in disconnected:
                chat_clients[room_id].remove(client)
                
    except WebSocketDisconnect:
        chat_clients[room_id].remove(websocket)
        if not chat_clients[room_id]:
            del chat_clients[room_id]