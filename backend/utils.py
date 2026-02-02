"""
유틸리티 함수 모듈

데이터 포맷 변환 및 파일 저장 기능을 제공합니다.
"""

import csv
import io
from typing import List, Dict

from .config import DEFAULT_FORMAT, SUPPORTED_FORMATS


def format_keywords_txt(keywords: List[Dict]) -> str:
    """
    키워드명만 추출 (기존 CLI 방식)
    
    Args:
        keywords: [{'name': ..., 'participantCount': ...}, ...]
        
    Returns:
        키워드명을 줄바꿈으로 구분한 문자열
    """
    return "\n".join(k['name'] for k in keywords)


def format_keywords_tsv(keywords: List[Dict]) -> str:
    """
    키워드명\t참여자수 형식 (TSV)
    
    Args:
        keywords: [{'name': ..., 'participantCount': ...}, ...]
        
    Returns:
        TSV 형식 문자열
    """
    lines = []
    for k in keywords:
        lines.append(f"{k['name']}\t{k['participantCount']}")
    return "\n".join(lines)


def format_keywords_csv(keywords: List[Dict]) -> str:
    """
    CSV 형식 (헤더 포함)
    
    Args:
        keywords: [{'name': ..., 'participantCount': ...}, ...]
        
    Returns:
        CSV 형식 문자열
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 헤더
    writer.writerow(['keyword', 'participantCount'])
    
    # 데이터
    for k in keywords:
        writer.writerow([k['name'], k['participantCount']])
    
    return output.getvalue()


def save_keywords(
    category_name: str, 
    keywords: Dict[str, List[Dict]], 
    format: str = DEFAULT_FORMAT, 
    include_recomm: bool = False
) -> str:
    """
    키워드 데이터를 파일로 저장
    
    Args:
        category_name: 카테고리명 (파일명으로 사용)
        keywords: {'recomm': [...], 'normal': [...]}
        format: 'txt' | 'tsv' | 'csv'
        include_recomm: 추천 키워드 포함 여부
        
    Returns:
        저장된 파일 경로
        
    Raises:
        ValueError: 지원하지 않는 포맷
    """
    if format not in SUPPORTED_FORMATS:
        raise ValueError(f"지원하지 않는 포맷: {format}. 사용 가능: {SUPPORTED_FORMATS}")
    
    # 데이터 병합
    data = keywords['normal'].copy()
    if include_recomm and keywords['recomm']:
        data = keywords['recomm'] + data
    
    # 포맷 변환
    if format == "txt":
        content = format_keywords_txt(data)
    elif format == "tsv":
        content = format_keywords_tsv(data)
    else:  # csv
        content = format_keywords_csv(data)
    
    # 파일 저장
    # 파일명에서 슬래시 제거 (기존 동작 유지)
    safe_filename = category_name.replace('/', '')
    filepath = f"./{safe_filename}.{format}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filepath
