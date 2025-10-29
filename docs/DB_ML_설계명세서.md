# KBO 경기 예측 및 AI 베팅 시스템
## DB 및 ML 모델 설계 명세서

---

## 1. 데이터베이스 설계 개요

### 1.1 목표
- KBO 경기, 팀, 선수 데이터 저장 및 관리
- AI 예측 결과 및 배당률 데이터 저장
- 베팅 시뮬레이션 내역 관리
- 성과 분석 및 리스크 관리 데이터 제공

### 1.2 기술 스택
- **DBMS**: PostgreSQL 12+ 또는 MySQL 8+
- **ORM**: SQLAlchemy (Python)
- **백업**: 일일 자동 백업, 증분 백업

---

## 2. 데이터베이스 스키마 설계

### 2.1 핵심 엔티티

#### 2.1.1 teams (팀)

```sql
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '팀명 (LG, 두산, 삼성 등)',
    abbreviation VARCHAR(10) COMMENT '팀 약칭',
    stadium_name VARCHAR(100) COMMENT '홈 구장 이름',
    founded_year INTEGER COMMENT '창단 연도',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**데이터 요구사항:**
- KBO 10개 구단 정보 입력
- 팀명, 약칭, 홈 구장, 창단 연도 포함

---

#### 2.1.2 matches (경기)

```sql
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    home_team_id INTEGER NOT NULL REFERENCES teams(id),
    away_team_id INTEGER NOT NULL REFERENCES teams(id),
    match_date DATE NOT NULL COMMENT '경기 날짜',
    season INTEGER NOT NULL COMMENT '연도',
    round INTEGER COMMENT '라운드 번호',
    match_number INTEGER COMMENT '경기 순번',
    stadium VARCHAR(100) COMMENT '경기장',
    
    -- 경기 결과
    home_score INTEGER COMMENT '홈팀 점수',
    away_score INTEGER COMMENT '원정팀 점수',
    winner VARCHAR(10) COMMENT 'winner: home/away, 확정되지 않음: NULL',
    is_completed BOOLEAN DEFAULT FALSE COMMENT '경기 종료 여부',
    
    -- 추가 정보
    weather VARCHAR(50) COMMENT '날씨 정보',
    attendance INTEGER COMMENT '관중 수',
    innings INTEGER COMMENT '이닝 수',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE(season, round, match_number),
    INDEX idx_match_date (match_date),
    INDEX idx_teams (home_team_id, away_team_id)
);
```

**데이터 요구사항:**
- 시뮬레이션 대상 경기 정보
- 과거 경기 결과 포함 (학습 데이터용)
- 홈/원정 매치업, 경기 날짜, 결과

---

#### 2.1.3 players (선수)

```sql
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams(id),
    name VARCHAR(50) NOT NULL COMMENT '선수 이름',
    position VARCHAR(20) COMMENT '포지션 (투수, 타자 등)',
    jersey_number INTEGER COMMENT '등번호',
    birth_date DATE COMMENT '생년월일',
    height_cm INTEGER COMMENT '키',
    weight_kg INTEGER COMMENT '몸무게',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_team (team_id)
);
```

**데이터 요구사항:**
- 향후 확장 기능 (현재는 선택적)
- 선수 통계 연계 가능

---

#### 2.1.4 match_odds (배당률)

```sql
CREATE TABLE match_odds (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    odds_provider VARCHAR(50) COMMENT '배당 제공처 (sportstoto 등)',
    home_team_odds DECIMAL(5,2) COMMENT '홈팀 승률',
    away_team_odds DECIMAL(5,2) COMMENT '원정팀 승률',
    draw_odds DECIMAL(5,2) COMMENT '무승부 배당률 (야구는 없을 수도 있음)',
    
    captured_at TIMESTAMP COMMENT '배당률 수집 시각',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE(match_id, odds_provider),
    INDEX idx_match (match_id),
    INDEX idx_captured_at (captured_at)
);
```

**데이터 요구사항:**
- AI 예측과 비교하여 베팅 가치(Expected Value) 계산
- 여러 배당률 제공처 지원 (선택적)

---

#### 2.1.5 predictions (AI 예측 결과)

```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    model_name VARCHAR(50) NOT NULL COMMENT '모델명 (lstm_v1, gru_v2 등)',
    
    -- 예측 확률
    home_win_probability DECIMAL(5,4) NOT NULL COMMENT '0.0000 ~ 1.0000',
    away_win_probability DECIMAL(5,4) NOT NULL COMMENT '0.0000 ~ 1.0000',
    
    -- 예측 정확도 지표
    confidence_score DECIMAL(5,4) COMMENT '모델 신뢰도',
    
    -- 베팅 추천
    recommended_bet VARCHAR(10) COMMENT 'recommend: home/away/pass',
    expected_value DECIMAL(8,2) COMMENT '기대값',
    kelly_percentage DECIMAL(5,4) COMMENT '켈리 포뮬러 추천 베팅 비율',
    
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(match_id, model_name),
    INDEX idx_match (match_id),
    INDEX idx_model (model_name),
    INDEX idx_predicted_at (predicted_at)
);
```

**데이터 요구사항:**
- 각 경기별 AI 예측 확률 저장
- 여러 모델의 예측 결과 비교 가능
- 예측 모델 성능 평가 용도

---

#### 2.1.6 betting_histories (베팅 시뮬레이션 내역)

```sql
CREATE TABLE betting_histories (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    prediction_id INTEGER REFERENCES predictions(id),
    
    -- 베팅 정보
    betting_model VARCHAR(50) NOT NULL COMMENT '베팅 모델 (하이리턴, 스탠다드, 로우리스크)',
    bet_on VARCHAR(10) NOT NULL COMMENT 'bet_on: home/away',
    betting_amount DECIMAL(12,2) NOT NULL COMMENT '베팅 금액',
    
    -- 배당률 (베팅 당시)
    odds DECIMAL(5,2) COMMENT '받을 배당률',
    expected_profit DECIMAL(12,2) COMMENT '예상 수익',
    
    -- 실제 결과
    actual_result VARCHAR(10) COMMENT 'actual_result: win/loss (경기 종료 후)',
    actual_profit DECIMAL(12,2) COMMENT '실제 수익/손실',
    
    bet_placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_updated_at TIMESTAMP,
    
    INDEX idx_match (match_id),
    INDEX idx_model (betting_model),
    INDEX idx_bet_placed_at (bet_placed_at),
    INDEX idx_result (actual_result)
);
```

**데이터 요구사항:**
- AI 예측 기반 베팅 시뮬레이션 결과 저장
- 실제 경기 결과와 비교하여 성과 분석
- 베팅 모델별 성능 추적

---

#### 2.1.7 betting_models (베팅 모델 설정)

```sql
CREATE TABLE betting_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '모델명 (하이리턴, 스탠다드, 로우리스크)',
    description TEXT COMMENT '모델 설명',
    
    -- 베팅 전략 파라미터
    min_confidence_threshold DECIMAL(5,4) COMMENT '최소 신뢰도 임계값',
    min_ev_threshold DECIMAL(8,2) COMMENT '최소 기대값 임계값',
    max_kelly_percentage DECIMAL(5,4) COMMENT '최대 켈리 비율',
    risk_multiplier DECIMAL(5,4) COMMENT '리스크 배수',
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**데이터 요구사항:**
- 베팅 모델 3종류 설정:
  - **하이리턴**: 고수익/고위험 전략, EV 임계값 높음
  - **스탠다드**: 균형 전략
  - **로우리스크**: 안정성 우선, 신뢰도 임계값 높음

