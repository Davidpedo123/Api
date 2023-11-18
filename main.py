from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configura la conexión a la base de datos SQLite
DATABASE_URL = "sqlite:///./northwind.db"
engine = create_engine(DATABASE_URL)

# Define el modelo de datos
Base = declarative_base()

class Product(Base):
    __tablename__ = "Products"
    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String, index=True)
    SupplierID = Column(Integer)
    CategoryID = Column(Integer)
    QuantityPerUnit = Column(String)
    UnitPrice = Column(Float)
    UnitsInStock = Column(Integer)
    UnitsOnOrder = Column(Integer)
    ReorderLevel = Column(Integer)
    Discontinued = Column(Integer)

# Crea la tabla en la base de datos
Base.metadata.create_all(bind=engine)

# Configura la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Configura CORS
origins = [
    "http://127.0.0.1:3000",
    "http://127.0.0.1:7000",
    "http://localhost:3000",# Permitir solicitudes desde este origen
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener un producto por su ID
@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.ProductID == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
