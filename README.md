# KBO Match Prediction and Betting AI

## 📋 프로젝트 개요

이 프로젝트는 스포츠 경기 데이터를 기반으로 승부를 예측하고, 이를 활용해 자동화된 베팅 전략을 수립·평가하는 AI 연구입니다. 주요 목표는 딥러닝 모델을 통해 경기 결과의 확률을 예측하고, 예측값과 실제 배당률을 결합하여 최적의 베팅 의사결정을 도출하는 것입니다.

### 🎯 연구 목표
- **예측 정확도 향상**: 딥러닝 모델을 통한 경기 결과 확률 예측
- **수익성 최적화**: 예측값과 배당률을 결합한 베팅 전략 수립
- **리스크 관리**: 안정적이고 지속가능한 투자 전략 개발
- **실시간 모니터링**: 웹 기반 대시보드를 통한 성과 추적

## 🏟️ 연구 범위

### 주요 대상
- **KBO (한국프로야구)**: 공인 경기 기록 및 스포츠토토 배당 데이터 활용
- **시계열 데이터**: 팀 성과, 선수 통계, 경기 조건 등 다차원 데이터 분석

### 기술적 접근
- **데이터베이스**: SQL 기반 데이터 저장 및 관리
- **ETL 파이프라인**: 데이터 수집-정제-적재 프로세스 자동화
- **딥러닝 모델**: LSTM, GRU 등 시계열 예측 모델 적용
- **확률 보정**: Calibration을 통한 예측 신뢰도 향상
- **백테스트**: 과거 데이터를 활용한 전략 검증

## 🛠️ 기술 스택

### 데이터 처리
- **Database**: PostgreSQL / MySQL
- **ETL**: Python, Pandas, SQLAlchemy
- **데이터 수집**: Web Scraping, API 연동

### 머신러닝
- **Framework**: TensorFlow / PyTorch
- **모델**: LSTM, GRU, Transformer
- **전처리**: Scikit-learn, NumPy

### 웹 개발
- **Frontend**: React.js
- **Backend**: FastAPI
- **시각화**: D3.js, Chart.js, Plotly

### 인프라
- **배포**: Docker, AWS / GCP
- **모니터링**: Grafana, Prometheus
- **버전 관리**: Git, GitHub Actions

## 📊 성과 지표

### 정량적 평가 지표
- **수익률 (ROI)**: 투자 대비 수익률
- **예측 정확도**: LogLoss, Brier Score
- **안정성**: Maximum Drawdown (MDD)
- **시장 효율성**: CLV (Calibration Loss Variance)

### 보조 지표
- **EV 캡처율**: Expected Value 달성률
- **리스크 효율**: 위험 대비 수익률
- **샤프 비율**: 위험 조정 수익률

## 🚀 설치 및 실행

### 사전 요구사항
```bash
Python 3.8+
Node.js 16+
```

### 빠른 시작 (Windows)

```bash
# 1. 백엔드 서버 시작
start_backend.bat

# 2. 새 터미널에서 프론트엔드 시작
cd frontend
npm install
npm start
```

### 빠른 시작 (Linux/Mac)

```bash
# 1. 백엔드 서버 시작
chmod +x start_backend.sh
./start_backend.sh

# 2. 새 터미널에서 프론트엔드 시작
cd frontend
npm install
npm start
```

### 수동 설치 및 실행

#### 백엔드 설정
```bash
# Python 가상환경 생성
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python run.py
```

#### 프론트엔드 설정
```bash
cd frontend
npm install
npm start
```

### API 문서 확인

백엔드 서버 실행 후:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 백엔드 API 테스트

```bash
cd backend
python test_api.py
```

## 📁 프로젝트 구조