---

#### 2.1.8 model_performances (모델 성능 지표)

```sql
CREATE TABLE model_performances (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL COMMENT '모델명',
    evaluation_period VARCHAR(20) COMMENT 'evaluation_period: 7일, 30일, 3개월 등',
    
    -- 예측 성능 지표
    accuracy DECIMAL(5,4) COMMENT '예측 정확도 (승/패 맞춘 비율)',
    log_loss DECIMAL(6,6) COMMENT 'Log Loss',
    brier_score DECIMAL(6,6) COMMENT 'Brier Score',
    
    -- 수익성 지표
    total_bets INTEGER COMMENT '총 베팅 횟수',
    win_count INTEGER COMMENT '승리 횟수',
    win_rate DECIMAL(5,4) COMMENT '승률',
    total_profit DECIMAL(12,2) COMMENT '총 수익',
    roi DECIMAL(6,2) COMMENT '투자 수익률 (%)',
    sharpe_ratio DECIMAL(5,4) COMMENT '샤프 비율',
    max_drawdown DECIMAL(6,2) COMMENT '최대 낙폭 (%)',
    
    evaluation_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_model (model_name),
    INDEX idx_evaluation_date (evaluation_date),
    UNIQUE(model_name, evaluation_period, evaluation_date)
);
```

