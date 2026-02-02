"""
FastAPI 애플리케이션

네이버 인플루언서 키워드 수집 REST API를 제공합니다.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from typing import Literal

from .scraper import fetch_categories, get_all_keywords
from .utils import format_keywords_txt, format_keywords_tsv, format_keywords_csv
from .config import MIN_SLEEP_SEC, MAX_SLEEP_SEC, DEFAULT_SLEEP_SEC_API

app = FastAPI(
    title="Naver Influencer Keyword API",
    description="네이버 인플루언서 키워드 수집 API (개인용 로컬 실행)",
    version="1.0.0"
)

# CORS 설정 (로컬 프론트엔드 호출 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용, 프로덕션에서는 제한 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "Naver Influencer Keyword API",
        "version": "1.0.0",
        "endpoints": {
            "categories": "/api/categories",
            "keywords_json": "/api/keywords?categoryId={id}&sleepSec={sec}",
            "keywords_text": "/api/keywords.txt?categoryId={id}&format={txt|tsv|csv}&includeRecomm={0|1}"
        }
    }


@app.get("/api/categories")
async def get_categories():
    """
    카테고리 목록 조회
    
    Returns:
        [{'id': ..., 'name': ..., 'keywordCount': ...}, ...]
    """
    try:
        categories = fetch_categories()
        return categories
    except ValueError as e:
        # 파싱 오류 등 (네이버 응답 구조 변경)
        raise HTTPException(status_code=502, detail=f"네이버 응답 처리 실패: {str(e)}")
    except Exception as e:
        # 네트워크 오류 등
        raise HTTPException(status_code=502, detail=f"카테고리 조회 실패: {str(e)}")


@app.get("/api/keywords")
async def get_keywords(
    categoryId: str = Query(..., description="카테고리 ID"),
    sleepSec: float = Query(
        DEFAULT_SLEEP_SEC_API, 
        ge=MIN_SLEEP_SEC, 
        le=MAX_SLEEP_SEC, 
        description="요청 간 대기 시간 (초)"
    )
):
    """
    키워드 조회 (JSON 응답)
    
    Args:
        categoryId: 카테고리 ID
        sleepSec: 요청 간 대기 시간 (0~10초)
        
    Returns:
        {'recomm': [{'name': ..., 'participantCount': ...}], 'normal': [...]}
    """
    try:
        keywords = get_all_keywords(categoryId, sleepSec)
        return keywords
    except ValueError as e:
        # GraphQL 오류 (errors 키 존재 또는 data 없음)
        raise HTTPException(status_code=502, detail=f"네이버 응답 오류: {str(e)}")
    except Exception as e:
        # 네트워크 오류 등
        raise HTTPException(status_code=502, detail=f"키워드 조회 실패: {str(e)}")


@app.get("/api/keywords.txt", response_class=PlainTextResponse)
async def get_keywords_text(
    categoryId: str = Query(..., description="카테고리 ID"),
    format: Literal["txt", "tsv", "csv"] = Query("txt", description="출력 포맷"),
    includeRecomm: Literal[0, 1] = Query(0, description="추천 키워드 포함 여부 (0=미포함, 1=포함)")
):
    """
    키워드 조회 (텍스트 응답)
    
    Args:
        categoryId: 카테고리 ID
        format: 출력 포맷 (txt=키워드만, tsv/csv=키워드+참여자수)
        includeRecomm: 추천 키워드 포함 여부
        
    Returns:
        텍스트 형식의 키워드 데이터
    """
    try:
        keywords = get_all_keywords(categoryId, DEFAULT_SLEEP_SEC_API)
        
        # 데이터 병합
        data = keywords['normal'].copy()
        
        if includeRecomm == 1 and keywords['recomm']:
            # 추천 키워드를 맨 위에 추가하고 빈 줄로 구분
            if format == "txt":
                # txt 포맷: 추천 키워드 + 빈 줄 + 일반 키워드
                recomm_text = format_keywords_txt(keywords['recomm'])
                normal_text = format_keywords_txt(keywords['normal'])
                return f"{recomm_text}\n\n{normal_text}"
            else:
                # tsv/csv 포맷: 추천을 맨 위에 추가 (빈 줄 없이)
                data = keywords['recomm'] + keywords['normal']
        
        # 포맷 변환
        if format == "txt":
            return format_keywords_txt(data)
        elif format == "tsv":
            return format_keywords_tsv(data)
        else:  # csv
            return format_keywords_csv(data)
            
    except ValueError as e:
        # GraphQL 오류
        raise HTTPException(status_code=502, detail=f"네이버 응답 오류: {str(e)}")
    except Exception as e:
        # 네트워크 오류 등
        raise HTTPException(status_code=502, detail=f"키워드 조회 실패: {str(e)}")
