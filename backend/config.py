"""
설정 상수 모듈

네이버 인플루언서 키워드 수집에 사용되는 모든 설정값을 정의합니다.
"""

# API 엔드포인트
NAVER_INFLUENCER_URL = "https://in.naver.com/keywords"
GRAPHQL_URL = "https://in.naver.com/graphql"

# 스크래핑 설정
DEFAULT_SLEEP_SEC_CLI = 3  # CLI 기본값 (기존 유지)
DEFAULT_SLEEP_SEC_API = 2  # API 기본값 (더 빠른 응답)
MIN_SLEEP_SEC = 0
MAX_SLEEP_SEC = 10
DEFAULT_LIMIT = 20
RECOMMEND_LIMIT = 3

# 저장 설정
DEFAULT_FORMAT = "txt"  # CLI 기본값 (키워드명만)
SUPPORTED_FORMATS = ["txt", "tsv", "csv"]

# HTTP 헤더
HEADERS_HTML = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

HEADERS_GRAPHQL = {
    'Accept-Language': 'ko-KR,ko;q=0.7',
    'Origin': 'https://in.naver.com',
    'Referer': 'https://in.naver.com/keywords',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'content-type': 'application/json',
}

# GraphQL 쿼리
QUERY_WHITE_POOL_KEYWORDS = """query getWhitePoolKeywords($input: WhitePoolKeywordInput!) {
  whitePoolKeywords(input: $input) {
    ...Keyword
    __typename
  }
}

fragment Keyword on Keyword {
  categoryId
  challengeable
  challengeableContentCount
  challengedKeyword
  id
  name
  participantCount
  property
  thumbnailUrl
  __typename
}
"""

QUERY_SEARCH_CATEGORY_KEYWORDS = """query getSearchCategoryKeywords($input: SearchKeywordInput!, $paging: PagingInput!) {
  searchCategoryKeywords(input: $input, paging: $paging) {
    items {
      ... on Keyword {
        categoryId
        challengeable
        id
        issueKeyword
        name
        participantCount
        thumbnailUrl
        challengedKeyword
        issueKeyword
        __typename
      }
      __typename
    }
    paging {
      nextCursor
      total
      __typename
    }
    __typename
  }
}
"""
