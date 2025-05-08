import asyncio, json, time, traceback
from datetime import datetime
from elasticsearch import AsyncElasticsearch, helpers

from fastapi import APIRouter, HTTPException, status

from mapping.trademark_mapping import trade_mappings
from client.trade_clinet import client
##############################################################################################
tradeindexing = APIRouter(prefix='/tradeindexing')

MAPPINGS = trade_mappings  # Elasticsearch에 사용할 매핑
DOCUMENTS = "trademark_sample.json"  # 업로드할 JSON 문서 경로
INDEX_NAME = "trademark"

# 매핑에서 'text' 타입 필드를 추출하는 함수
def extract_text_fields(mappings):
    text_fields = []
    properties = mappings.get("mappings", {}).get("properties", {})
    for field_name, field_info in properties.items():
        # 'text' 타입 필드만 추출
        if field_info.get("type") == "text":
            text_fields.append(field_name)
    return text_fields


# 문서를 클린징하는 함수
# 텍스트 필드가 None일 경우 빈 문자열로 대체
def clean_doc(doc, mappings):
    text_fields = extract_text_fields(mappings)
    
    doc_copy = doc.copy()
    for k, v in doc_copy.items():
        # 해당 필드가 텍스트 필드이고 값이 None일 경우 빈 문자열로 처리
        if v is None and k in text_fields:
            doc_copy[k] = ""
    return doc_copy


# 데이터를 배치로 나누는 함수
def split_batches(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


# 각 배치를 Elasticsearch에 색인하는 함수
async def index_batch(batch, batch_idx, batch_size, mappings):
    start = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    # 배치 시작 로그 (출력 생략 가능)
    # print(f"[{start}] 배치 {batch_idx} 시작")
    
    actions = [
        {
            "_index": INDEX_NAME,  # 색인 이름
            "_id": f"{INDEX_NAME}_id_{batch_idx * batch_size + i}",  # 문서 ID
            "_source": clean_doc(doc, mappings)  # 문서 내용 클린징 후 추가
        }
        for i, doc in enumerate(batch)
    ]
    
    # 비동기적으로 데이터를 Elasticsearch에 색인 (bulk 방식)
    await helpers.async_bulk(client, actions)
    
    end = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    # 배치 완료 로그 (출력 생략 가능)
    # print(f"[{end}] 배치 {batch_idx} 완료")


# 비동기적으로 색인 작업을 처리하는 메인 함수
async def async_indexing(mappings=MAPPINGS, batch_size=50):
    # Elasticsearch에 인덱스 생성
    await client.indices.create(index=INDEX_NAME, body=mappings)
    
    # JSON 파일에서 데이터 읽기
    with open(f"{DOCUMENTS}", "r", encoding="utf-8") as f:
        data = json.load(f)

    tasks = []
    # 데이터를 배치 크기(batch_size)로 나누어 작업 생성
    for idx, batch in enumerate(split_batches(data, batch_size)):
        tasks.append(index_batch(batch, idx, batch_size, mappings))

    # 병렬 실행을 위한 세마포어 설정 (최대 20개 작업 동시 실행)
    semaphore = asyncio.Semaphore(20)
    start_time = time.time()
    
    # 세마포어를 사용하여 각 작업을 비동기적으로 실행
    async def sem_task(task_func):
        async with semaphore:
            return await task_func

    # 비동기 작업을 병렬로 실행
    await asyncio.gather(*(sem_task(t) for t in tasks))
    
    end_time = time.time()
    # 작업 종료 후 소요 시간 출력 (출력 생략 가능)
    # print(f"Bulk 색인 소요 시간: {end_time - start_time:.2f}초")
    
    # Elasticsearch 연결 종료
    await client.close()

# FastAPI에서 색인 작업을 실행하는 POST 엔드포인트
@tradeindexing.post("/indexing", status_code = status.HTTP_200_OK, tags=['Indexing'])
def indexing():
    print('\n\033[36m[Elasticsearch API] \033[32m 인덱싱')  # 색인 시작 로그
    try:
        # 비동기 색인 작업 실행
        asyncio.run(async_indexing(MAPPINGS, 50))
    except Exception as e:
        # 에러 발생 시 로그 출력 및 HTTP 응답 반환
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"에러 발생: {str(e)}"
        }
