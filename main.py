# Base
import os
from dotenv import load_dotenv

# FastAPI
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status

# Module
from Indexing.trademark_indexing import tradeindexing
from search.trademark_search import tradesearching
#################################################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

# Default
@app.get("/")
def say_hello():
    return {"message": "Hello world from FastAPI"}

# 인덱싱
app.include_router(tradeindexing)

# 검색
app.include_router(tradesearching)

if __name__ == '__main__':
    print(f'Documents: http://localhost:8000/docs')
    uvicorn.run("main:app", reload=True)