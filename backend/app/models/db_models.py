"""
SQLAlchemy ORM 모델
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, DECIMAL, Text, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base


class Team(Base):
    """팀 정보 테이블"""
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, comment='팀명 (LG, 두산, 삼성 등)')
    abbreviation = Column(String(10), comment='팀 약칭')
    stadium_name = Column(String(100), comment='홈 구장 이름')
    founded_year = Column(Integer, comment='창단 연도')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    home_matches = relationship("Match", foreign_keys='Match.home_team_id', back_populates="home_team")
    away_matches = relationship("Match", foreign_keys='Match.away_team_id', back_populates="away_team")
    players = relationship("Player", back_populates="team")


class Match(Base):
    """경기 정보 테이블"""
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    home_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    match_date = Column(Date, nullable=False, comment='경기 날짜')
    season = Column(Integer, nullable=False, comment='연도')
    round = Column(Integer, comment='라운드 번호')
    match_number = Column(Integer, comment='경기 순번')
    stadium = Column(String(100), comment='경기장')
    
    # 경기 결과
    home_score = Column(Integer, comment='홈팀 점수')
    away_score = Column(Integer, comment='원정팀 점수')
    winner = Column(String(10), comment='winner: home/away')
    is_completed = Column(Boolean, default=False, comment='경기 종료 여부')
    
    # 추가 정보
    weather = Column(String(50), comment='날씨 정보')
    attendance = Column(Integer, comment='관중 수')
    innings = Column(Integer, comment='이닝 수')
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    odds = relationship("MatchOdds", back_populates="match")
    predictions = relationship("Prediction", back_populates="match")
    betting_histories = relationship("BettingHistory", back_populates="match")
    
    __table_args__ = (
        UniqueConstraint('season', 'round', 'match_number', name='unique_match'),
        Index('idx_match_date', 'match_date'),
        Index('idx_teams', 'home_team_id', 'away_team_id'),
    )


class Player(Base):
    """선수 정보 테이블 (선택적)"""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    name = Column(String(50), nullable=False, comment='선수 이름')
    position = Column(String(20), comment='포지션 (투수, 타자 등)')
    jersey_number = Column(Integer, comment='등번호')
    birth_date = Column(Date, comment='생년월일')
    height_cm = Column(Integer, comment='키')
    weight_kg = Column(Integer, comment='몸무게')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    team = relationship("Team", back_populates="players")
    
    __table_args__ = (
        Index('idx_team', 'team_id'),
    )


class MatchOdds(Base):
    """경기 배당률 테이블"""
    __tablename__ = "match_odds"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    odds_provider = Column(String(50), comment='배당 제공처 (sportstoto 등)')
    home_team_odds = Column(DECIMAL(5, 2), comment='홈팀 승률')
    away_team_odds = Column(DECIMAL(5, 2), comment='원정팀 승률')
    draw_odds = Column(DECIMAL(5, 2), comment='무승부 배당률')
    
    captured_at = Column(DateTime, comment='배당률 수집 시각')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 관계
    match = relationship("Match", back_populates="odds")
    
    __table_args__ = (
        UniqueConstraint('match_id', 'odds_provider', name='unique_odds'),
        Index('idx_match', 'match_id'),
        Index('idx_captured_at', 'captured_at'),
    )


class Prediction(Base):
    """AI 예측 결과 테이블"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    model_name = Column(String(50), nullable=False, comment='모델명 (lstm_v1, gru_v2 등)')
    
    # 예측 확률
    home_win_probability = Column(DECIMAL(5, 4), nullable=False, comment='홈팀 승률')
    away_win_probability = Column(DECIMAL(5, 4), nullable=False, comment='원정팀 승률')
    
    # 예측 정확도 지표
    confidence_score = Column(DECIMAL(5, 4), comment='모델 신뢰도')
    
    # 베팅 추천
    recommended_bet = Column(String(10), comment='recommend: home/away/pass')
    expected_value = Column(DECIMAL(8, 2), comment='기대값')
    kelly_percentage = Column(DECIMAL(5, 4), comment='켈리 포뮬러 추천 베팅 비율')
    
    predicted_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    
    # 관계
    match = relationship("Match", back_populates="predictions")
    betting_histories = relationship("BettingHistory", back_populates="prediction")
    
    __table_args__ = (
        UniqueConstraint('match_id', 'model_name', name='unique_prediction'),
        Index('idx_match', 'match_id'),
        Index('idx_model', 'model_name'),
        Index('idx_predicted_at', 'predicted_at'),
    )


