"""
스크래핑 비즈니스 로직 모듈

네이버 인플루언서 플랫폼에서 카테고리 및 키워드 데이터를 수집하는 함수들을 제공합니다.
"""

import requests
import json
import re
import time
from typing import List, Dict, Optional

from .config import (
    NAVER_INFLUENCER_URL,
    GRAPHQL_URL,
    HEADERS_HTML,
    HEADERS_GRAPHQL,
    QUERY_WHITE_POOL_KEYWORDS,
    QUERY_SEARCH_CATEGORY_KEYWORDS,
    RECOMMEND_LIMIT,
    DEFAULT_LIMIT,
)


def fetch_categories() -> List[Dict]:
    """
    네이버 인플루언서 카테고리 목록 조회
    
    Returns:
        카테고리 정보 리스트 [{'id': ..., 'name': ..., 'keywordCount': ...}, ...]
        
    Raises:
        requests.RequestException: 네트워크 오류
        ValueError: 응답 파싱 실패
    """
    try:
        response = requests.get(NAVER_INFLUENCER_URL, headers=HEADERS_HTML, timeout=10)
        response.raise_for_status()
        
        # window.__PRELOADED_STATE__ 추출
        pattern = r'window.__PRELOADED_STATE__ = (.*?);'
        match = re.search(pattern, response.text)
        
        if not match:
            raise ValueError("카테고리 정보를 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다.")
        
        data = json.loads(match.group(1))
        
        # 데이터 구조 검증
        if 'keyword' not in data or 'categoryGroups' not in data['keyword']:
            raise ValueError("예상하지 못한 데이터 구조입니다.")
        
        category_groups = data['keyword']['categoryGroups']['data']
        
        # 모든 카테고리 평탄화
        categories = []
        for group in category_groups:
            if 'categories' in group:
                categories.extend(group['categories'])
        
        return categories
        
    except requests.RequestException as e:
        raise requests.RequestException(f"카테고리 목록 조회 실패: {str(e)}")
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"응답 파싱 실패: {str(e)}")


def fetch_recommend_keywords(category_id: str) -> List[Dict]:
    """
    추천 키워드 조회 (상위 3개)
    
    Args:
        category_id: 카테고리 ID
        
    Returns:
        [{'name': '키워드명', 'participantCount': 123}, ...]
        
    Raises:
        requests.RequestException: 네트워크 오류
        ValueError: GraphQL 응답에 errors 포함 또는 data 없음
    """
    json_data = {
        'operationName': 'getWhitePoolKeywords',
        'variables': {
            'input': {
                'categoryId': category_id,
                'limit': RECOMMEND_LIMIT,
            },
        },
        'query': QUERY_WHITE_POOL_KEYWORDS,
    }
    
    try:
        response = requests.post(GRAPHQL_URL, headers=HEADERS_GRAPHQL, json=json_data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        # GraphQL 오류 확인
        if 'errors' in result:
            error_msg = result['errors'][0].get('message', '알 수 없는 오류') if result['errors'] else '알 수 없는 오류'
            raise ValueError(f"GraphQL 오류: {error_msg}")
        
        if 'data' not in result or 'whitePoolKeywords' not in result['data']:
            raise ValueError("응답에 data가 없습니다.")
        
        keywords_data = result['data']['whitePoolKeywords']
        
        # 필요한 필드만 추출
        keywords = []
        for k in keywords_data:
            keywords.append({
                'name': k['name'],
                'participantCount': k['participantCount']
            })
        
        return keywords
        
    except requests.RequestException as e:
        raise requests.RequestException(f"추천 키워드 조회 실패: {str(e)}")
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"응답 파싱 실패: {str(e)}")


def fetch_all_keywords(category_id: str, sleep_sec: float = 2.0) -> List[Dict]:
    """
    카테고리의 모든 키워드 조회 (페이지네이션)
    
    Args:
        category_id: 카테고리 ID
        sleep_sec: 요청 간 대기 시간 (초)
        
    Returns:
        [{'name': '키워드명', 'participantCount': 123}, ...]
        
    Raises:
        requests.RequestException: 네트워크 오류
        ValueError: GraphQL 응답 오류
    """
    keywords = []
    cursor: Optional[str] = None
    
    while True:
        try:
            # 페이지네이션 변수 설정
            variables = {
                'input': {
                    'categoryId': category_id,
                    'name': '',
                },
                'paging': {
                    'limit': DEFAULT_LIMIT,
                },
            }
            
            if cursor:
                variables['paging']['cursor'] = cursor
            
            json_data = {
                'operationName': 'getSearchCategoryKeywords',
                'variables': variables,
                'query': QUERY_SEARCH_CATEGORY_KEYWORDS,
            }
            
            response = requests.post(GRAPHQL_URL, headers=HEADERS_GRAPHQL, json=json_data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            # GraphQL 오류 확인
            if 'errors' in result:
                error_msg = result['errors'][0].get('message', '알 수 없는 오류') if result['errors'] else '알 수 없는 오류'
                raise ValueError(f"GraphQL 오류: {error_msg}")
            
            if 'data' not in result or 'searchCategoryKeywords' not in result['data']:
                raise ValueError("응답에 data가 없습니다.")
            
            main_data = result['data']['searchCategoryKeywords']
            items = main_data['items']
            paging = main_data['paging']
            
            # 키워드 추출
            for k in items:
                keywords.append({
                    'name': k['name'],
                    'participantCount': k['participantCount']
                })
            
            # 다음 페이지 확인
            next_cursor = paging.get('nextCursor')
            if not next_cursor:
                break
            
            cursor = next_cursor
            
            # Rate limiting 방지
            if sleep_sec > 0:
                time.sleep(sleep_sec)
                
        except requests.RequestException as e:
            raise requests.RequestException(f"키워드 조회 실패: {str(e)}")
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"응답 파싱 실패: {str(e)}")
    
    return keywords


def get_all_keywords(category_id: str, sleep_sec: float = 2.0) -> Dict[str, List[Dict]]:
    """
    추천 + 일반 키워드 모두 조회
    
    Args:
        category_id: 카테고리 ID
        sleep_sec: 요청 간 대기 시간 (초)
        
    Returns:
        {'recomm': [...], 'normal': [...]}
        
    Raises:
        requests.RequestException: 네트워크 오류
        ValueError: GraphQL 응답 오류
    """
    recomm = fetch_recommend_keywords(category_id)
    normal = fetch_all_keywords(category_id, sleep_sec)
    
    return {
        'recomm': recomm,
        'normal': normal
    }
