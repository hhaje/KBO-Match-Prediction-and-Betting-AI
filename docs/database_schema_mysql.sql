-- KBO 경기 예측 및 AI 베팅 시스템
-- 데이터베이스 스키마 SQL (MySQL 버전)

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS kbo_betting_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE kbo_betting_db;

-- ==============================================
-- 1. 팀 정보 테이블
-- ==============================================
CREATE TABLE IF NOT EXISTS teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '팀명 (LG, 두산, 삼성 등)',
    abbreviation VARCHAR(10) COMMENT '팀 약칭',
    stadium_name VARCHAR(100) COMMENT '홈 구장 이름',
    founded_year INT COMMENT '창단 연도',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================
-- 2. 경기 정보 테이블
-- ==============================================
CREATE TABLE IF NOT EXISTS matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    match_date DATE NOT NULL COMMENT '경기 날짜',
    season INT NOT NULL COMMENT '연도',
    round INT COMMENT '라운드 번호',
    match_number INT COMMENT '경기 순번',
    stadium VARCHAR(100) COMMENT '경기장',
    
    -- 경기 결과
    home_score INT COMMENT '홈팀 점수',
    away_score INT COMMENT '원정팀 점수',
    winner VARCHAR(10) COMMENT 'winner: home/away, 확정되지 않음: NULL',
    is_completed BOOLEAN DEFAULT FALSE COMMENT '경기 종료 여부',
    
    -- 추가 정보
    weather VARCHAR(50) COMMENT '날씨 정보',
    attendance INT COMMENT '관중 수',
    innings INT COMMENT '이닝 수',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (home_team_id) REFERENCES teams(id),
    FOREIGN KEY (away_team_id) REFERENCES teams(id),
    UNIQUE KEY unique_match (season, round, match_number),
    INDEX idx_match_date (match_date),
    INDEX idx_teams (home_team_id, away_team_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================
-- 3. 선수 정보 테이블 (선택적)
-- ==============================================
CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    name VARCHAR(50) NOT NULL COMMENT '선수 이름',
    position VARCHAR(20) COMMENT '포지션 (투수, 타자 등)',
    jersey_number INT COMMENT '등번호',
    birth_date DATE COMMENT '생년월일',
    height_cm INT COMMENT '키',
    weight_kg INT COMMENT '몸무게',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (team_id) REFERENCES teams(id),
    INDEX idx_team (team_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================
-- 4. 경기 배당률 테이블
-- ==============================================
CREATE TABLE IF NOT EXISTS match_odds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    odds_provider VARCHAR(50) COMMENT '배당 제공처 (sportstoto 등)',
    home_team_odds DECIMAL(5,2) COMMENT '홈팀 승률',
    away_team_odds DECIMAL(5,2) COMMENT '원정팀 승률',
    draw_odds DECIMAL(5,2) COMMENT '무승부 배당률',
    
    captured_at TIMESTAMP COMMENT '배당률 수집 시각',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (match_id) REFERENCES matches(id),
    UNIQUE KEY unique_odds (match_id, odds_provider),
    INDEX idx_match (match_id),
    INDEX idx_captured_at (captured_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================
-- 5. AI 예측 결과 테이블
-- ==============================================
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    model_name VARCHAR(50) NOT NULL COMMENT '모델명 (lstm_v1, gru_v2 등)',
    
    -- 예측 확률 (0.0000 ~ 1.0000)
    home_win_probability DECIMAL(5,4) NOT NULL COMMENT '홈팀 승률',
    away_win_probability DECIMAL(5,4) NOT NULL COMMENT '원정팀 승률',
    
    -- 예측 정확도 지표
    confidence_score DECIMAL(5,4) COMMENT '모델 신뢰도',
    
    -- 베팅 추천
    recommended_bet VARCHAR(10) COMMENT 'recommend: home/away/pass',
    expected_value DECIMAL(8,2) COMMENT '기대값',
    kelly_percentage DECIMAL(5,4) COMMENT '켈리 포뮬러 추천 베팅 비율',
    
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (match_id) REFERENCES matches(id),
    UNIQUE KEY unique_prediction (match_id, model_name),
    INDEX idx_match (match_id),
    INDEX idx_model (model_name),
    INDEX idx_predicted_at (predicted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================
-- 6. 베팅 시뮬레이션 내역 테이블
-- ==============================================
CREATE TABLE IF NOT EXISTS betting_histories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    prediction_id INT,
    
    -- 베팅 정보
    betting_model VARCHAR(50) NOT NULL COMMENT '베팅 모델 (하이리턴, 스탠다드, 로우리스크)',
    bet_on VARCHAR(10) NOT NULL COMMENT 'bet_on: home/away',
    betting_amount DECIMAL(12,2) NOT NULL COMMENT '베팅 금액',
    
    -- 배당률 (베팅 당시)
    odds DECIMAL(5,2) COMMENT '받을 배당률',
    expected_profit DECIMAL(12,2) COMMENT '예상 수익',
    
    -- 실제 결과
    actual_result VARCHAR(10) COMMENT 'actual_result: win/loss',
    actual_profit DECIMAL(12,2) COMMENT '실제 수익/손실',
    
    bet_placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_updated_at TIMESTAMP NULL,
    
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (prediction_id) REFERENCES predictions(id),
    INDEX idx_match (match_id),
    INDEX idx_model (betting_model),
    INDEX idx_bet_placed_at (bet_placed_at),
    INDEX idx_result (actual_result)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================
-- 7. 베팅 모델 설정 테이블
-- ==============================================
CREATE TABLE IF NOT EXISTS betting_models (
    id INT AUTO_INCREMENT PRIMARY KEY,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 초기 베팅 모델 데이터
INSERT INTO betting_models (name, description, min_confidence_threshold, min_ev_threshold, max_kelly_percentage, risk_multiplier) VALUES
('하이리턴', '고수익 고위험 전략', 0.55, 1000, 0.25, 1.2),
('스탠다드', '균형잡힌 전략', 0.60, 500, 0.15, 1.0),
('로우리스크', '안정성 우선 전략', 0.70, 300, 0.10, 0.8);

-- ==============================================
-- 8. 모델 성능 지표 테이블
-- ==============================================
CREATE TABLE IF NOT EXISTS model_performances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL COMMENT '모델명',
    evaluation_period VARCHAR(20) COMMENT 'evaluation_period: 7일, 30일, 3개월 등',
    
    -- 예측 성능 지표
    accuracy DECIMAL(5,4) COMMENT '예측 정확도',
    log_loss DECIMAL(6,6) COMMENT 'Log Loss',
    brier_score DECIMAL(6,6) COMMENT 'Brier Score',
    
    -- 수익성 지표
    total_bets INT COMMENT '총 베팅 횟수',
    win_count INT COMMENT '승리 횟수',
    win_rate DECIMAL(5,4) COMMENT '승률',
    total_profit DECIMAL(12,2) COMMENT '총 수익',
    roi DECIMAL(6,2) COMMENT '투자 수익률 (%)',
    sharpe_ratio DECIMAL(5,4) COMMENT '샤프 비율',
    max_drawdown DECIMAL(6,2) COMMENT '최대 낙폭 (%)',
    
    evaluation_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_performance (model_name, evaluation_period, evaluation_date),
    INDEX idx_model (model_name),
    INDEX idx_evaluation_date (evaluation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================
-- 초기 데이터 입력 (KBO 구단)
-- ==============================================
INSERT INTO teams (name, abbreviation, stadium_name, founded_year) VALUES
('LG 트윈스', 'LG', '잠실야구장', 1982),
('두산 베어스', '두산', '잠실야구장', 1982),
('삼성 라이온즈', '삼성', '대구삼성라이온즈파크', 1982),
('KIA 타이거즈', 'KIA', '광주-기아 챔피언스 필드', 1982),
('NC 다이노스', 'NC', '창원NC파크', 2011),
('KT 위즈', 'KT', '수원KT위즈파크', 2013),
('SSG 랜더스', 'SSG', '인천SSG랜더스필드', 2000),
('한화 이글스', '한화', '대전한화생명이글스파크', 1986),
('롯데 자이언츠', '롯데', '사직야구장', 1982),
('키움 히어로즈', '키움', '고척스카이돔', 2008);

-- ==============================================
-- 뷰 생성 (자주 사용되는 쿼리)
-- ==============================================

-- 팀별 최근 성적 뷰
CREATE OR REPLACE VIEW team_recent_performance AS
SELECT 
    t.id AS team_id,
    t.name AS team_name,
    SUM(CASE 
        WHEN (m.home_team_id = t.id AND m.winner = 'home') OR 
             (m.away_team_id = t.id AND m.winner = 'away') 
        THEN 1 ELSE 0 
    END) AS wins,
    SUM(CASE 
        WHEN (m.home_team_id = t.id AND m.winner = 'away') OR 
             (m.away_team_id = t.id AND m.winner = 'home') 
        THEN 1 ELSE 0 
    END) AS losses,
    COUNT(*) AS total_games
FROM teams t
LEFT JOIN matches m ON (m.home_team_id = t.id OR m.away_team_id = t.id) AND m.is_completed = TRUE
GROUP BY t.id, t.name;


