from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json
import pandas as pd
from io import BytesIO
import os

app = FastAPI(title="한강주조 출고표 자동화 API")

# CORS 설정 (프론트엔드와 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 마스터리스트 로드
def load_master_lists():
    with open('data/company_master.json', 'r', encoding='utf-8') as f:
        companies = json.load(f)
    with open('data/product_master.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    return companies, products

# 정규화 함수
def normalize_company(company_name, companies):
    """업체명 정규화"""
    company_dict = {c['original']: c['normalized'] 
                   for c in companies['companies']}
    return company_dict.get(company_name, company_name)

def normalize_product(product_name, products):
    """물품명 정규화"""
    product_dict = {p['original']: p['normalized'] 
                   for p in products['products']}
    return product_dict.get(product_name, product_name)

# 루트 엔드포인트
@app.get("/")
def read_root():
    return {"message": "한강주조 출고표 자동화 API 서버 실행 중"}

# 카톡 데이터 파싱 API
@app.post("/api/parse")
async def parse_kakaotalk(text: str):
    """카톡 데이터를 파싱하여 정규화"""
    companies, products = load_master_lists()
    
    # 간단한 파싱 로직
    lines = text.split('\n')
    orders = []
    
    # 파싱 로직 (상세한 구현은 별도)
    # ...
    
    return {"orders": orders, "count": len(orders)}

# 엑셀 생성 API
@app.post("/api/generate-excel")
async def generate_excel(orders: list):
    """출고표 엑셀 파일 생성"""
    companies, products = load_master_lists()
    
    # 엑셀 생성 로직
    # 템플릿 로드 및 데이터 입력
    # ...
    
    # 파일 반환
    return FileResponse(path="output.xlsx", 
                       filename="출고표.xlsx",
                       media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 마스터리스트 조회 API
@app.get("/api/master-lists")
async def get_master_lists():
    """마스터리스트 반환"""
    companies, products = load_master_lists()
    return {
        "companies": companies['companies'],
        "products": products['products']
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)