**데이터 요구사항:**
- 모델별 성능 지표 주기적 업데이트
- 대시보드 표시용 데이터

---

### 2.2 관계 다이어그램

```
teams (1) ──< (N) matches >── (N) players
               │
               ├── (1) match_odds
               │
               ├── (N) predictions
               │     │
               │     └── (N) betting_histories
               │
               └── (N) betting_histories

betting_models (1) ──< (N) betting_histories

model_performances (독립)
```

---

## 3. ML 모델 설계 명세

### 3.1 모델 아키텍처 개요

#### 모델 타입
1. **LSTM (Long Short-Term Memory)**
   - 과거 N경기 시계열 데이터 활용
   - 장기 의존성 학습

2. **GRU (Gated Recurrent Unit)**
   - LSTM보다 효율적인 학습
   - 계산 효율성과 성능의 균형

3. **Transformer (선택적)**
   - 어텐션 메커니즘 활용
   - 팀 특성 간 관계 학습

4. **Ensemble**
   - 다중 모델 결과 결합
   - 가중 평균 및 스태킹 기법

---

#### 3.2 모델 입력 특성 (Input Features)

```python
# 시계열 특성 (팀별 최근 N경기)
team_features = {
    # 팀 성과 지표
    'recent_wins': 10,           # 최근 10경기 승수
    'recent_losses': 10,          # 최근 10경기 패수
    'win_rate_10': 0.65,         # 최근 10경기 승률
    'avg_score': 5.2,             # 평균 득점
    'avg_allowed': 4.1,           # 평균 실점
    
    # 공격 지표
    'avg_hit_rate': 0.285,        # 평균 타율
    'avg_on_base': 0.352,         # 평균 출루율
    'avg_slugging': 0.445,        # 평균 장타율
    'avg_home_runs': 1.2,         # 평균 홈런
    
    # 수비 지표
    'avg_era': 4.15,              # 평균 방어율
    'avg_whip': 1.38,             # 평균 WHIP
    'avg_strikeout_rate': 0.20,   # 삼진율
    'avg_hit_allowed': 8.5,       # 평균 피안타
    
    # 시즌 통계
    'season_wins': 72,            # 시즌 총 승수
    'season_losses': 48,          # 시즌 총 패수
    'season_rank': 3,             # 현재 순위
    'head_to_head_wins': 8,       # 상대전적 승수
    'head_to_head_losses': 5,     # 상대전적 패수
}

# 경기 특성
match_features = {
    'is_home': 1,                 # 홈/원정 (1/0)
    'travel_distance': 150,       # 이동 거리 (km)
    'rest_days': 1,               # 휴식일 수
    'weather_temp': 15.5,         # 기온
    'weather_wind': 8.2,          # 풍속
    'home_fatigue': 0.3,          # 피로도 지수
    'away_fatigue': 0.4,          # 피로도 지수
}

# 최근 경기 결과 (시계열)
recent_matches = [
    # 최근 5경기 결과
    {'score': 6, 'allowed': 3, 'win': 1},
    {'score': 5, 'allowed': 4, 'win': 1},
    {'score': 2, 'allowed': 7, 'win': 0},
    {'score': 8, 'allowed': 2, 'win': 1},
    {'score': 4, 'allowed': 4, 'win': 0},
]
```

