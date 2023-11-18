from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

app = FastAPI()
#se hace una peticion get  en esta ulr '/' que es como el index
@app.get("/")
#se define la funcion que devuelve un diccionario
def read_root():
    return {"Hello": "World"}







app = FastAPI()
products = [ {
    "ID" : 1,
    "Product"  : "Carnes",
    "Price"  : "20$"
},
{
    "ID" : 2,
    "Product"  : "Pescados",
    "Price"  : "15$"
}         ]
#aqui lo mismo pero creas url donde encontraras el contenido de products 
@app.get('/Products')
def get_product():
    return products
#aqui lo mismo pero agregamos un parametro a la url llamada id que recibe datos tipo int
@app.get('/Products/{ID}')
def getID(ID: int):
    return list(filter(lambda item: item ['ID'] == ID, products ))
      
    