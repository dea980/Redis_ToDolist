from fastapi import FastAPI
from app.routers import todos
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 (프론트엔드와 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요에 따라 도메인 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(todos.router)

# 정적 파일 제공 (React 빌드 파일)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI + Redis"}
