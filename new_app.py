from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from mysql_orm import Product, Department, Features, Package, engine, Base, sessionmaker

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get the SQLAlchemy session
def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# Set up templates directory.
templates = Jinja2Templates(directory="./templates")

@app.get("/")
def get(request: Request):
    return templates.TemplateResponse('form.html', {'request': request})

# Post a Product model using FastAPI
@app.post("/product")
def post_product(product: Product_, db: Session = Depends(get_db)):

    #Print the sent product to the command line.
    print(product)
    try:
        # Create the Department object
        department = db.query(Department).filter_by(serial_no=product.department_serial).first()
        if not department:
            department = Department(serial_no=product.department_serial, name=product.department_name)
            db.add(department)
            db.commit()
            db.refresh(department)


        # Create the Features list
        feature_list = []
        for feature_data in product.features:
            feature = Features(
                name=feature_data.name,
                description=feature_data.description,
                image=feature_data.image,
                cta=feature_data.cta
            )
            db.add(feature)
            db.commit()
            db.refresh(feature)
            feature_list.append(feature)

        # Create the Product object
        new_product = Product(
            name=product.name,
            image=product.image,
            description=product.description,
            department_id=department.id,
            features=feature_list
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {"product_id": new_product.id}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

# Run using this command: uvicorn model:app --host 0.0.0.0 --port 5000 --reload