from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl
from typing import List

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

# To get the index page of the website.
@app.get("/")
def index():
    return {"message":"welcome to fastapi"}

# Post a Package model using fastapi
@app.post("/product")
def post_product(product:Product):
    return product


# Code to run the server locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)


# Run using this command : uvicorn model:app --host 0.0.0.0 --port 5000 --reload