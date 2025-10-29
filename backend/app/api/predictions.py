"""
예측 관련 API 엔드포인트
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List

from ..models.schemas import Prediction, PredictionRequest
from ..services.prediction_service import PredictionService

router = APIRouter()
prediction_service = PredictionService()


@router.post("/generate", response_model=Prediction)
async def generate_prediction(request: PredictionRequest):
    """
    경기 예측 생성
    """
    try:
        prediction = prediction_service.generate_prediction(
            request.match_id,
            request.model_name
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{match_id}", response_model=Prediction)
async def get_prediction(
    match_id: int,
    model_name: str = Query("lstm_v1", description="모델명")
):
    """
    경기 예측 조회
    """
    prediction = prediction_service.get_prediction(match_id, model_name)
    
    if not prediction:
        raise HTTPException(status_code=404, detail="예측 결과를 찾을 수 없습니다")
    
    return prediction


@router.get("/{match_id}/all", response_model=List[Prediction])
async def get_all_predictions(match_id: int):
    """
    경기의 모든 모델 예측 조회
    """
    predictions = prediction_service.get_predictions_by_match(match_id)
    return predictions


