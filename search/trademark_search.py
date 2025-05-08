import asyncio, json, time, traceback
from datetime import datetime
from elasticsearch import AsyncElasticsearch, helpers

from fastapi import APIRouter, HTTPException, status

from mapping.trademark_mapping import trade_mappings
from client.trade_clinet import client
##############################################################################################
tradesearching = APIRouter(prefix='/tradesearching')

MAPPINGS = trade_mappings
INDEX_NAME = "trademark"

# match_term: 키워드로 match 및 term 검색 수행 (필터: publicationDate >= 20200101)
@tradesearching.post("/matchterm", status_code=status.HTTP_200_OK, tags=['Searching'])
async def match_term_search(key: str):
    print('\n\033[36m[Elasticsearch API] \033[32m match_term')

    query = {
        "bool": {
            "should": [
                { "match": { "all_text_fields": key } },  # 분석된 필드에서 검색 
                { "term": { "all_keyword_fields": key } } # 키워드 필드에서 정확히 일치하는 항목 검색
            ],
            "filter": [
                {
                    "range": {
                        "publicationDate": {
                            "gte": "20200101",   # 2020년 이후의 데이터만 검색
                            "format": "yyyyMMdd"
                        }
                    }
                }
            ]
        }
    }
 
    try:
        res = await client.search(index="trademark", query=query)
        await client.close()
        result = [hit["_source"] for hit in res["hits"]["hits"]]
        return { "status": "success", "results": result }

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"에러 발생: {str(e)}"
        }
    
# minimum_should_match: match 검색을 하되 최소 일치율을 50%로 설정
@tradesearching.post("/minimumshould", status_code=status.HTTP_200_OK, tags=['Searching'])
async def minimum_should_search(key: str):
    print('\n\033[36m[Elasticsearch API] \033[32m minimum_should')
    try:
        query = {
            "bool": {
                "should": [
                    {"match": {"all_text_fields": key}}
                ],
                "minimum_should_match": "50%"
            }
        }

        res = await client.search(index=INDEX_NAME, query=query)
        await client.close()
        results = [hit["_source"] for hit in res["hits"]["hits"]]

        return {"status": "success", "results": results}

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"에러 발생: {str(e)}"
        }
