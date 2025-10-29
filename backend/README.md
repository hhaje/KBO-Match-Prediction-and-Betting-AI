# KBO 경기 예측 AI 베팅 시스템 - 백엔드

FastAPI 기반 백엔드 서버

## 설치

### 1. Python 가상환경 생성

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
# env.template을 복사하여 .env 파일 생성
cp env.template .env

# .env 파일을 편집하여 데이터베이스 정보 입력
# DB_HOST, DB_USER, DB_PASSWORD 등
```

### 4. MySQL 데이터베이스 설정

**자세한 설정 가이드:** [MySQL 설정 가이드](../docs/MySQL_설정_가이드.md)

```bash
# MySQL에 데이터베이스 생성
mysql -u root -p -e "CREATE DATABASE kbo_betting_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 스키마 생성 (방법 1: SQL 스크립트 사용)
mysql -u root -p kbo_betting_db < ../docs/database_schema_mysql.sql

# 또는 (방법 2: Python 초기화 스크립트 사용)
python init_db.py
```

## 실행

### 개발 서버 실행

```bash
# 프로젝트 루트에서 실행
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

또는

```bash
python app/main.py
```

### API 문서 확인

서버 실행 후 다음 URL로 접속:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

### 경기 관련 (`/api/matches`)

- `GET /api/matches/` - 경기 목록 조회
- `GET /api/matches/upcoming` - 예정된 경기 조회
- `GET /api/matches/recent` - 최근 경기 결과 조회
- `GET /api/matches/{match_id}` - 특정 경기 조회

### 예측 관련 (`/api/predictions`)

- `POST /api/predictions/generate` - 경기 예측 생성
- `GET /api/predictions/{match_id}` - 경기 예측 조회
- `GET /api/predictions/{match_id}/all` - 모든 모델 예측 조회

### 베팅 관련 (`/api/betting`)

- `GET /api/betting/results` - 베팅 결과 조회
- `GET /api/betting/models/stats` - 모든 베팅 모델 통계
- `GET /api/betting/models/{model_name}/stats` - 특정 베팅 모델 통계
- `POST /api/betting/recommend` - 베팅 추천 계산

### 성능 관련 (`/api/performance`)

- `GET /api/performance/model` - 모델 성능 지표 조회
- `GET /api/performance/model/compare` - 모델 성능 비교
- `GET /api/performance/profit` - 수익 분석 데이터
- `GET /api/performance/chart` - ROI 추이 차트 데이터

## 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션
│   ├── database.py             # 데이터베이스 연결 설정
│   ├── api/                    # API 엔드포인트
│   │   ├── matches.py
│   │   ├── predictions.py
│   │   ├── betting.py
│   │   └── performance.py
│   ├── services/               # 비즈니스 로직
│   │   ├── match_service.py
│   │   ├── prediction_service.py
│   │   ├── betting_service.py
│   │   └── performance_service.py
│   ├── models/                 # 데이터 모델
│   │   ├── schemas.py          # Pydantic 스키마
│   │   └── db_models.py        # SQLAlchemy ORM 모델
│   └── data/                   # 데이터 처리
│       └── mock_data.py        # 모의 데이터 (임시)
├── init_db.py                  # DB 초기화 스크립트
├── run.py                      # 서버 실행 스크립트
├── env.template                # 환경 변수 템플릿
├── .env                        # 환경 변수 (Git에서 제외)
├── requirements.txt
└── README.md
```

## 현재 구현 상태

✅ **완료:**
- FastAPI 기본 구조
- API 엔드포인트 (경기, 예측, 베팅, 성능)
- 서비스 레이어
- 모의 데이터 생성
- CORS 설정
- API 문서 자동 생성

⏳ **진행 중:**
- ✅ MySQL 데이터베이스 스키마 설계
- ✅ SQLAlchemy ORM 모델 작성
- ⏳ 서비스 레이어 DB 통합
- ⏳ 실제 ML 모델 개발 및 통합
- ⏳ KBO 데이터 수집 자동화

⏳ **향후 구현:**
- 인증/인가 (JWT)
- 로깅 및 모니터링
- 테스트 코드
- Docker 컨테이너화

## 데이터베이스 및 ML 모델 통합

현재는 모의 데이터를 사용하고 있습니다. 실제 DB와 ML 모델 준비 시:

1. **데이터베이스 통합:**
   - `app/models/database.py` 추가 (SQLAlchemy 모델)
   - `app/db/` 디렉토리 생성 (DB 연결 설정)
   - 각 서비스에서 `mock_data` 대신 DB 쿼리 사용

2. **ML 모델 통합:**
   - `app/ml/` 디렉토리 생성 (모델 로더, 전처리)
   - `prediction_service.py`에서 실제 모델 호출
   - 모델 파일 경로 설정

## 테스트

```bash
# 간단한 테스트
curl http://localhost:8000/health

# 경기 목록 조회
curl http://localhost:8000/api/matches/

# 베팅 결과 조회
curl http://localhost:8000/api/betting/results
```

## 문제 해결

### 포트 이미 사용 중

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### 패키지 설치 오류

```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```


