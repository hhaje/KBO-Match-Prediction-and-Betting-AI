"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import matches, predictions, betting, performance

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="KBO 경기 예측 AI 베팅 시스템 API",
    description="KBO 경기 예측 및 베팅 시뮬레이션 API",
    version="0.1.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(matches.router, prefix="/api/matches", tags=["경기"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["예측"])
app.include_router(betting.router, prefix="/api/betting", tags=["베팅"])
app.include_router(performance.router, prefix="/api/performance", tags=["성능"])


@app.get("/")
async def root():
    """
    API 루트
    """
    return {
        "message": "KBO 경기 예측 AI 베팅 시스템 API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """
    헬스 체크
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


