from fastapi import FastAPI,Depends,HTTPException
from contextlib import asynccontextmanager
from .crud import consume_messages
import asyncio
from .db import create_table,get_session
from .scehma import ProductAdd,Product
from typing import Annotated
from sqlmodel import Session
import multipart
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifspan event is started")
    print("table creating....")
    create_table()
    print("creating table succesfully")
    task = asyncio.create_task(consume_messages('userService', 'broker:19092'))
    yield
    
    
app = FastAPI(lifespan=lifespan,
               title="FastAPI Service",
               description="This is a FastAPI Service",
               version="0.0.1"
)


@app.get("/")
async def root():
    return {"message": "welcome to the product Service"}

@app.post('/product/')
async def create_product(product:ProductAdd,session:Annotated[Session,Depends(get_session)]):
    product_data = Product(product_name=product.product_name,product_category=product.product_category,
                           product_price=product.product_price,product_quantity=product.product_quantity)
    session.add(product_data)
    session.commit()
    session.refresh(product_data)

    return {"message": "product created successfully"}


@app.get('/product/')
async def get_product(session:Annotated[Session,Depends(get_session)]):
 
    products = session.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products
    






