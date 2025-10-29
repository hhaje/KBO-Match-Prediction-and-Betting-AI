"""
모의 데이터 생성
실제 DB 연결 전까지 사용
"""
from datetime import date, datetime, timedelta
import random
from typing import List, Dict


# ========================================
# KBO 팀 데이터
# ========================================

TEAMS = [
    {"id": 1, "name": "LG 트윈스", "abbreviation": "LG", "stadium_name": "잠실야구장"},
    {"id": 2, "name": "두산 베어스", "abbreviation": "두산", "stadium_name": "잠실야구장"},
    {"id": 3, "name": "삼성 라이온즈", "abbreviation": "삼성", "stadium_name": "대구삼성라이온즈파크"},
    {"id": 4, "name": "KIA 타이거즈", "abbreviation": "KIA", "stadium_name": "광주-기아 챔피언스 필드"},
    {"id": 5, "name": "NC 다이노스", "abbreviation": "NC", "stadium_name": "창원NC파크"},
    {"id": 6, "name": "KT 위즈", "abbreviation": "KT", "stadium_name": "수원KT위즈파크"},
    {"id": 7, "name": "SSG 랜더스", "abbreviation": "SSG", "stadium_name": "인천SSG랜더스필드"},
    {"id": 8, "name": "한화 이글스", "abbreviation": "한화", "stadium_name": "대전한화생명이글스파크"},
    {"id": 9, "name": "롯데 자이언츠", "abbreviation": "롯데", "stadium_name": "사직야구장"},
    {"id": 10, "name": "키움 히어로즈", "abbreviation": "키움", "stadium_name": "고척스카이돔"},
]


def get_team_by_id(team_id: int) -> Dict:
    """팀 ID로 팀 정보 조회"""
    return next((t for t in TEAMS if t["id"] == team_id), None)


def get_all_teams() -> List[Dict]:
    """모든 팀 정보 조회"""
    return TEAMS


# ========================================
# 경기 데이터 생성
# ========================================

def generate_matches(start_date: date, end_date: date, include_future: bool = True) -> List[Dict]:
    """
    지정된 기간의 경기 데이터 생성
    """
    matches = []
    match_id = 1
    current_date = start_date
    
    while current_date <= end_date:
        # 주말에는 더 많은 경기
        num_matches = random.randint(3, 5) if current_date.weekday() >= 5 else random.randint(2, 3)
        
        used_teams = set()
        for i in range(num_matches):
            # 겹치지 않는 팀 선택
            available_teams = [t for t in TEAMS if t["id"] not in used_teams]
            if len(available_teams) < 2:
                break
            
            home_team = random.choice(available_teams)
            used_teams.add(home_team["id"])
            available_teams = [t for t in available_teams if t["id"] != home_team["id"]]
            
            away_team = random.choice(available_teams)
            used_teams.add(away_team["id"])
            
            # 미래 경기는 결과 없음
            is_completed = current_date < date.today()
            
            if is_completed:
                home_score = random.randint(0, 12)
                away_score = random.randint(0, 12)
                winner = "home" if home_score > away_score else "away"
            else:
                home_score = None
                away_score = None
                winner = None
            
            match = {
                "id": match_id,
                "home_team_id": home_team["id"],
                "away_team_id": away_team["id"],
                "home_team_name": home_team["name"],
                "away_team_name": away_team["name"],
                "match_date": current_date,
                "season": current_date.year,
                "stadium": home_team["stadium_name"],
                "home_score": home_score,
                "away_score": away_score,
                "winner": winner,
                "is_completed": is_completed,
            }
            matches.append(match)
            match_id += 1
        
        current_date += timedelta(days=1)
    
    return matches


# ========================================
# 베팅 결과 데이터 생성
# ========================================

def generate_betting_results(num_results: int = 50) -> List[Dict]:
    """
    베팅 결과 데이터 생성
    """
    betting_models = ["하이리턴", "스탠다드", "로우리스크"]
    results = []
    
    for i in range(num_results):
        is_recent = i == 0  # 첫 번째만 최근 결과로 표시
        match_date = date.today() - timedelta(days=i)
        
        # 랜덤 팀 선택
        home_team = random.choice(TEAMS)
        away_team = random.choice([t for t in TEAMS if t["id"] != home_team["id"]])
        
        # 베팅 정보
        betting_model = random.choice(betting_models)
        bet_on = random.choice(["home", "away"])
        betting_amount = random.choice([30000, 50000, 75000, 100000, 120000, 150000, 200000])
        odds = round(random.uniform(1.5, 3.5), 2)
        
        # 승률에 따라 결과 결정 (약 65% 승률)
        is_win = random.random() < 0.65
        
        if is_win:
            actual_profit = betting_amount * (odds - 1)
            actual_result = "win"
        else:
            actual_profit = -betting_amount
            actual_result = "loss"
        
        result = {
            "id": i + 1,
            "match_id": i + 1,
            "match_date": match_date,
            "home_team": home_team["name"],
            "away_team": away_team["name"],
            "betting_model": betting_model,
            "bet_on": bet_on,
            "betting_amount": betting_amount,
            "odds": odds,
            "expected_profit": betting_amount * (odds - 1),
            "actual_result": actual_result,
            "actual_profit": actual_profit,
            "bet_placed_at": datetime.combine(match_date, datetime.min.time()),
            "is_recent": is_recent,
        }
        results.append(result)
    
    return results


