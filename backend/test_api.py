"""
백엔드 API 간단 테스트 스크립트
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"


def test_health():
    """헬스 체크 테스트"""
    print("\n[테스트 1] 헬스 체크...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"상태 코드: {response.status_code}")
    print(f"응답: {response.json()}")
    assert response.status_code == 200


def test_get_matches():
    """경기 목록 조회 테스트"""
    print("\n[테스트 2] 경기 목록 조회...")
    today = date.today()
    start_date = (today - timedelta(days=7)).isoformat()
    end_date = (today + timedelta(days=7)).isoformat()
    
    response = requests.get(
        f"{BASE_URL}/api/matches/",
        params={"start_date": start_date, "end_date": end_date}
    )
    print(f"상태 코드: {response.status_code}")
    data = response.json()
    print(f"총 경기 수: {data['total']}")
    if data['matches']:
        print(f"첫 번째 경기: {data['matches'][0]}")
    assert response.status_code == 200


def test_get_prediction():
    """예측 조회 테스트"""
    print("\n[테스트 3] 예측 조회...")
    match_id = 1
    
    response = requests.get(
        f"{BASE_URL}/api/predictions/{match_id}",
        params={"model_name": "lstm_v1"}
    )
    print(f"상태 코드: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"홈팀 승률: {data['home_win_probability']}")
        print(f"원정팀 승률: {data['away_win_probability']}")
        print(f"신뢰도: {data['confidence_score']}")


def test_get_betting_results():
    """베팅 결과 조회 테스트"""
    print("\n[테스트 4] 베팅 결과 조회...")
    
    response = requests.get(
        f"{BASE_URL}/api/betting/results",
        params={"model": "하이리턴", "limit": 10}
    )
    print(f"상태 코드: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"총 결과 수: {data['total']}")
        if data['results']:
            print(f"첫 번째 결과: {data['results'][0]}")


def test_get_model_performance():
    """모델 성능 조회 테스트"""
    print("\n[테스트 5] 모델 성능 조회...")
    
    response = requests.get(
        f"{BASE_URL}/api/performance/model",
        params={"model_name": "lstm_v1", "period": "30일"}
    )
    print(f"상태 코드: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"정확도: {data['accuracy']}")
        print(f"Log Loss: {data['log_loss']}")
        print(f"Brier Score: {data['brier_score']}")


def test_get_profit_analysis():
    """수익 분석 조회 테스트"""
    print("\n[테스트 6] 수익 분석 조회...")
    
    today = date.today()
    start_date = (today - timedelta(days=30)).isoformat()
    end_date = today.isoformat()
    
    response = requests.get(
        f"{BASE_URL}/api/performance/profit",
        params={"start_date": start_date, "end_date": end_date}
    )
    print(f"상태 코드: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"ROI: {data['roi']}%")
        print(f"총 수익: {data['total_profit']:,}원")
        print(f"샤프 비율: {data['sharpe_ratio']}")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 50)
    print("KBO 베팅 AI 시스템 API 테스트")
    print("=" * 50)
    
    try:
        test_health()
        test_get_matches()
        test_get_prediction()
        test_get_betting_results()
        test_get_model_performance()
        test_get_profit_analysis()
        
        print("\n" + "=" * 50)
        print("✅ 모든 테스트 통과!")
        print("=" * 50)
        
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"❌ 테스트 실패: {e}")
        print("=" * 50)


if __name__ == "__main__":
    run_all_tests()


