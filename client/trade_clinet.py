from elasticsearch import AsyncElasticsearch
##############################################################################################

ELASTIC_ID = "elastic"
ELASTIC_PASSWORD = "changeme"

# client instance 생성
local_client = AsyncElasticsearch(
    "https://localhost:9200",   # endpoint
    ca_certs="C:/elasticsearch-9.0.0/config/certs/http_ca.crt",
    basic_auth=(ELASTIC_ID, ELASTIC_PASSWORD)
)

client = AsyncElasticsearch(
        "https://d91a7e7d99d242c1a857b6717a6038d5.us-central1.gcp.cloud.es.io:443",  # Cloud endpoint
        api_key="eF82aG41WUJiRXRSTU93b3BxZm46Mkg3SEFQUGFZR3BidlJwMy1yZGtwQQ=="
    )