```
KBO match data and AI-powered match prediction-betting model and monetization/
├── backend/                    # 백엔드 (FastAPI)
│   ├── app/
│   │   ├── api/               # API 엔드포인트
│   │   │   ├── matches.py     # 경기 관련 API
│   │   │   ├── predictions.py # 예측 관련 API
│   │   │   ├── betting.py     # 베팅 관련 API
│   │   │   └── performance.py # 성능 관련 API
│   │   ├── services/          # 비즈니스 로직
│   │   ├── models/            # Pydantic 스키마
│   │   └── data/              # 모의 데이터 (임시)
│   ├── run.py                 # 서버 실행 스크립트
│   ├── test_api.py            # API 테스트
│   └── requirements.txt       # Python 패키지
├── frontend/                  # 프론트엔드 (React)
│   ├── src/
│   │   ├── components/       # React 컴포넌트
│   │   │   └── Dashboard/    # 대시보드 컴포넌트
│   │   ├── services/         # API 서비스
│   │   └── pages/            # 페이지 컴포넌트
│   ├── public/
│   └── package.json
├── docs/                      # 문서
│   ├── DB_ML_설계명세서.md    # DB 및 ML 모델 설계 명세
│   ├── database_schema.sql    # 데이터베이스 스키마
│   ├── model_structure_example.py  # ML 모델 예제
│   └── 구현가이드.md          # 구현 가이드
├── start_backend.bat          # Windows 백엔드 시작 스크립트
├── start_backend.sh           # Linux/Mac 백엔드 시작 스크립트
└── README.md                  # 프로젝트 README
```

## 🎯 현재 구현 상태

### ✅ 완료
- FastAPI 백엔드 구조
- React 프론트엔드 대시보드
- API 엔드포인트 (경기, 예측, 베팅, 성능)
- 모의 데이터 시스템
- DB 및 ML 모델 설계 명세서

### ⏳ 향후 구현 (명세서 참고)
- PostgreSQL 데이터베이스 연결
- 실제 KBO 데이터 수집
- LSTM/GRU 모델 학습
- 예측 시스템 통합
- 실시간 베팅 시뮬레이션

## 🔄 데이터 파이프라인

### 1. 데이터 수집 (Extract)
- KBO 공식 통계 데이터 수집
- 스포츠토토 배당률 데이터 수집
- 날씨, 부상 등 외부 요인 데이터 수집

### 2. 데이터 정제 (Transform)
- 데이터 정합성 검증
- 결측값 처리 및 이상치 제거
- 특성 엔지니어링 및 정규화

### 3. 데이터 적재 (Load)
- 정제된 데이터를 데이터베이스에 저장
- 데이터 버전 관리 및 백업

## 🤖 모델링 접근법

### 시계열 예측 모델
- **LSTM**: 장기 의존성 학습
- **GRU**: 계산 효율성과 성능의 균형
- **Transformer**: 어텐션 메커니즘을 활용한 패턴 학습

### 앙상블 방법
- 다중 모델 예측 결과 결합
- 가중 평균 및 스태킹 기법 적용

### 확률 보정 (Calibration)
- Platt Scaling
- Isotonic Regression
- Temperature Scaling

## 📈 웹 대시보드 기능

### 실시간 모니터링
- 모델 예측 결과 시각화
- 누적 수익률 추이
- 경기별 베팅 시뮬레이션
- 강화학습 상태변수 추이

### 분석 도구
- 성과 지표 대시보드
- 리스크 분석 차트
- 포트폴리오 최적화 도구

## 🧪 테스트 및 검증

### 백테스트
```bash
# 과거 데이터를 활용한 전략 검증
python scripts/backtest.py --start-date 2020-01-01 --end-date 2023-12-31
```

### 단위 테스트
```bash
# 테스트 실행
pytest tests/
```

### 모델 검증
```bash
# 교차 검증 및 성능 평가
python scripts/evaluate_model.py
```

## 📚 참고 문헌

- [Deep Learning for Sports Betting](https://example.com)
- [Time Series Forecasting with LSTM](https://example.com)
- [Calibration in Machine Learning](https://example.com)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 연락처

프로젝트 링크: [https://github.com/hhaje/KBO-Match-Prediction-and-Betting-AI](https://github.com/hhaje/KBO-Match-Prediction-and-Betting-AI)

## ⚠️ 면책 조항

이 프로젝트는 연구 및 교육 목적으로 제작되었습니다. 실제 베팅에 사용할 경우 발생하는 모든 손실에 대해 개발자는 책임지지 않습니다. 베팅은 위험을 수반하며, 신중한 판단과 책임감 있는 투자가 필요합니다.

---

**⚡ AI가 단순 예측을 넘어 실제 경제적 의사결정과 수익 창출로 확장될 수 있음을 보여주는 실증적 사례**
