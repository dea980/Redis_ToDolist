# 할 일 목록 라우터 (todos.py) 설명서

## 개요
이 파일은 할 일 목록의 CRUD(생성, 읽기, 수정, 삭제) 작업과 디버깅 정보를 처리하는 API 엔드포인트를 제공합니다. Redis를 데이터베이스로 사용하여 할 일 항목을 저장하고 관리합니다.

## 코드 구조 및 작동 원리

### 1. 기본 설정
```python
from fastapi import APIRouter, HTTPException
from app.redis import get_redis_client
from urllib.parse import unquote

router = APIRouter()
redis_client = get_redis_client()
```

#### 주요 구성 요소
- **APIRouter**: FastAPI의 라우팅 시스템
- **Redis 클라이언트**: 데이터 저장소 연결
- **URL 디코딩**: 한글 등 특수문자 처리

### 2. 할 일 목록 조회 기능

#### 엔드포인트 구현
```python
@router.get("/todos")
def list_todos():
    """
    Redis에서 모든 할 일 항목을 조회합니다.
    """
    try:
        keys = redis_client.keys("todo:*")
        todos = {key: redis_client.get(key) for key in keys}
        return {"todos": todos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todos: {str(e)}")
```

#### 작동 원리
1. **데이터 조회**
   - "todo:" 프리픽스로 시작하는 모든 키 검색
   - 각 키에 해당하는 값 조회
   - 딕셔너리 형태로 변환

2. **에러 처리**
   - 예외 상황 감지
   - HTTP 500 에러 반환
   - 상세 에러 메시지 제공

### 3. 할 일 추가 기능

#### 엔드포인트 구현
```python
@router.post("/todos/{todo_id}")
def create_todo(todo_id: str, task: str):
    """
    새로운 할 일을 추가합니다.
    """
    redis_key = f"todo:{todo_id}"
    try:
        if redis_client.exists(redis_key):
            raise HTTPException(status_code=400, detail="Todo already exists")
        redis_client.set(redis_key, task)
        return {"message": "Todo created successfully", "todo_id": todo_id, "task": task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating todo: {str(e)}")
```

#### 작동 원리
1. **데이터 검증**
   - 중복 키 확인
   - 입력 데이터 유효성 검사
   - 에러 상황 처리

2. **저장 프로세스**
   - Redis 키 생성
   - 데이터 저장
   - 결과 반환

### 4. 할 일 수정 기능

#### 엔드포인트 구현
```python
@router.put("/todos/{todo_id}")
async def update_todo(todo_id: str, task: str):
    """
    기존 할 일을 수정합니다.
    """
    redis_key = todo_id if todo_id.startswith("todo:") else f"todo:{todo_id}"
    try:
        if not redis_client.exists(redis_key):
            raise HTTPException(status_code=404, detail="Todo not found")
        redis_client.set(redis_key, task)
        print(f"Updated Todo: {redis_key} -> {task}")
        return {"message": "Todo updated successfully", "todo_id": todo_id, "task": task}
    except Exception as e:
        print(f"Error updating todo: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating todo: {str(e)}")
```

#### 작동 원리
1. **키 처리**
   - 프리픽스 확인 및 추가
   - 존재 여부 확인
   - 유효성 검사

2. **업데이트 프로세스**
   - 데이터 갱신
   - 로그 기록
   - 결과 반환

### 5. 할 일 삭제 기능

#### 엔드포인트 구현
```python
@router.delete("/todos/{key}")
def delete_todo(key: str):
    """
    할 일을 삭제합니다.
    """
    decoded_key = unquote(key)
    try:
        if redis_client.exists(decoded_key):
            redis_client.delete(decoded_key)
            return {"message": f"Todo '{decoded_key}' deleted successfully."}
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting todo: {str(e)}")
```

#### 작동 원리
1. **키 처리**
   - URL 디코딩
   - 존재 확인
   - 에러 처리

2. **삭제 프로세스**
   - Redis에서 데이터 제거
   - 결과 확인
   - 응답 반환

### 6. 디버깅 기능

#### 엔드포인트 구현
```python
@router.get("/debug/redis")
async def debug_redis():
    """
    Redis의 모든 할 일 데이터를 조회합니다.
    """
    try:
        keys = redis_client.keys("todo:*")
        data = {key: redis_client.get(key) for key in keys}
        return {"debug_data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching debug data: {str(e)}")
```

#### 작동 원리
1. **데이터 조회**
   - 전체 데이터 검색
   - 포맷팅
   - 디버그 정보 제공

## 데이터 구조

### 1. Redis 키 형식
- 프리픽스: "todo:"
- 형태: `todo:{고유ID}`
- 값: 할 일 내용 문자열

### 2. 응답 형식

#### 목록 조회
```json
{
    "todos": {
        "todo:123": "할 일 내용",
        "todo:456": "다른 할 일"
    }
}
```

#### 생성/수정
```json
{
    "message": "Todo created/updated successfully",
    "todo_id": "123",
    "task": "할 일 내용"
}
```

## 성능 최적화

### 1. Redis 작업
- 효율적인 키-값 저장
- 빠른 데이터 접근
- 메모리 최적화

### 2. 에러 처리
- 예외 상황 포착
- 적절한 에러 코드
- 상세한 에러 메시지

### 3. 데이터 검증
- 입력 데이터 확인
- 중복 검사
- 유효성 검증

## 보안 고려사항

### 1. 데이터 보안
- 입력 데이터 검증
- URL 디코딩 처리
- 에러 메시지 보안

### 2. 접근 제어
- 엔드포인트 보호
- 데이터 무결성
- 권한 확인

## 확장성

### 1. 코드 구조
- 모듈화된 설계
- 명확한 책임 분리
- 유지보수 용이성

### 2. 기능 확장
- 새로운 엔드포인트 추가 용이
- 기존 기능 수정 편의
- 테스트 용이성