from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.routers import todos, chat
from app.redis import get_redis_client
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis 연결 초기화
redis_client = get_redis_client()

# WebSocket 클라이언트 관리
connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # Redis에서 "todo:*" 키 가져오기
            keys = redis_client.keys("todo:*")
            data = {key: redis_client.get(key) for key in keys}
            message = json.dumps(data)

            # 모든 클라이언트에 메시지 전송
            disconnected_clients = []
            for client in connected_clients:
                try:
                    await client.send_text(message)
                except Exception as e:
                    print(f"Error sending to client: {e}")
                    disconnected_clients.append(client)

            # 비정상 연결 제거
            for client in disconnected_clients:
                connected_clients.remove(client)

            await asyncio.sleep(1)  # 데이터 전송 간격
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Client disconnected")

# 라우터 추가
app.include_router(todos.router)
app.include_router(chat.router)
