from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
from datetime import datetime, timedelta
import json
import asyncio
from app.redis import get_redis_client

router = APIRouter()
redis_client = get_redis_client()

# Store connected chat clients
chat_clients: Dict[str, Set[WebSocket]] = {}

async def cleanup_old_messages():
    """Delete messages older than 30 minutes"""
    while True:
        try:
            # Get all chat keys
            all_chat_keys = redis_client.keys("chat:*")
            
            # Current time minus 30 minutes
            cutoff_time = datetime.now() - timedelta(minutes=30)
            
            for key in all_chat_keys:
                try:
                    # Get message data
                    message_data = json.loads(redis_client.get(key))
                    message_time = datetime.fromisoformat(message_data["timestamp"])
                    
                    # Delete if older than 30 minutes
                    if message_time < cutoff_time:
                        redis_client.delete(key)
                except (json.JSONDecodeError, KeyError, ValueError):
                    # If there's any error parsing the message, delete it
                    redis_client.delete(key)
                    
        except Exception as e:
            print(f"Error in cleanup task: {e}")
            
        # Run every minute
        await asyncio.sleep(60)

@router.websocket("/ws/chat/{room_id}")
async def chat_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    # Initialize room if it doesn't exist
    if room_id not in chat_clients:
        chat_clients[room_id] = set()
    chat_clients[room_id].add(websocket)
    
    # Start cleanup task if it's not already running
    if not any(task.get_name() == "cleanup_task" for task in asyncio.all_tasks()):
        cleanup_task = asyncio.create_task(cleanup_old_messages())
        cleanup_task.set_name("cleanup_task")
    
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
            
            # Get recent messages (not older than 30 minutes)
            message_keys = redis_client.keys(f"chat:{room_id}:*")
            recent_messages = []
            cutoff_time = datetime.now() - timedelta(minutes=30)
            
            for key in sorted(message_keys)[-50:]:  # Keep last 50 messages
                msg = redis_client.get(key)
                if msg:
                    try:
                        msg_data = json.loads(msg)
                        msg_time = datetime.fromisoformat(msg_data["timestamp"])
                        if msg_time >= cutoff_time:
                            recent_messages.append(msg_data)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
            
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