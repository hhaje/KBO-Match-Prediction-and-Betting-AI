"""
성능 분석 관련 비즈니스 로직
"""
from datetime import date, timedelta
from typing import Optional
from ..data import mock_data


class PerformanceService:
    """성능 분석 서비스"""
    
    def get_model_performance(
        self, 
        model_name: str = "lstm_v1",
        period: str = "30일"
    ) -> dict:
        """
        모델 성능 지표 조회
        
        Args:
            model_name: 모델명
            period: 평가 기간 (7일, 30일, 3개월, 6개월, 1년, 전체)
        """
        return mock_data.generate_model_performance(model_name, period)
    
    def get_profit_analysis(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """
        수익 분석 데이터 조회
        
        Args:
            start_date: 시작 날짜
            end_date: 종료 날짜
        """
        if end_date is None:
            end_date = date.today()
        
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        return mock_data.generate_profit_analysis(start_date, end_date)
    
    def get_chart_data(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """
        ROI 추이 차트 데이터 조회
        """
        if end_date is None:
            end_date = date.today()
        
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        return mock_data.generate_chart_data(start_date, end_date)
    
    def compare_models(self, period: str = "30일") -> list:
        """
        모델 성능 비교
        """
        models = ["lstm_v1", "gru_v1", "ensemble_v1"]
        performances = []
        
        for model_name in models:
            perf = self.get_model_performance(model_name, period)
            performances.append(perf)
        
        # 정확도 순으로 정렬
        performances.sort(key=lambda x: x["accuracy"], reverse=True)
        
        return performances


