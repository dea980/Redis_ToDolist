from fastapi import APIRouter, HTTPException
from app.redis import get_redis_client

router = APIRouter()
redis_client = get_redis_client()

@router.get("/todos")
def list_todos():
    """모든 작업 조회"""
    keys = redis_client.keys("todo:*")
    todos = {key: redis_client.get(key) for key in keys}
    return todos

@router.post("/todos/{todo_id}")
def create_todo(todo_id: str, task: str):
    """새 작업 추가"""
    if redis_client.exists(f"todo:{todo_id}"):
        raise HTTPException(status_code=400, detail="Todo already exists")
    redis_client.set(f"todo:{todo_id}", task)
    return {"todo_id": todo_id, "task": task}

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    """작업 삭제"""
    if not redis_client.exists(f"todo:{todo_id}"):
        raise HTTPException(status_code=404, detail="Todo not found")
    redis_client.delete(f"todo:{todo_id}")
    return {"message": "Todo deleted"}
