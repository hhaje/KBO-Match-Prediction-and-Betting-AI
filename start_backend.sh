#!/bin/bash

echo "===================================="
echo "KBO 베팅 AI 시스템 백엔드 서버 시작"
echo "===================================="

cd backend

# 가상환경 활성화 확인
if [ ! -d "venv" ]; then
    echo "가상환경을 찾을 수 없습니다. 먼저 설치를 진행합니다."
    echo ""
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "백엔드 서버를 시작합니다..."
echo "API 문서: http://localhost:8000/docs"
echo ""

python run.py


