import json
from fastapi import APIRouter
from models.product import Product
from typing import List

router = APIRouter(tags=['Product Management'])

PRODUCTS_FILE = 'database/products.json'

def read_products():
    with open(PRODUCTS_FILE, 'r') as file:
        return json.load(file)

def write_products(products):
    with open(PRODUCTS_FILE, 'w') as file:
        json.dump(products, file, indent=4)

@router.get('/all/', response_model=List[Product])
async def all_products():
    return read_products()

@router.post('/add/', response_model=Product)
async def add_product(product: Product):
    products = read_products()
    if any(p['id'] == product.id for p in products):
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products.append(product.dict())
    write_products(products)
    return product
