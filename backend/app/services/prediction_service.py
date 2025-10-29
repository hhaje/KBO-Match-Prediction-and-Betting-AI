"""
예측 관련 비즈니스 로직
"""
from typing import Optional
from ..data import mock_data


class PredictionService:
    """예측 서비스"""
    
    def generate_prediction(self, match_id: int, model_name: str = "lstm_v1") -> dict:
        """
        경기 예측 생성
        
        실제 구현 시:
        1. match_id로 경기 데이터 조회
        2. 팀별 최근 성적, 특성 추출
        3. ML 모델 로드
        4. 예측 실행
        5. 결과 DB 저장
        6. 결과 반환
        """
        # 현재는 모의 데이터 반환
        prediction = mock_data.generate_prediction(match_id, model_name)
        return prediction
    
    def get_prediction(
        self, 
        match_id: int, 
        model_name: str = "lstm_v1"
    ) -> Optional[dict]:
        """
        저장된 예측 조회
        
        실제 구현 시: DB에서 조회
        """
        # 현재는 새로 생성
        return self.generate_prediction(match_id, model_name)
    
    def get_predictions_by_match(self, match_id: int) -> list:
        """
        경기의 모든 모델 예측 조회
        """
        models = ["lstm_v1", "gru_v1", "ensemble_v1"]
        predictions = []
        
        for model_name in models:
            pred = self.generate_prediction(match_id, model_name)
            predictions.append(pred)
        
        return predictions


