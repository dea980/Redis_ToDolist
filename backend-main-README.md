# 백엔드 메인 애플리케이션 (main.py) 설명서

## 개요
이 파일은 FastAPI 백엔드 애플리케이션의 진입점으로, 서버 설정, WebSocket 연결, 라우터 통합을 담당합니다.

## 코드 구조 및 작동 원리

### 1. 기본 설정
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.routers import todos, chat
from app.redis import get_redis_client
from fastapi.middleware.cors import CORSMiddleware
```

#### 주요 컴포넌트
- **FastAPI**: 고성능 웹 프레임워크
- **WebSocket**: 실시간 양방향 통신 지원
- **Redis**: 인메모리 데이터베이스 연결
- **CORS**: 교차 출처 리소스 공유 설정

### 2. CORS 설정 원리
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 작동 방식
1. **교차 출처 요청 처리**
   - 다른 도메인에서의 API 접근 허용
   - 보안 정책 설정
   - 리소스 접근 제어

2. **보안 고려사항**
   - 모든 출처 허용 ("*")
   - 인증 정보 처리 활성화
   - HTTP 메소드 및 헤더 제어

### 3. WebSocket 연결 관리

#### 연결 설정
```python
connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
```

#### 작동 원리
1. **연결 수립**
   - 클라이언트 연결 요청 수락
   - 연결된 클라이언트 추적
   - 비동기 통신 설정

2. **데이터 동기화**
   ```python
   while True:
       keys = redis_client.keys("todo:*")
       data = {key: redis_client.get(key) for key in keys}
       message = json.dumps(data)
   ```
   - Redis 데이터 실시간 조회
   - JSON 형식으로 변환
   - 모든 클라이언트에 브로드캐스트

3. **에러 처리**
   ```python
   try:
       await client.send_text(message)
   except Exception as e:
       print(f"Error sending to client: {e}")
       disconnected_clients.append(client)
   ```
   - 전송 실패 감지
   - 연결 끊김 처리
   - 클라이언트 정리

### 4. Redis 연동 메커니즘

#### 초기화
```python
redis_client = get_redis_client()
```

#### 데이터 처리 흐름
1. **데이터 조회**
   - Redis 키 패턴 매칭
   - 데이터 일괄 조회
   - 실시간 동기화

2. **성능 최적화**
   - 인메모리 처리
   - 빠른 데이터 접근
   - 효율적인 캐싱

### 5. 비동기 처리 시스템

#### 구현 원리
```python
async def websocket_endpoint(websocket: WebSocket):
    while True:
        # 데이터 처리
        await asyncio.sleep(1)
```

1. **비동기 작동 방식**
   - 이벤트 루프 기반 처리
   - 논블로킹 작업 수행
   - 효율적인 리소스 사용

2. **성능 고려사항**
   - 동시성 처리
   - 메모리 효율성
   - 응답성 유지

### 6. 에러 처리 시스템

#### 주요 에러 처리
1. **연결 에러**
   ```python
   except WebSocketDisconnect:
       connected_clients.remove(websocket)
       print("Client disconnected")
   ```
   - 연결 종료 감지
   - 리소스 정리
   - 상태 로깅

2. **데이터 전송 에러**
   - 전송 실패 처리
   - 클라이언트 상태 관리
   - 자동 복구 메커니즘

### 7. 라우터 통합

#### 구조
```python
app.include_router(todos.router)
app.include_router(chat.router)
```

#### 작동 방식
1. **모듈화**
   - 기능별 라우터 분리
   - 코드 구조화
   - 유지보수성 향상

2. **라우팅 처리**
   - URL 패턴 매칭
   - 요청 처리 위임
   - 응답 반환

## 성능 최적화 전략

### 1. 메모리 관리
- Set 자료구조 사용으로 O(1) 검색
- 효율적인 클라이언트 추적
- 적절한 가비지 컬렉션

### 2. 통신 최적화
- 실시간 데이터 동기화
- 최소한의 데이터 전송
- 효율적인 브로드캐스팅

### 3. 확장성 고려
- 모듈식 구조
- 독립적인 컴포넌트
- 유연한 구성

## 디버깅 및 모니터링

### 1. 로깅 시스템
- 연결 상태 추적
- 에러 로깅
- 성능 모니터링

### 2. 에러 추적
- 상세한 에러 메시지
- 스택 트레이스 기록
- 문제 해결 용이성

## 보안 고려사항

### 1. 데이터 보안
- 입력 검증
- 데이터 무결성
- 접근 제어

### 2. 연결 보안
- WebSocket 보안
- CORS 정책
- 인증 처리