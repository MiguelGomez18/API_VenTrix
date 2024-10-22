from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class Sucursal(BaseModel):
    nit: str
    rut: str
    nombre: str
    direccion: str
    telefono: str
    correo: str
    documento: int

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

# Definir un Enum para los estados
class EstadoMesa(str, Enum):
    fisica = "Fisica"
    rapida = "Rapida"

# Definir la clase Mesas con el Enum
class Mesas(BaseModel):
    nombre: str
    estado: EstadoMesa

class Venta(BaseModel):
    id: int
    id_pedido: int
    id_producto: int
    cantidad: int
    total: float
    fecha_hora: datetime 


class TipoPago(BaseModel):
    id: int
    descripcion: str


class Mesa_rapida(BaseModel):
    nombre: str