# ========================================
# 모델 성능 데이터 생성
# ========================================

def generate_model_performance(model_name: str, period: str) -> Dict:
    """
    모델 성능 지표 생성
    """
    # 기간에 따라 성능 변화
    period_multiplier = {
        "7일": 1.05,
        "30일": 1.0,
        "3개월": 0.97,
        "6개월": 0.95,
        "1년": 0.92,
        "전체": 0.90,
    }
    
    multiplier = period_multiplier.get(period, 1.0)
    
    base_accuracy = 0.768
    accuracy = round(base_accuracy * multiplier, 3)
    previous_accuracy = round(accuracy * 0.965, 3)  # 이전 기간보다 약간 향상
    
    return {
        "model_name": model_name,
        "evaluation_period": period,
        "accuracy": accuracy,
        "log_loss": round(0.467 / multiplier, 3),
        "brier_score": round(0.241 / multiplier, 3),
        "previous_accuracy": previous_accuracy,
    }


# ========================================
# 수익 분석 데이터 생성
# ========================================

def generate_profit_analysis(start_date: date, end_date: date) -> Dict:
    """
    수익 분석 데이터 생성
    """
    days_diff = (end_date - start_date).days
    
    # 기간에 따라 스케일 조정
    roi_scale = 1 + (days_diff / 365) * 0.5
    profit_scale = 1 + (days_diff / 365) * 0.8
    
    roi = round(15.2 * roi_scale, 1)
    previous_roi = round(11.8 * roi_scale, 1)
    
    return {
        "period_start": start_date,
        "period_end": end_date,
        "roi": roi,
        "total_profit": int(3200000 * profit_scale),
        "sharpe_ratio": round(1.92 - (days_diff / 365) * 0.3, 2),
        "max_drawdown": round(-12.1 - (days_diff / 365) * 5, 1),
        "win_rate": round(71.2 - (days_diff / 365) * 3, 1),
        "previous_roi": previous_roi,
    }


# ========================================
# 차트 데이터 생성
# ========================================

def generate_chart_data(start_date: date, end_date: date) -> Dict:
    """
    ROI 추이 차트 데이터 생성 (베팅 수 기준)
    """
    days_diff = (end_date - start_date).days
    
    # 기간에 따른 총 베팅 수 추정 (하루 평균 2~3베팅)
    total_bets = int(days_diff * 2.5)
    
    # 차트 포인트 수 (최소 5개, 최대 10개)
    num_points = min(10, max(5, total_bets // 10))
    
    # 베팅 번호로 레이블 생성
    bet_interval = max(1, total_bets // num_points)
    labels = [f"베팅 {(i+1) * bet_interval}" for i in range(num_points)]
    
    # 기본 데이터에 추세 적용
    base_data = [3.2, 7.8, 12.1, 15.2, 18.5, 21.2, 24.8, 26.5, 28.1, 29.5]
    data = [round(val * (1 + days_diff / 365), 1) for val in base_data[:num_points]]
    
    return {
        "labels": labels,
        "data": data,
    }


# ========================================
# 베팅 모델 통계 생성
# ========================================

def generate_betting_model_stats(model_name: str) -> Dict:
    """
    베팅 모델별 통계 생성
    """
    model_stats = {
        "하이리턴": {
            "name": "하이리턴",
            "win_rate": 75,
            "return_rate": 12.5,
            "total_bets": 45,
            "win_bets": 34,
        },
        "스탠다드": {
            "name": "스탠다드",
            "win_rate": 68,
            "return_rate": 8.2,
            "total_bets": 52,
            "win_bets": 35,
        },
        "로우리스크": {
            "name": "로우리스크",
            "win_rate": 82,
            "return_rate": 5.8,
            "total_bets": 38,
            "win_bets": 31,
        },
    }
    
    return model_stats.get(model_name, model_stats["스탠다드"])


# ========================================
# 예측 데이터 생성
# ========================================

def generate_prediction(match_id: int, model_name: str) -> Dict:
    """
    경기 예측 데이터 생성
    """
    # 홈팀 승률 (0.4 ~ 0.7 사이)
    home_win_prob = round(random.uniform(0.4, 0.7), 4)
    away_win_prob = round(1 - home_win_prob, 4)
    
    # 신뢰도 (0.6 ~ 0.9 사이)
    confidence = round(random.uniform(0.6, 0.9), 4)
    
    # 베팅 추천 결정
    if home_win_prob > 0.6 and confidence > 0.7:
        recommended_bet = "home"
    elif away_win_prob > 0.6 and confidence > 0.7:
        recommended_bet = "away"
    else:
        recommended_bet = "pass"
    
    # 기대값 계산 (임의)
    expected_value = round(random.uniform(-500, 2000), 2) if recommended_bet != "pass" else 0
    
    return {
        "id": match_id,
        "match_id": match_id,
        "model_name": model_name,
        "home_win_probability": home_win_prob,
        "away_win_probability": away_win_prob,
        "confidence_score": confidence,
        "recommended_bet": recommended_bet,
        "expected_value": expected_value,
        "predicted_at": datetime.now(),
    }


