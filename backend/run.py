"""
백엔드 서버 실행 스크립트
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 개발 모드에서 코드 변경 시 자동 재시작
        log_level="info"
    )


