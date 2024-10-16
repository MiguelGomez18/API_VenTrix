from pydantic import BaseModel
from datetime import datetime

class Sucursal(BaseModel):
    nit: str
    rut: str
    nombre: str
    direccion: str
    telefono: str
    correo: str

class Propietario(BaseModel):
    documento:int
    nombre:str
    correo:str
    password:str

class Login(BaseModel):
    correo:str
    password:str

class Producto(BaseModel):
    id: int 
    nombre: str
    precio: int
    id_categoria:int

class Categoria(BaseModel):
    nombre:str
    
class Mesas(BaseModel):
    nombre:str
    
    


class Venta(BaseModel):
    id: int
    id_pedido: int
    id_producto: int
    cantidad: int
    total: float
    fecha_hora: datetime 