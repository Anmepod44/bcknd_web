from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from fastapi.requests import Request
from typing import List
from orm import Product,Department,Features,Package

app = FastAPI()

class Feature_(BaseModel):
    name: str = Field(..., example="Unified Search Experience")
    description: str = Field(..., example="Transformative AI Power: Amazon Q Business leverages generative AI...")
    image: str = Field(..., example="analytics.png")
    cta: str = Field(..., example="Learn More")

class Product_(BaseModel):
    name: str = Field(..., example="Amazon Q")
    image: str = Field(..., example="https://example.com/amazon-q-image.jpg")
    description: str = Field(..., example="Your employees spend countless hours sifting through emails, documents, and online resources...")
    department_serial: str = Field(..., example="D001")
    department_name: str = Field(..., example="Storage Solutions")
    features: List[Feature_]

class Package_(BaseModel):
    name: str = Field(..., example="Bronze Package")
    image: str = Field(..., example="https://example.com/bronze-package-image.jpg")
    description: str = Field(..., example="The Bronze Package is tailored for small businesses aiming to enhance productivity...")
    products: List[Product_]

#Set up templates directory.
templates=Jinja2Templates(directory=r"./templates")

@app.get("/")
def get(request:Request):
    return templates.TemplateResponse('form.html',{'request':request})
# Post a Package model using fastapi

@app.post("/product")
def post_product(request:Request,product:Product_):
    prod_list=list()

    for feature in product.features:
        feature_=Features(
            name=feature.name,
            description=feature.description,
            image=str(feature.image),
            cta=feature.cta
        )

        prod_list.append(feature_)
    
    # Getting the department from the user.
    prod_department=Department(serial_no=product.department_serial, name=product.department_name)

    sample_product=Product(
        name=product.name,
        image=str(product.image),
        description=product.description,
        department=prod_department,
        features=prod_list

    )
    #Save the product before returning it.
    sample_product.save()
    return sample_product.pk

# Run using this command : uvicorn model:app --host 0.0.0.0 --port 5000 --reload