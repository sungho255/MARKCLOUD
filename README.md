# 마크클라우드 백엔드 개발자 채용 과제

## API 사용법 및 실행 방법
  - 실행 환경 설정
  1. Python 환경 설정

  <pre> $ pip install -r requirements.txt  </pre>

  2. 서버 실행

  <pre> $ python main.py  </pre>

## 구현된 기능 설명
  - Indexing
    - async-elasticsearch를 활용해 비동기 처리로 속도를 향상시킴
    - copy_to를 활용하여 여러 필드를 하나의 통합 필드로 복사, 검색 효율성 향상
      
  - Searching
    - match query와 term query를 조합하여 정확한 검색과 자연어 기반 검색을 모두 지원
    - minimum_should_match를 사용하여 유사도가 일정 수준 이상인 문서만 반환
      
## 기술적 의사결정에 대한 설명
  - match + term 조합
    - match는 형태소 단위로 분해하여 유사한 문서 검색에 유리
    - term은 정확히 일치하는 키워드를 찾을 때 사용
    - 두 쿼리를 적절히 조합하여 검색 정확도와 유연성을 동시에 확보
  
  - minimum_should_match
    - 검색 결과의 품질 제어를 위해 도입
    - 너무 적은 키워드 일치로 인한 검색 오류를 방지
  
  - copy_to
    - 여러 필드를 하나의 필드로 통합하여 검색 인덱스 관리 단순화
      ex) productName과 productNameEng를 all_text_fields로 복사하여 단일 필드 기반 검색 가능
  
  - AsyncElasticsearch
    - 동기 방식보다 효율적이고, 수천 건 이상의 데이터를 색인할 때 속도 향상
    - asyncio.gather()를 이용해 병렬로 bulk indexing 처리

## 문제 해결 과정에서 고민했던 점
  - 전체 색인 과정이 적은 데이터 양에 비해 오래 걸림
    
    -> 비동기 처리 도입: async-elasticsearch로 전환하고, asyncio.gather()를 이용한 병렬 색인 작업을 수행함으로써 0.85초에서  0.33초까지 속도 단축
  - 키워드가 정확하게 일치하지 않으면 원하는 결과를 찾을 수 없음
    
    -> 검색 정확도 향상: 단순 match 쿼리는 검색 품질이 낮아, minimum_should_match와 copy_to를 통해 검색 품질과 성능을 함께 향상시킴

## 개선하고 싶은 부분 (선택사항)
  - 기본 standard analyzer로는 한국어 분해 성능이 떨어짐, 한국어 형태소 분석기(nori) 기반 커스텀 analyzer 적용하고 싶음
  - 부분 색인을 통해 자주 변경되는 데이터만 재색인하고 싶음