---

#### 3.3 모델 출력 (Output)

```python
predictions = {
    'home_win_probability': 0.652,    # 홈팀 승률
    'away_win_probability': 0.348,    # 원정팀 승률
    'confidence_score': 0.82,         # 모델 신뢰도
    'predicted_score_diff': 2.3,      # 예상 점수차
}
```

---

#### 3.4 확률 보정 (Probability Calibration)

**목적**: 모델의 예측 확률을 실제 확률 분포에 맞게 보정

```python
from sklearn.calibration import CalibratedClassifierCV

# Temperature Scaling 적용
def calibrate_probability(predictions):
    # 모델 출력 확률을 실제 확률 분포에 맞게 보정
    calibrated_prob = temperature_scaling(predictions, calibration_data)
    return calibrated_prob
```

**보정 방법:**
- Platt Scaling
- Isotonic Regression
- Temperature Scaling

---

### 3.5 모델 학습 파이프라인

```python
# 프로젝트 구조
models/
├── lstm_model.py              # LSTM 모델 정의
├── gru_model.py               # GRU 모델 정의
├── transformer_model.py       # Transformer 모델 정의
├── ensemble_model.py          # 앙상블 모델
├── calibration.py             # 확률 보정
├── train.py                   # 학습 스크립트
└── evaluate.py                # 평가 스크립트
```

**학습 프로세스:**
1. 데이터 수집 및 정제
2. 특성 추출 및 정규화
3. 시계열 시퀀스 생성
4. Train/Validation/Test Split
5. 모델 학습 (Early Stopping)
6. 교차 검증 (K-Fold)
7. 확률 보정
8. 성능 평가 (Log Loss, Brier Score)

---

## 4. API 인터페이스 설계

### 4.1 주요 엔드포인트

```python
# FastAPI 백엔드 구조
@app.post("/api/predict")
async def predict_match(match_id: int, model_name: str):
    """경기 예측 생성"""
    prediction = predict_service.generate_prediction(match_id, model_name)
    return prediction

@app.get("/api/matches")
async def get_matches(start_date: str, end_date: str):
    """경기 목록 조회"""
    matches = match_service.get_matches_by_date_range(start_date, end_date)
    return matches

@app.get("/api/betting-results")
async def get_betting_results(model: str, period: str):
    """베팅 결과 조회"""
    results = betting_service.get_results(model, period)
    return results

@app.get("/api/performance")
async def get_model_performance(model_name: str, period: str):
    """모델 성능 지표 조회"""
    performance = performance_service.get_performance(model_name, period)
    return performance
```

---

## 5. 데이터 수집 및 관리

### 5.1 데이터 수집 소스
- **KBO 공식 통계**
- **스포츠토토 배당률**
- **기상청 날씨 데이터**

### 5.2 ETL 파이프라인
- **데이터 수집**: Cron 스케줄링, 일일 업데이트
- **데이터 검증 및 정제**: 결측값 처리, 이상치 제거
- **데이터 저장**: PostgreSQL 인증 저장
- **데이터 업데이트**: 증분 업데이트, 중복 방지
- **버전 관리**: 날짜별 버전 관리
- **모니터링**: 자동 성능 모니터링 및 알림

---

## 6. 성능 및 모니터링

### 6.1 데이터베이스
- **인덱스 최적화**: 자주 조회되는 컬럼에 인덱스 추가
- **쿼리 최적화**: EXPLAIN 분석, JOIN 최적화
- **백업**: 일일 자동 백업, 주간 전체 백업

### 6.2 ML 모델
- **모델 성능 지표**: Accuracy, Log Loss, Brier Score, ROI
- **모니터링**: 예측 성능 추이, 이상 탐지, 자동 재학습

---

## 7. 데이터 흐름

1. 경기 예정 발표 → 경기 정보 수집 → DB 저장
2. AI 모델 실행 → 경기 예측 확률 생성 → DB 저장
3. 베팅 시뮬레이션 → 베팅 결정 → DB 저장
4. 경기 종료 → 결과 업데이트 → 성과 분석 → 대시보드 표시

---



