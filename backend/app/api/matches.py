"""
경기 관련 API 엔드포인트
"""
from fastapi import APIRouter, Query, HTTPException
from datetime import date
from typing import Optional

from ..models.schemas import Match, MatchList
from ..services.match_service import MatchService

router = APIRouter()
match_service = MatchService()


@router.get("/", response_model=MatchList)
async def get_matches(
    start_date: Optional[date] = Query(None, description="시작 날짜"),
    end_date: Optional[date] = Query(None, description="종료 날짜"),
):
    """
    경기 목록 조회
    """
    matches = match_service.get_matches_by_date_range(start_date, end_date)
    
    return {
        "matches": matches,
        "total": len(matches)
    }


@router.get("/upcoming", response_model=MatchList)
async def get_upcoming_matches(
    limit: int = Query(10, ge=1, le=50, description="조회할 경기 수")
):
    """
    예정된 경기 조회
    """
    matches = match_service.get_upcoming_matches(limit=limit)
    
    return {
        "matches": matches,
        "total": len(matches)
    }


@router.get("/recent", response_model=MatchList)
async def get_recent_matches(
    limit: int = Query(10, ge=1, le=50, description="조회할 경기 수")
):
    """
    최근 경기 결과 조회
    """
    matches = match_service.get_recent_matches(limit=limit)
    
    return {
        "matches": matches,
        "total": len(matches)
    }


@router.get("/{match_id}", response_model=Match)
async def get_match(match_id: int):
    """
    특정 경기 조회
    """
    match = match_service.get_match_by_id(match_id)
    
    if not match:
        raise HTTPException(status_code=404, detail="경기를 찾을 수 없습니다")
    
    return match


