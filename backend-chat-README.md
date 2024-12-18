# 채팅 라우터 (chat.py) 설명서

## 개요
이 파일은 WebSocket을 사용한 실시간 채팅 기능을 구현하며, Redis를 사용하여 메시지를 저장하고 관리합니다. 채팅방 기반의 실시간 메시지 교환 시스템을 제공합니다.

## 코드 구조 및 작동 원리

### 1. 기본 설정
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
from datetime import datetime
import json
from app.redis import get_redis_client

router = APIRouter()
redis_client = get_redis_client()
chat_clients: Dict[str, Set[WebSocket]] = {}
```

#### 주요 구성 요소
- **WebSocket**: 실시간 양방향 통신
- **Redis**: 메시지 저장소
- **채팅방 관리**: Dictionary와 Set 자료구조 활용

### 2. WebSocket 연결 관리

#### 엔드포인트 구현
```python
@router.websocket("/ws/chat/{room_id}")
async def chat_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in chat_clients:
        chat_clients[room_id] = set()
    chat_clients[room_id].add(websocket)
```

#### 작동 원리
1. **연결 수립**
   - WebSocket 연결 수락
   - 채팅방 초기화
   - 클라이언트 등록

2. **채팅방 관리**
   - 룸별 클라이언트 그룹화
   - Set 자료구조로 중복 방지
   - 효율적인 클라이언트 관리

### 3. 메시지 처리 시스템

#### 구현 코드
```python
try:
    while True:
        # 메시지 수신
        data = await websocket.receive_text()
        message_data = json.loads(data)
        
        # 타임스탬프 추가
        message_data["timestamp"] = datetime.now().isoformat()
        
        # Redis에 저장
        message_key = f"chat:{room_id}:{message_data['timestamp']}"
        redis_client.set(message_key, json.dumps(message_data))
```

#### 작동 원리
1. **메시지 수신**
   - JSON 형식 파싱
   - 타임스탬프 추가
   - 데이터 구조화

2. **메시지 저장**
   - Redis 키 생성
   - JSON 직렬화
   - 영구 저장

### 4. 메시지 브로드캐스팅

#### 구현 방식
```python
# 최근 메시지 조회
message_keys = redis_client.keys(f"chat:{room_id}:*")
recent_messages = []
for key in sorted(message_keys)[-50:]:
    msg = redis_client.get(key)
    if msg:
        recent_messages.append(json.loads(msg))

# 브로드캐스팅
disconnected = set()
for client in chat_clients[room_id]:
    try:
        await client.send_json({
            "type": "messages",
            "messages": recent_messages
        })
    except Exception:
        disconnected.add(client)
```

#### 작동 원리
1. **메시지 히스토리**
   - 최근 50개 메시지 유지
   - 시간순 정렬
   - JSON 역직렬화

2. **메시지 전송**
   - 룸 내 전체 전송
   - 연결 상태 확인
   - 실패 처리

### 5. 연결 관리 시스템

#### 구현 코드
```python
# 연결 해제된 클라이언트 제거
for client in disconnected:
    chat_clients[room_id].remove(client)

except WebSocketDisconnect:
    chat_clients[room_id].remove(websocket)
    if not chat_clients[room_id]:
        del chat_clients[room_id]
```

#### 작동 원리
1. **연결 해제 처리**
   - 클라이언트 제거
   - 빈 방 정리
   - 리소스 정리

2. **에러 처리**
   - 연결 끊김 감지
   - 안전한 제거
   - 상태 관리

## 데이터 구조

### 1. 메시지 형식
```json
{
    "username": "사용자명",
    "content": "메시지 내용",
    "room_id": "방 ID",
    "timestamp": "2023-01-01T12:00:00.000Z"
}
```

### 2. Redis 키 구조
- 패턴: `chat:{room_id}:{timestamp}`
- 예시: `chat:room1:2023-01-01T12:00:00.000Z`

### 3. 클라이언트 관리
```python
chat_clients = {
    "room1": {websocket1, websocket2},
    "room2": {websocket3}
}
```

## 성능 최적화

### 1. 메모리 관리
- Set 자료구조 활용
- 최근 메시지 제한
- 효율적인 클라이언트 추적

### 2. 메시지 처리
- 비동기 처리
- 일괄 전송
- 효율적인 저장

### 3. 연결 관리
- 빠른 클라이언트 검색
- 자동 정리
- 리소스 최적화

## 에러 처리

### 1. 연결 에러
- WebSocket 예외 처리
- 자동 재연결
- 상태 복구

### 2. 메시지 에러
- JSON 파싱 에러
- 전송 실패
- 저장 실패

## 보안 고려사항

### 1. 메시지 보안
- 입력 검증
- XSS 방지
- 데이터 무결성

### 2. 연결 보안
- 인증 처리
- 권한 확인
- 접근 제어

## 확장성

### 1. 기능 확장
- 새로운 메시지 타입
- 추가 메타데이터
- 사용자 상태 관리

### 2. 성능 확장
- 채팅방 수 확장
- 메시지 처리량 증가
- 동시 접속자 처리

## 모니터링 및 디버깅

### 1. 로깅
- 연결 상태
- 메시지 흐름
- 에러 추적

### 2. 성능 모니터링
- 메시지 처리 시간
- 메모리 사용량
- 연결 상태