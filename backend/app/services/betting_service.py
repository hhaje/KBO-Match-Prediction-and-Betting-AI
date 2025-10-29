"""
베팅 관련 비즈니스 로직
"""
from datetime import date, timedelta
from typing import List, Optional
from ..data import mock_data


class BettingService:
    """베팅 서비스"""
    
    def get_betting_results(
        self, 
        betting_model: Optional[str] = None,
        period: Optional[str] = None,
        limit: int = 50
    ) -> List[dict]:
        """
        베팅 결과 조회
        
        Args:
            betting_model: 베팅 모델명 (하이리턴, 스탠다드, 로우리스크)
            period: 기간 (7일, 30일, 전체 등)
            limit: 최대 결과 수
        """
        results = mock_data.generate_betting_results(num_results=limit)
        
        # 베팅 모델 필터링
        if betting_model:
            results = [r for r in results if r["betting_model"] == betting_model]
        
        # 기간 필터링
        if period and period != "전체":
            days_map = {
                "7일": 7,
                "30일": 30,
                "3개월": 90,
                "6개월": 180,
                "1년": 365,
            }
            days = days_map.get(period, 30)
            cutoff_date = date.today() - timedelta(days=days)
            results = [r for r in results if r["match_date"] >= cutoff_date]
        
        return results
    
    def get_betting_model_stats(self, model_name: str) -> dict:
        """
        베팅 모델 통계 조회
        """
        return mock_data.generate_betting_model_stats(model_name)
    
    def get_all_betting_models_stats(self) -> List[dict]:
        """
        모든 베팅 모델 통계 조회
        """
        models = ["하이리턴", "스탠다드", "로우리스크"]
        stats = []
        
        for model in models:
            stat = self.get_betting_model_stats(model)
            stats.append(stat)
        
        return stats
    
    def calculate_betting_recommendation(
        self,
        prediction: dict,
        odds: float,
        betting_model: str = "스탠다드"
    ) -> dict:
        """
        베팅 추천 계산
        
        Args:
            prediction: 예측 결과
            odds: 배당률
            betting_model: 베팅 모델
        
        Returns:
            베팅 추천 정보
        """
        # 베팅 모델별 임계값
        thresholds = {
            "하이리턴": {"min_confidence": 0.55, "min_ev": 1000},
            "스탠다드": {"min_confidence": 0.60, "min_ev": 500},
            "로우리스크": {"min_confidence": 0.70, "min_ev": 300},
        }
        
        threshold = thresholds.get(betting_model, thresholds["스탠다드"])
        
        # 기대값 계산
        home_win_prob = prediction["home_win_probability"]
        expected_value = (home_win_prob * odds * 10000) - 10000
        
        # 베팅 추천 결정
        should_bet = (
            prediction["confidence_score"] >= threshold["min_confidence"] and
            expected_value >= threshold["min_ev"]
        )
        
        return {
            "should_bet": should_bet,
            "expected_value": expected_value,
            "recommended_amount": 10000 if should_bet else 0,
            "confidence": prediction["confidence_score"],
        }


