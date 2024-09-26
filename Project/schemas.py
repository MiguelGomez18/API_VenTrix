from pydantic import BaseModel

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
    id:int
    nombre:str