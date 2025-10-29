"""
성능 분석 관련 API 엔드포인트
"""
from fastapi import APIRouter, Query
from datetime import date
from typing import Optional, List

from ..models.schemas import ModelPerformance, ProfitAnalysis, ChartData
from ..services.performance_service import PerformanceService

router = APIRouter()
performance_service = PerformanceService()


@router.get("/model", response_model=ModelPerformance)
async def get_model_performance(
    model_name: str = Query("lstm_v1", description="모델명"),
    period: str = Query("30일", description="평가 기간 (7일, 30일, 3개월, 6개월, 1년, 전체)")
):
    """
    모델 성능 지표 조회
    """
    performance = performance_service.get_model_performance(model_name, period)
    return performance


@router.get("/model/compare", response_model=List[ModelPerformance])
async def compare_models(
    period: str = Query("30일", description="평가 기간")
):
    """
    모델 성능 비교
    """
    performances = performance_service.compare_models(period)
    return performances


@router.get("/profit", response_model=ProfitAnalysis)
async def get_profit_analysis(
    start_date: Optional[date] = Query(None, description="시작 날짜"),
    end_date: Optional[date] = Query(None, description="종료 날짜")
):
    """
    수익 분석 데이터 조회
    """
    analysis = performance_service.get_profit_analysis(start_date, end_date)
    return analysis


@router.get("/chart", response_model=ChartData)
async def get_chart_data(
    start_date: Optional[date] = Query(None, description="시작 날짜"),
    end_date: Optional[date] = Query(None, description="종료 날짜")
):
    """
    ROI 추이 차트 데이터 조회
    """
    chart_data = performance_service.get_chart_data(start_date, end_date)
    return chart_data


