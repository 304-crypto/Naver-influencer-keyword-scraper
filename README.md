# 네이버 인플루언서 키워드 수집 프로그램

네이버 인플루언서 플랫폼에서 카테고리별 키워드 데이터를 수집하는 도구입니다.

## 📋 주요 기능

- **CLI 모드**: 대화형 인터페이스로 키워드 수집 및 파일 저장
- **REST API**: FastAPI 기반 웹 API로 프론트엔드 연동 가능
- **다양한 포맷**: TXT, TSV, CSV 형식 지원
- **안정적인 동작**: 네트워크 오류 및 입력 검증 처리

## 🚀 설치 방법

```bash
# 의존성 설치
pip install -r requirements.txt
```

## 💻 사용 방법

### 1. CLI 모드 (기본)

```bash
python main.py
```

- 카테고리 목록에서 원하는 카테고리 선택
- 자동으로 키워드 수집 및 파일 저장 (`.txt` 형식)
- 저장 파일: `{카테고리명}.txt` (키워드명만 포함)

### 2. FastAPI 서버 실행

```bash
uvicorn backend.app:app --reload --port 8000
```

서버 실행 후 브라우저에서 `http://localhost:8000` 접속

#### API 문서

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API 엔드포인트

### `GET /api/categories`

카테고리 목록 조회

**응답 예시:**
```json
[
  {
    "id": "123",
    "name": "뷰티",
    "keywordCount": 150
  }
]
```

### `GET /api/keywords`

키워드 조회 (JSON)

**파라미터:**
- `categoryId` (필수): 카테고리 ID
- `sleepSec` (선택, 기본값: 2.0): 요청 간 대기 시간 (0~10초)

**응답 예시:**
```json
{
  "recomm": [
    {"name": "추천키워드1", "participantCount": 500}
  ],
  "normal": [
    {"name": "일반키워드1", "participantCount": 300}
  ]
}
```

### `GET /api/keywords.txt`

키워드 조회 (텍스트)

**파라미터:**
- `categoryId` (필수): 카테고리 ID
- `format` (선택, 기본값: txt): 출력 포맷 (`txt` | `tsv` | `csv`)
- `includeRecomm` (선택, 기본값: 0): 추천 키워드 포함 여부 (`0` | `1`)

**포맷별 출력:**
- `txt`: 키워드명만 (한 줄에 하나씩)
- `tsv`: 키워드명\t참여자수
- `csv`: CSV 형식 (헤더 포함)

**사용 예시:**
```bash
# 키워드명만 (txt)
curl "http://localhost:8000/api/keywords.txt?categoryId=123&format=txt"

# 키워드 + 참여자수 (tsv)
curl "http://localhost:8000/api/keywords.txt?categoryId=123&format=tsv"

# 추천 키워드 포함 (csv)
curl "http://localhost:8000/api/keywords.txt?categoryId=123&format=csv&includeRecomm=1"
```

## 🏗️ 프로젝트 구조

```
naver_infl/
├── main.py                 # CLI 스크립트
├── backend/
│   ├── __init__.py
│   ├── app.py             # FastAPI 애플리케이션
│   ├── scraper.py         # 스크래핑 로직
│   ├── config.py          # 설정 상수
│   └── utils.py           # 유틸리티 함수
├── requirements.txt
└── README.md
```

## ⚠️ 주의사항

- **개인용 로컬 실행 전용**: 이 도구는 개인적인 연구 및 분석 목적으로만 사용하세요
- **Rate Limiting**: 네이버 서버 부하 방지를 위해 요청 간 대기 시간이 설정되어 있습니다
- **CORS 설정**: 현재 모든 origin 허용 (`allow_origins=["*"]`), 프로덕션 환경에서는 제한 필요

## 🔧 설정 변경

`backend/config.py`에서 다음 값들을 조정할 수 있습니다:

- `DEFAULT_SLEEP_SEC_CLI`: CLI 기본 대기 시간 (기본값: 3초)
- `DEFAULT_SLEEP_SEC_API`: API 기본 대기 시간 (기본값: 2초)
- `DEFAULT_LIMIT`: 페이지당 조회 개수 (기본값: 20)
- `RECOMMEND_LIMIT`: 추천 키워드 개수 (기본값: 3)

## 📝 라이선스

개인 사용 목적으로만 제공됩니다.
