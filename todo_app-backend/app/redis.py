import redis
from fastapi import HTTPException

# Redis 클라이언트 설정
redis_client = redis.StrictRedis(
    host="redis",  # Docker Compose에서 Redis 컨테이너 이름
    port=6379,
    decode_responses=True
)

# Redis 연결 확인 함수
def get_redis_client():
    try:
        redis_client.ping()  # 연결 테스트
        return redis_client
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Cannot connect to Redis server")
