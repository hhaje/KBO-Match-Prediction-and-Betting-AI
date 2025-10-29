"""
경기 관련 비즈니스 로직
"""
from datetime import date, timedelta
from typing import List, Optional
from ..data import mock_data


class MatchService:
    """경기 서비스"""
    
    def get_matches_by_date_range(
        self, 
        start_date: Optional[date] = None, 
        end_date: Optional[date] = None
    ) -> List[dict]:
        """
        날짜 범위로 경기 조회
        """
        if start_date is None:
            start_date = date.today() - timedelta(days=7)
        if end_date is None:
            end_date = date.today() + timedelta(days=7)
        
        matches = mock_data.generate_matches(start_date, end_date)
        return matches
    
    def get_match_by_id(self, match_id: int) -> Optional[dict]:
        """
        경기 ID로 조회
        """
        # 간단한 구현 - 실제로는 DB에서 조회
        matches = self.get_matches_by_date_range(
            date.today() - timedelta(days=30),
            date.today() + timedelta(days=30)
        )
        
        for match in matches:
            if match["id"] == match_id:
                return match
        
        return None
    
    def get_upcoming_matches(self, limit: int = 10) -> List[dict]:
        """
        예정된 경기 조회
        """
        matches = self.get_matches_by_date_range(
            date.today(),
            date.today() + timedelta(days=14)
        )
        
        # 완료되지 않은 경기만 필터링
        upcoming = [m for m in matches if not m["is_completed"]]
        return upcoming[:limit]
    
    def get_recent_matches(self, limit: int = 10) -> List[dict]:
        """
        최근 경기 결과 조회
        """
        matches = self.get_matches_by_date_range(
            date.today() - timedelta(days=14),
            date.today()
        )
        
        # 완료된 경기만 필터링
        recent = [m for m in matches if m["is_completed"]]
        recent.sort(key=lambda x: x["match_date"], reverse=True)
        return recent[:limit]


