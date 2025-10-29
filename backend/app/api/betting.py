"""
베팅 관련 API 엔드포인트
"""
from fastapi import APIRouter, Query
from typing import Optional, List

from ..models.schemas import BettingHistory, BettingResultList, BettingModelStats
from ..services.betting_service import BettingService

router = APIRouter()
betting_service = BettingService()


@router.get("/results", response_model=BettingResultList)
async def get_betting_results(
    model: Optional[str] = Query(None, description="베팅 모델 (하이리턴, 스탠다드, 로우리스크)"),
    period: Optional[str] = Query(None, description="기간 (7일, 30일, 3개월, 6개월, 1년, 전체)"),
    limit: int = Query(50, ge=1, le=100, description="조회할 결과 수")
):
    """
    베팅 결과 조회
    """
    results = betting_service.get_betting_results(
        betting_model=model,
        period=period,
        limit=limit
    )
    
    return {
        "results": results,
        "total": len(results)
    }


@router.get("/models/stats", response_model=List[BettingModelStats])
async def get_all_betting_models_stats():
    """
    모든 베팅 모델 통계 조회
    """
    stats = betting_service.get_all_betting_models_stats()
    return stats


@router.get("/models/{model_name}/stats", response_model=BettingModelStats)
async def get_betting_model_stats(model_name: str):
    """
    특정 베팅 모델 통계 조회
    """
    stats = betting_service.get_betting_model_stats(model_name)
    return stats


@router.post("/recommend")
async def get_betting_recommendation(
    prediction: dict,
    odds: float = Query(..., gt=1.0, description="배당률"),
    betting_model: str = Query("스탠다드", description="베팅 모델")
):
    """
    베팅 추천 계산
    """
    recommendation = betting_service.calculate_betting_recommendation(
        prediction=prediction,
        odds=odds,
        betting_model=betting_model
    )
    return recommendation


