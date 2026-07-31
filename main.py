from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Product
from database import session, engine
import db_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db_models.Base.metadata.create_all(bind=engine)

products_list = [
    Product(id=1, name="Product 1", description="dfgger", price=10.99, quantity=5),
    Product(id=2, name="Product 2", description="dfgger", price=19.99, quantity=3),
    Product(id=3, name="Product 3", description="dfgger", price=5.99, quantity=10),
    Product(id=4, name="Product 4", description="dfgger", price=5.59, quantity=30),
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    try:
        count = db.query(db_models.Product).count()
        if count == 0:
            for product in products_list:
                db.add(db_models.Product(**product.model_dump()))
            db.commit()
    finally:
        db.close()


init_db()


@app.get("/")
def greet():
    return {"message": "Hello, World!"}


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(db_models.Product).all()


@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = db_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
