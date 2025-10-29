# MySQL 데이터베이스 설정 가이드

## 📋 목차

1. [MySQL 설치](#1-mysql-설치)
2. [데이터베이스 생성](#2-데이터베이스-생성)
3. [환경 변수 설정](#3-환경-변수-설정)
4. [Python 패키지 설치](#4-python-패키지-설치)
5. [스키마 생성](#5-스키마-생성)
6. [연결 테스트](#6-연결-테스트)
7. [트러블슈팅](#7-트러블슈팅)

---

## 1. MySQL 설치

### Windows

**방법 1: MySQL Installer 사용 (추천)**

1. [MySQL 공식 다운로드 페이지](https://dev.mysql.com/downloads/installer/) 접속
2. `mysql-installer-community-8.x.x.msi` 다운로드
3. 설치 프로그램 실행
4. **Developer Default** 선택
5. 루트 비밀번호 설정 (예: `root123`)
6. MySQL Server 서비스 시작

**방법 2: Chocolatey 사용**

```powershell
choco install mysql
```

### macOS

```bash
# Homebrew 사용
brew install mysql

# MySQL 서비스 시작
brew services start mysql

# 초기 보안 설정
mysql_secure_installation
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install mysql-server

# MySQL 서비스 시작
sudo systemctl start mysql
sudo systemctl enable mysql

# 초기 보안 설정
sudo mysql_secure_installation
```

---

## 2. 데이터베이스 생성

### 방법 1: MySQL CLI 사용

```bash
# MySQL 접속
mysql -u root -p

# 비밀번호 입력 후...
```

```sql
-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS kbo_betting_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 사용자 생성 (선택적)
CREATE USER 'kbo_user'@'localhost' IDENTIFIED BY 'kbo_password';

-- 권한 부여
GRANT ALL PRIVILEGES ON kbo_betting_db.* TO 'kbo_user'@'localhost';
FLUSH PRIVILEGES;

-- 확인
SHOW DATABASES;

-- 종료
EXIT;
```

### 방법 2: SQL 스크립트 실행

```bash
# 프로젝트 루트 디렉토리에서
mysql -u root -p < docs/database_schema_mysql.sql
```

---

## 3. 환경 변수 설정

### backend 폴더에 `.env` 파일 생성

**파일 위치:** `backend/.env`

```env
# 데이터베이스 설정
DB_HOST=localhost
DB_PORT=3306
DB_NAME=kbo_betting_db
DB_USER=root
DB_PASSWORD=root123

# API 설정
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# 보안
SECRET_KEY=your-secret-key-change-this-in-production

# CORS 설정
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**⚠️ 주의사항:**
- `.env` 파일은 **절대 Git에 커밋하지 마세요**
- 프로덕션에서는 강력한 비밀번호 사용
- `SECRET_KEY`는 랜덤 문자열로 변경

---

## 4. Python 패키지 설치

```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# 가상 환경 활성화 (macOS/Linux)
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

**설치되는 주요 패키지:**
- `sqlalchemy==2.0.23` - ORM
- `pymysql==1.1.0` - MySQL 드라이버
- `cryptography==41.0.7` - 암호화
- `python-dotenv==1.0.0` - 환경 변수

---

## 5. 스키마 생성

### 방법 1: SQL 스크립트 직접 실행 (추천)

```bash
# MySQL에 접속하여 실행
mysql -u root -p kbo_betting_db < docs/database_schema_mysql.sql
```

### 방법 2: Python ORM으로 생성

```python
# backend 디렉토리에서 Python 실행
python

>>> from app.database import init_db, check_db_connection
>>> check_db_connection()  # 연결 확인
>>> init_db()  # 테이블 생성
```

### 방법 3: 초기화 스크립트 작성

**파일:** `backend/init_db.py`

```python
"""
데이터베이스 초기화 스크립트
"""
from app.database import init_db, check_db_connection

if __name__ == "__main__":
    print("🔍 데이터베이스 연결 확인 중...")
    if check_db_connection():
        print("🚀 테이블 생성 중...")
        init_db()
        print("✅ 데이터베이스 초기화 완료!")
    else:
        print("❌ 데이터베이스 연결 실패. .env 파일을 확인하세요.")
```

**실행:**

```bash
cd backend
python init_db.py
```

---

## 6. 연결 테스트

### 테스트 1: MySQL CLI로 확인

```bash
mysql -u root -p kbo_betting_db
```

```sql
-- 테이블 목록 확인
SHOW TABLES;

-- 팀 데이터 확인
SELECT * FROM teams;

-- 테이블 구조 확인
DESCRIBE matches;
```

### 테스트 2: Python으로 확인

```python
from app.database import SessionLocal
from app.models.db_models import Team

# 세션 생성
db = SessionLocal()

# 팀 목록 조회
teams = db.query(Team).all()
for team in teams:
    print(f"{team.name} ({team.abbreviation})")

db.close()
```

### 테스트 3: API 엔드포인트 확인

```bash
# 백엔드 서버 시작
cd backend
python run.py

# 브라우저에서 확인
# http://localhost:8000/docs
```

---

## 7. 트러블슈팅

### 문제 1: MySQL 서비스가 시작되지 않음

**Windows:**

```powershell
# 서비스 시작
net start MySQL80

# 또는 서비스 관리자에서 수동 시작
services.msc
```

**macOS/Linux:**

```bash
# 상태 확인
sudo systemctl status mysql

# 재시작
sudo systemctl restart mysql
```

---

### 문제 2: "Access denied for user" 오류

```sql
-- MySQL에 root로 접속
mysql -u root -p

-- 비밀번호 재설정
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

---

### 문제 3: pymysql 연결 오류

**오류 메시지:**
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
```

**해결 방법:**

1. `.env` 파일 확인
2. MySQL 서비스 실행 여부 확인
3. 방화벽 설정 확인
4. 호스트/포트 확인

```python
# 직접 연결 테스트
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root123',
    database='kbo_betting_db',
    charset='utf8mb4'
)
print("✅ 연결 성공!")
connection.close()
```

---

### 문제 4: 테이블이 생성되지 않음

```sql
-- MySQL CLI에서 확인
USE kbo_betting_db;
SHOW TABLES;

-- 테이블이 없으면 SQL 스크립트 재실행
SOURCE /path/to/database_schema_mysql.sql;
```

---

### 문제 5: 인코딩 오류 (한글 깨짐)

```sql
-- 데이터베이스 문자셋 확인
SHOW CREATE DATABASE kbo_betting_db;

-- 문자셋 변경
ALTER DATABASE kbo_betting_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

---

## 📊 초기 데이터 확인

스키마가 정상적으로 생성되면 다음 데이터가 있어야 합니다:

### 팀 정보 (10개)

```sql
SELECT id, name, abbreviation FROM teams;
```

| id | name | abbreviation |
|----|------|--------------|
| 1 | LG 트윈스 | LG |
| 2 | 두산 베어스 | 두산 |
| 3 | 삼성 라이온즈 | 삼성 |
| 4 | KIA 타이거즈 | KIA |
| 5 | NC 다이노스 | NC |
| 6 | KT 위즈 | KT |
| 7 | SSG 랜더스 | SSG |
| 8 | 한화 이글스 | 한화 |
| 9 | 롯데 자이언츠 | 롯데 |
| 10 | 키움 히어로즈 | 키움 |

### 베팅 모델 (3개)

```sql
SELECT name, description FROM betting_models;
```

| name | description |
|------|-------------|
| 하이리턴 | 고수익 고위험 전략 |
| 스탠다드 | 균형잡힌 전략 |
| 로우리스크 | 안정성 우선 전략 |

---

## 🎯 다음 단계

1. ✅ **백엔드 서비스 레이어 수정** - mock_data → DB 쿼리로 변경
2. ✅ **KBO 데이터 수집** - 실제 경기 데이터 크롤링
3. ✅ **API 테스트** - 실제 DB 데이터로 동작 확인

---

## 📚 참고 자료

- [MySQL 공식 문서](https://dev.mysql.com/doc/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [PyMySQL 문서](https://pymysql.readthedocs.io/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)


