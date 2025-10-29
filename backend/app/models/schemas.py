"""
Pydantic 스키마 정의
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List


# ========================================
# 팀 관련 스키마
# ========================================

class Team(BaseModel):
    id: int
    name: str
    abbreviation: str
    stadium_name: Optional[str] = None


# ========================================
# 경기 관련 스키마
# ========================================

class Match(BaseModel):
    id: int
    home_team_id: int
    away_team_id: int
    home_team_name: str
    away_team_name: str
    match_date: date
    season: int
    stadium: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    winner: Optional[str] = None  # 'home' or 'away'
    is_completed: bool = False


class MatchList(BaseModel):
    matches: List[Match]
    total: int


# ========================================
# 예측 관련 스키마
# ========================================

class Prediction(BaseModel):
    id: int
    match_id: int
    model_name: str
    home_win_probability: float = Field(..., ge=0.0, le=1.0)
    away_win_probability: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    recommended_bet: Optional[str] = None  # 'home', 'away', 'pass'
    expected_value: Optional[float] = None
    predicted_at: datetime


class PredictionRequest(BaseModel):
    match_id: int
    model_name: str = "lstm_v1"


# ========================================
# 베팅 관련 스키마
# ========================================

class BettingHistory(BaseModel):
    id: int
    match_id: int
    match_date: date
    home_team: str
    away_team: str
    betting_model: str
    bet_on: str  # 'home' or 'away'
    betting_amount: float
    odds: float
    expected_profit: float
    actual_result: Optional[str] = None  # 'win' or 'loss'
    actual_profit: Optional[float] = None
    bet_placed_at: datetime
    is_recent: bool = False


class BettingResultList(BaseModel):
    results: List[BettingHistory]
    total: int


class BettingModelStats(BaseModel):
    name: str
    win_rate: float
    return_rate: float
    total_bets: int
    win_bets: int


# ========================================
# 성능 지표 관련 스키마
# ========================================

class ModelPerformance(BaseModel):
    model_name: str
    evaluation_period: str
    accuracy: float
    log_loss: float
    brier_score: float
    previous_accuracy: Optional[float] = None


class ProfitAnalysis(BaseModel):
    period_start: date
    period_end: date
    roi: float
    total_profit: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    previous_roi: Optional[float] = None


class ChartData(BaseModel):
    labels: List[str]
    data: List[float]


