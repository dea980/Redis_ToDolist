from fastapi import APIRouter, HTTPException
from app.redis import get_redis_client
from urllib.parse import unquote
import json

router = APIRouter()

# Redis 클라이언트 초기화
redis_client = get_redis_client()

@router.get("/todos")
def list_todos():
    """
    Redis에서 "todo:*" 패턴에 해당하는 모든 작업을 반환합니다.
    """
    try:
        keys = redis_client.keys("todo:*")
        todos = {key: json.loads(redis_client.get(key)) for key in keys}  # JSON 문자열을 파싱
        return {"todos": todos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todos: {str(e)}")


@router.post("/todos/{todo_id}")
def create_todo(todo_id: str, task: str, date: str, goal: str):
    """
    새로운 작업을 Redis에 추가합니다.
    """
    redis_key = f"todo:{todo_id}"
    try:
        if redis_client.exists(redis_key):
            raise HTTPException(status_code=400, detail="Todo already exists")
        
        todo_data = {
            "task": task,
            "date": date,
            "goal": goal
        }
        redis_client.set(redis_key, json.dumps(todo_data))
        return {"message": "Todo created successfully", "todo_id": todo_id, "data": todo_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating todo: {str(e)}")

@router.put("/todos/{todo_id}")
async def update_todo(todo_id: str, task: str, date: str, goal: str):
    """
    특정 작업을 업데이트합니다.
    """
    redis_key = todo_id if todo_id.startswith("todo:") else f"todo:{todo_id}"
    try:
        if not redis_client.exists(redis_key):
            raise HTTPException(status_code=404, detail="Todo not found")

        todo_data = {
            "task": task,
            "date": date,
            "goal": goal
        }
        redis_client.set(redis_key, json.dumps(todo_data))
        return {"message": "Todo updated successfully", "todo_id": todo_id, "data": todo_data}
    except Exception as e:
        print(f"Error updating todo: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating todo: {str(e)}")


@router.delete("/todos/{key}")
def delete_todo(key: str):
    """
    Redis에서 특정 작업을 삭제합니다.
    """
    decoded_key = unquote(key)  # URL 디코딩
    try:
        if redis_client.exists(decoded_key):
            redis_client.delete(decoded_key)
            return {"message": f"Todo '{decoded_key}' deleted successfully."}
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting todo: {str(e)}")


@router.get("/debug/redis")
async def debug_redis():
    """
    Redis의 모든 작업 디버깅 데이터를 반환합니다.
    """
    try:
        keys = redis_client.keys("todo:*")
        data = {key: redis_client.get(key) for key in keys}
        return {"debug_data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching debug data: {str(e)}")