class BettingHistory(Base):
    """베팅 시뮬레이션 내역 테이블"""
    __tablename__ = "betting_histories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    prediction_id = Column(Integer, ForeignKey('predictions.id'))
    
    # 베팅 정보
    betting_model = Column(String(50), nullable=False, comment='베팅 모델 (하이리턴, 스탠다드, 로우리스크)')
    bet_on = Column(String(10), nullable=False, comment='bet_on: home/away')
    betting_amount = Column(DECIMAL(12, 2), nullable=False, comment='베팅 금액')
    
    # 배당률
    odds = Column(DECIMAL(5, 2), comment='받을 배당률')
    expected_profit = Column(DECIMAL(12, 2), comment='예상 수익')
    
    # 실제 결과
    actual_result = Column(String(10), comment='actual_result: win/loss')
    actual_profit = Column(DECIMAL(12, 2), comment='실제 수익/손실')
    
    bet_placed_at = Column(DateTime, server_default=func.now())
    result_updated_at = Column(DateTime)
    
    # 관계
    match = relationship("Match", back_populates="betting_histories")
    prediction = relationship("Prediction", back_populates="betting_histories")
    
    __table_args__ = (
        Index('idx_match', 'match_id'),
        Index('idx_model', 'betting_model'),
        Index('idx_bet_placed_at', 'bet_placed_at'),
        Index('idx_result', 'actual_result'),
    )


class BettingModel(Base):
    """베팅 모델 설정 테이블"""
    __tablename__ = "betting_models"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, comment='모델명 (하이리턴, 스탠다드, 로우리스크)')
    description = Column(Text, comment='모델 설명')
    
    # 베팅 전략 파라미터
    min_confidence_threshold = Column(DECIMAL(5, 4), comment='최소 신뢰도 임계값')
    min_ev_threshold = Column(DECIMAL(8, 2), comment='최소 기대값 임계값')
    max_kelly_percentage = Column(DECIMAL(5, 4), comment='최대 켈리 비율')
    risk_multiplier = Column(DECIMAL(5, 4), comment='리스크 배수')
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ModelPerformance(Base):
    """모델 성능 지표 테이블"""
    __tablename__ = "model_performances"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(50), nullable=False, comment='모델명')
    evaluation_period = Column(String(20), comment='evaluation_period: 7일, 30일, 3개월 등')
    
    # 예측 성능 지표
    accuracy = Column(DECIMAL(5, 4), comment='예측 정확도')
    log_loss = Column(DECIMAL(6, 6), comment='Log Loss')
    brier_score = Column(DECIMAL(6, 6), comment='Brier Score')
    
    # 수익성 지표
    total_bets = Column(Integer, comment='총 베팅 횟수')
    win_count = Column(Integer, comment='승리 횟수')
    win_rate = Column(DECIMAL(5, 4), comment='승률')
    total_profit = Column(DECIMAL(12, 2), comment='총 수익')
    roi = Column(DECIMAL(6, 2), comment='투자 수익률 (%)')
    sharpe_ratio = Column(DECIMAL(5, 4), comment='샤프 비율')
    max_drawdown = Column(DECIMAL(6, 2), comment='최대 낙폭 (%)')
    
    evaluation_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('model_name', 'evaluation_period', 'evaluation_date', name='unique_performance'),
        Index('idx_model', 'model_name'),
        Index('idx_evaluation_date', 'evaluation_date'),
    )


