-- KBO 경기 예측 및 AI 베팅 시스템
-- 데이터베이스 스키마 SQL
-- PostgreSQL 버전

-- ==============================================
-- 1. 팀 정보 테이블
-- ==============================================
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    abbreviation VARCHAR(10),
    stadium_name VARCHAR(100),
    founded_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE teams IS 'KBO 구단 정보';
COMMENT ON COLUMN teams.name IS '팀명 (LG, 두산, 삼성 등)';
COMMENT ON COLUMN teams.abbreviation IS '팀 약칭';
COMMENT ON COLUMN teams.stadium_name IS '홈 구장 이름';

-- ==============================================
-- 2. 경기 정보 테이블
-- ==============================================
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    home_team_id INTEGER NOT NULL REFERENCES teams(id),
    away_team_id INTEGER NOT NULL REFERENCES teams(id),
    match_date DATE NOT NULL,
    season INTEGER NOT NULL,
    round INTEGER,
    match_number INTEGER,
    stadium VARCHAR(100),
    
    -- 경기 결과
    home_score INTEGER,
    away_score INTEGER,
    winner VARCHAR(10), -- 'home' or 'away'
    is_completed BOOLEAN DEFAULT FALSE,
    
    -- 추가 정보
    weather VARCHAR(50),
    attendance INTEGER,
    innings INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(season, round, match_number)
);

COMMENT ON TABLE matches IS '경기 정보 및 결과';
COMMENT ON COLUMN matches.winner IS 'winner: home/away, 확정되지 않음: NULL';
COMMENT ON COLUMN matches.is_completed IS '경기 종료 여부';

-- 인덱스
CREATE INDEX idx_match_date ON matches(match_date);
CREATE INDEX idx_teams ON matches(home_team_id, away_team_id);

-- ==============================================
-- 3. 선수 정보 테이블 (선택적)
-- ==============================================
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams(id),
    name VARCHAR(50) NOT NULL,
    position VARCHAR(20),
    jersey_number INTEGER,
    birth_date DATE,
    height_cm INTEGER,
    weight_kg INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE players IS '선수 정보 (향후 확장용)';

CREATE INDEX idx_team ON players(team_id);

-- ==============================================
-- 4. 경기 배당률 테이블
-- ==============================================
CREATE TABLE match_odds (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    odds_provider VARCHAR(50),
    home_team_odds DECIMAL(5,2),
    away_team_odds DECIMAL(5,2),
    draw_odds DECIMAL(5,2),
    
    captured_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(match_id, odds_provider)
);

COMMENT ON TABLE match_odds IS '경기 배당률 정보';
COMMENT ON COLUMN match_odds.odds_provider IS '배당 제공처 (sportstoto 등)';

CREATE INDEX idx_match ON match_odds(match_id);
CREATE INDEX idx_captured_at ON match_odds(captured_at);

-- ==============================================
-- 5. AI 예측 결과 테이블
-- ==============================================
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    model_name VARCHAR(50) NOT NULL,
    
    -- 예측 확률 (0.0000 ~ 1.0000)
    home_win_probability DECIMAL(5,4) NOT NULL,
    away_win_probability DECIMAL(5,4) NOT NULL,
    
    -- 예측 정확도 지표
    confidence_score DECIMAL(5,4),
    
    -- 베팅 추천
    recommended_bet VARCHAR(10), -- 'home', 'away', 'pass'
    expected_value DECIMAL(8,2),
    kelly_percentage DECIMAL(5,4),
    
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(match_id, model_name)
);

COMMENT ON TABLE predictions IS 'AI 모델 예측 결과';
COMMENT ON COLUMN predictions.home_win_probability IS '홈팀 승률 (0.0000 ~ 1.0000)';
COMMENT ON COLUMN predictions.confidence_score IS '모델 신뢰도';
COMMENT ON COLUMN predictions.recommended_bet IS 'recommend: home/away/pass';
COMMENT ON COLUMN predictions.kelly_percentage IS '켈리 포뮬러 추천 베팅 비율';

CREATE INDEX idx_match ON predictions(match_id);
CREATE INDEX idx_model ON predictions(model_name);
CREATE INDEX idx_predicted_at ON predictions(predicted_at);

-- ==============================================
-- 6. 베팅 시뮬레이션 내역 테이블
-- ==============================================
CREATE TABLE betting_histories (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id),
    prediction_id INTEGER REFERENCES predictions(id),
    
    -- 베팅 정보
    betting_model VARCHAR(50) NOT NULL,
    bet_on VARCHAR(10) NOT NULL, -- 'home' or 'away'
    betting_amount DECIMAL(12,2) NOT NULL,
    
    -- 배당률 (베팅 당시)
    odds DECIMAL(5,2),
    expected_profit DECIMAL(12,2),
    
    -- 실제 결과
    actual_result VARCHAR(10), -- 'win' or 'loss'
    actual_profit DECIMAL(12,2),
    
    bet_placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_updated_at TIMESTAMP
);

