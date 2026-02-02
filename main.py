"""
네이버 인플루언서 키워드 수집 CLI 스크립트

기존 동작을 100% 유지하면서 backend 모듈을 활용합니다.
"""

from backend.scraper import fetch_categories, get_all_keywords
from backend.utils import save_keywords
from backend.config import DEFAULT_SLEEP_SEC_CLI


def get_user_choice(menu):
    """
    사용자 입력을 안전하게 받고 검증
    
    Args:
        menu: 카테고리 목록
        
    Returns:
        선택한 카테고리 인덱스 (0-based) 또는 None (종료)
    """
    while True:
        try:
            choice = input("\n원하는 카테고리 번호를 선택하세요: ")
            choice_num = int(choice)
            
            # 종료 선택 (메뉴 개수 + 1)
            if choice_num == len(menu) + 1:
                return None
            
            # 범위 검증 (1 ~ len(menu))
            if 1 <= choice_num <= len(menu):
                return choice_num - 1  # 0-based 인덱스로 변환
            else:
                print(f"❌ 1부터 {len(menu) + 1} 사이의 숫자를 입력하세요.")
                
        except ValueError:
            print("❌ 숫자를 입력하세요.")
        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다.")
            return None


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("네이버 인플루언서 키워드 수집 프로그램")
    print("=" * 60)
    
    # 카테고리 목록 조회
    try:
        print("\n📋 카테고리 목록을 불러오는 중...")
        menu = fetch_categories()
        
        if not menu:
            print("❌ 카테고리 정보를 불러올 수 없습니다.")
            return
            
        print(f"✅ {len(menu)}개의 카테고리를 불러왔습니다.\n")
        
    except Exception as e:
        print(f"❌ 카테고리 조회 실패: {str(e)}")
        print("네트워크 연결을 확인하거나 나중에 다시 시도하세요.")
        return
    
    # 메인 루프
    while True:
        try:
            # 카테고리 메뉴 출력
            print("\n" + "=" * 60)
            for idx, category in enumerate(menu, 1):
                print(f"{idx}. {category['name']} (키워드 수: {category['keywordCount']}개)")
            print(f"{len(menu) + 1}. 종료")
            print("=" * 60)
            
            # 사용자 선택
            choice_idx = get_user_choice(menu)
            
            if choice_idx is None:
                print("\n프로그램을 종료합니다. 👋")
                break
            
            # 선택한 카테고리 정보
            selected = menu[choice_idx]
            category_id = selected['id']
            category_name = selected['name']
            
            print(f"\n📦 '{category_name}' 카테고리의 키워드를 수집합니다...")
            print(f"   카테고리 ID: {category_id}")
            
            # 키워드 수집
            try:
                keywords = get_all_keywords(category_id, DEFAULT_SLEEP_SEC_CLI)
                
                recomm_count = len(keywords['recomm'])
                normal_count = len(keywords['normal'])
                total_count = recomm_count + normal_count
                
                print(f"\n✅ 키워드 수집 완료!")
                print(f"   - 추천 키워드: {recomm_count}개")
                print(f"   - 일반 키워드: {normal_count}개")
                print(f"   - 총 {total_count}개")
                
                # 파일 저장 (기본 포맷: txt, 키워드명만)
                filepath = save_keywords(
                    category_name, 
                    keywords, 
                    format="txt",  # 기존 방식 유지
                    include_recomm=False  # 일반 키워드만 저장 (기존 동작)
                )
                
                print(f"\n💾 파일 저장 완료: {filepath}")
                print(f"   (일반 키워드 {normal_count}개가 저장되었습니다)")
                
            except ValueError as e:
                # GraphQL 오류 (네이버 응답 문제)
                print(f"\n❌ 네이버 응답 오류: {str(e)}")
                print("   카테고리 ID가 올바른지 확인하거나 나중에 다시 시도하세요.")
                
            except Exception as e:
                # 네트워크 오류 등
                print(f"\n❌ 키워드 수집 실패: {str(e)}")
                print("   네트워크 연결을 확인하거나 나중에 다시 시도하세요.")
            
        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다. 👋")
            break
        except Exception as e:
            # 예상치 못한 오류 (프로그램 크래시 방지)
            print(f"\n❌ 예상치 못한 오류: {str(e)}")
            print("   메뉴로 돌아갑니다.")


if __name__ == "__main__":
    main()