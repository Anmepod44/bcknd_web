from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from fastapi.requests import Request
from typing import List
from orm import Product,Department,Features,Package

app = FastAPI()

class Feature(BaseModel):
    name: str = Field(..., example="Unified Search Experience")
    description: str = Field(..., example="Transformative AI Power: Amazon Q Business leverages generative AI...")
    image: str = Field(..., example="analytics.png")
    cta: str = Field(..., example="Learn More")

class Product(BaseModel):
    name: str = Field(..., example="Amazon Q")
    image: HttpUrl = Field(..., example="https://example.com/amazon-q-image.jpg")
    description: str = Field(..., example="Your employees spend countless hours sifting through emails, documents, and online resources...")
    department_serial: str = Field(..., example="D001")
    department_name: str = Field(..., example="Storage Solutions")
    features: List[Feature]

class Package(BaseModel):
    name: str = Field(..., example="Bronze Package")
    image: HttpUrl = Field(..., example="https://example.com/bronze-package-image.jpg")
    description: str = Field(..., example="The Bronze Package is tailored for small businesses aiming to enhance productivity...")
    products: List[Product]

#Set up templates directory.
templates=Jinja2Templates(directory=r"./templates")

@app.get("/")
def get(request:Request):
    return templates.TemplateResponse('form.html',{'request':request})
# Post a Package model using fastapi

@app.post("/product")
def post_product(product:Product):
    print(product)
    sample_product=Product(product)
    
    return sample_product.pk

# Run using this command : uvicorn model:app --host 0.0.0.0 --port 5000 --reload