COMMENT ON TABLE betting_histories IS '베팅 시뮬레이션 내역';
COMMENT ON COLUMN betting_histories.betting_model IS '베팅 모델 (하이리턴, 스탠다드, 로우리스크)';
COMMENT ON COLUMN betting_histories.bet_on IS 'bet_on: home/away';
COMMENT ON COLUMN betting_histories.actual_result IS 'actual_result: win/loss';

CREATE INDEX idx_match ON betting_histories(match_id);
CREATE INDEX idx_model ON betting_histories(betting_model);
CREATE INDEX idx_bet_placed_at ON betting_histories(bet_placed_at);
CREATE INDEX idx_result ON betting_histories(actual_result);

-- ==============================================
-- 7. 베팅 모델 설정 테이블
-- ==============================================
CREATE TABLE betting_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    
    -- 베팅 전략 파라미터
    min_confidence_threshold DECIMAL(5,4),
    min_ev_threshold DECIMAL(8,2),
    max_kelly_percentage DECIMAL(5,4),
    risk_multiplier DECIMAL(5,4),
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE betting_models IS '베팅 모델 설정';
COMMENT ON COLUMN betting_models.name IS '모델명 (하이리턴, 스탠다드, 로우리스크)';
COMMENT ON COLUMN betting_models.min_confidence_threshold IS '최소 신뢰도 임계값';
COMMENT ON COLUMN betting_models.min_ev_threshold IS '최소 기대값 임계값';
COMMENT ON COLUMN betting_models.max_kelly_percentage IS '최대 켈리 비율';
COMMENT ON COLUMN betting_models.risk_multiplier IS '리스크 배수';

-- 초기 베팅 모델 데이터
INSERT INTO betting_models (name, description, min_confidence_threshold, min_ev_threshold, max_kelly_percentage, risk_multiplier) VALUES
('하이리턴', '고수익 고위험 전략', 0.55, 1000, 0.25, 1.2),
('스탠다드', '균형잡힌 전략', 0.60, 500, 0.15, 1.0),
('로우리스크', '안정성 우선 전략', 0.70, 300, 0.10, 0.8);

-- ==============================================
-- 8. 모델 성능 지표 테이블
-- ==============================================
CREATE TABLE model_performances (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    evaluation_period VARCHAR(20),
    
    -- 예측 성능 지표
    accuracy DECIMAL(5,4),
    log_loss DECIMAL(6,6),
    brier_score DECIMAL(6,6),
    
    -- 수익성 지표
    total_bets INTEGER,
    win_count INTEGER,
    win_rate DECIMAL(5,4),
    total_profit DECIMAL(12,2),
    roi DECIMAL(6,2),
    sharpe_ratio DECIMAL(5,4),
    max_drawdown DECIMAL(6,2),
    
    evaluation_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(model_name, evaluation_period, evaluation_date)
);

COMMENT ON TABLE model_performances IS '모델 성능 지표';
COMMENT ON COLUMN model_performances.evaluation_period IS 'evaluation_period: 7일, 30일, 3개월 등';
COMMENT ON COLUMN model_performances.accuracy IS '예측 정확도 (승/패 맞춘 비율)';
COMMENT ON COLUMN model_performances.roi IS '투자 수익률 (%)';
COMMENT ON COLUMN model_performances.max_drawdown IS '최대 낙폭 (%)';

CREATE INDEX idx_model ON model_performances(model_name);
CREATE INDEX idx_evaluation_date ON model_performances(evaluation_date);

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
CREATE VIEW team_recent_performance AS
SELECT 
    t.id AS team_id,
    t.name AS team_name,
    COUNT(CASE WHEN m.home_team_id = t.id AND m.winner = 'home' THEN 1 END) +
    COUNT(CASE WHEN m.away_team_id = t.id AND m.winner = 'away' THEN 1 END) AS wins,
    COUNT(CASE WHEN m.home_team_id = t.id AND m.winner = 'away' THEN 1 END) +
    COUNT(CASE WHEN m.away_team_id = t.id AND m.winner = 'home' THEN 1 END) AS losses,
    COUNT(CASE WHEN m.home_team_id = t.id OR m.away_team_id = t.id THEN 1 END) AS total_games
FROM teams t
LEFT JOIN matches m ON (m.home_team_id = t.id OR m.away_team_id = t.id)
WHERE m.is_completed = TRUE
GROUP BY t.id, t.name;

-- 종료


