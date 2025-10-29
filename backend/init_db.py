"""
데이터베이스 초기화 스크립트
MySQL 데이터베이스에 테이블 생성 및 초기 데이터 입력
"""
import sys
from pathlib import Path

# backend 디렉토리를 Python 경로에 추가
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.database import init_db, check_db_connection, SessionLocal
from app.models.db_models import Team, BettingModel


def insert_initial_data():
    """초기 데이터 입력"""
    db = SessionLocal()
    
    try:
        # 이미 데이터가 있는지 확인
        existing_teams = db.query(Team).count()
        if existing_teams > 0:
            print(f"⚠️  팀 데이터가 이미 존재합니다 ({existing_teams}개)")
            return
        
        print("📊 초기 데이터 입력 중...")
        
        # KBO 구단 정보
        teams = [
            Team(name='LG 트윈스', abbreviation='LG', stadium_name='잠실야구장', founded_year=1982),
            Team(name='두산 베어스', abbreviation='두산', stadium_name='잠실야구장', founded_year=1982),
            Team(name='삼성 라이온즈', abbreviation='삼성', stadium_name='대구삼성라이온즈파크', founded_year=1982),
            Team(name='KIA 타이거즈', abbreviation='KIA', stadium_name='광주-기아 챔피언스 필드', founded_year=1982),
            Team(name='NC 다이노스', abbreviation='NC', stadium_name='창원NC파크', founded_year=2011),
            Team(name='KT 위즈', abbreviation='KT', stadium_name='수원KT위즈파크', founded_year=2013),
            Team(name='SSG 랜더스', abbreviation='SSG', stadium_name='인천SSG랜더스필드', founded_year=2000),
            Team(name='한화 이글스', abbreviation='한화', stadium_name='대전한화생명이글스파크', founded_year=1986),
            Team(name='롯데 자이언츠', abbreviation='롯데', stadium_name='사직야구장', founded_year=1982),
            Team(name='키움 히어로즈', abbreviation='키움', stadium_name='고척스카이돔', founded_year=2008),
        ]
        
        db.bulk_save_objects(teams)
        print(f"✅ 팀 정보 {len(teams)}개 입력 완료")
        
        # 베팅 모델
        betting_models = [
            BettingModel(
                name='하이리턴',
                description='고수익 고위험 전략',
                min_confidence_threshold=0.55,
                min_ev_threshold=1000,
                max_kelly_percentage=0.25,
                risk_multiplier=1.2
            ),
            BettingModel(
                name='스탠다드',
                description='균형잡힌 전략',
                min_confidence_threshold=0.60,
                min_ev_threshold=500,
                max_kelly_percentage=0.15,
                risk_multiplier=1.0
            ),
            BettingModel(
                name='로우리스크',
                description='안정성 우선 전략',
                min_confidence_threshold=0.70,
                min_ev_threshold=300,
                max_kelly_percentage=0.10,
                risk_multiplier=0.8
            ),
        ]
        
        db.bulk_save_objects(betting_models)
        print(f"✅ 베팅 모델 {len(betting_models)}개 입력 완료")
        
        db.commit()
        print("✅ 모든 초기 데이터 입력 완료!")
        
    except Exception as e:
        print(f"❌ 초기 데이터 입력 실패: {e}")
        db.rollback()
    finally:
        db.close()


def verify_data():
    """데이터 확인"""
    db = SessionLocal()
    
    try:
        # 팀 확인
        teams = db.query(Team).all()
        print(f"\n📊 등록된 팀 ({len(teams)}개):")
        for team in teams:
            print(f"  - {team.name} ({team.abbreviation})")
        
        # 베팅 모델 확인
        models = db.query(BettingModel).all()
        print(f"\n⚙️  베팅 모델 ({len(models)}개):")
        for model in models:
            print(f"  - {model.name}: {model.description}")
        
    except Exception as e:
        print(f"❌ 데이터 확인 실패: {e}")
    finally:
        db.close()


def main():
    """메인 함수"""
    print("=" * 60)
    print("🚀 KBO 베팅 시스템 데이터베이스 초기화")
    print("=" * 60)
    
    # 1. 연결 확인
    print("\n🔍 데이터베이스 연결 확인 중...")
    if not check_db_connection():
        print("\n❌ 초기화 실패!")
        print("\n📋 체크리스트:")
        print("  1. MySQL 서버가 실행 중인가요?")
        print("  2. backend/.env 파일이 존재하고 올바르게 설정되어 있나요?")
        print("  3. 데이터베이스가 생성되어 있나요?")
        print("     mysql -u root -p -e 'CREATE DATABASE kbo_betting_db;'")
        return
    
    # 2. 테이블 생성
    print("\n🏗️  테이블 생성 중...")
    try:
        init_db()
    except Exception as e:
        print(f"❌ 테이블 생성 실패: {e}")
        return
    
    # 3. 초기 데이터 입력
    print("\n📥 초기 데이터 입력 중...")
    insert_initial_data()
    
    # 4. 데이터 확인
    print("\n🔍 데이터 확인 중...")
    verify_data()
    
    print("\n" + "=" * 60)
    print("✅ 데이터베이스 초기화 완료!")
    print("=" * 60)
    print("\n💡 다음 단계:")
    print("  1. 백엔드 서버 실행: python run.py")
    print("  2. API 문서 확인: http://localhost:8000/docs")
    print("  3. 프론트엔드 실행: cd ../frontend && npm start")


if __name__ == "__main__":
    main()


