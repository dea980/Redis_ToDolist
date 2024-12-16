import redis# {"conversationId":"c2646750-7516-4ea2-85dc-fefb609e6e02","source":"instruct"}

# Redis 클라이언트 설정
redis_client = redis.StrictRedis(
    host="localhost",  # 로컬 개발 환경에서는 localhost
    port=6379,
    decode_responses=True
)

# Redis 연결 확인 함수
def get_redis_client():
    try:
        redis_client.ping()
        print("Connected to Redis server successfully!")
        return redis_client
    except redis.ConnectionError:
        print("Failed to connect to Redis server!")
        raise
