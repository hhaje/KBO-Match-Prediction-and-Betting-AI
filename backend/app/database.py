"""
데이터베이스 연결 및 세션 관리
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MySQL 연결 설정
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "kbo_betting_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# MySQL 연결 URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 연결 유효성 체크
    pool_recycle=3600,   # 1시간마다 연결 재생성
    echo=False,          # SQL 로그 출력 (개발 시 True로 설정 가능)
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()


def get_db() -> Generator:
    """
    데이터베이스 세션 의존성
    FastAPI 엔드포인트에서 사용
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    데이터베이스 초기화
    모든 테이블 생성
    """
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블이 생성되었습니다.")


def check_db_connection():
    """
    데이터베이스 연결 확인
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ 데이터베이스 연결 성공")
        return True
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return False


