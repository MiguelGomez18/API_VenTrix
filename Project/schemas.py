from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from modelo import RolUsuario, EstadoRestaurante, EstadoSucursal

class SucursalSchema(BaseModel):
    id: str
    nombre: str
    direccion: str
    ciudad: str
    telefono: str
    fecha_apertura: date
    estado: EstadoSucursal
    administrador: Optional[str] = None

    class Config:
        orm_mode = True

class RestauranteSchema(BaseModel):
    id: str
    nombre: str
    descripcion: Optional[str] = None
    telefono: str
    direccion: str
    correo: str
    imagen: str
    fecha_creacion: date
    fecha_finalizacion: date
    estado: EstadoRestaurante
    sucursales: Optional[List[SucursalSchema]] = None

    class Config:
        orm_mode = True

class RestauranteCreateSchema(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    telefono: str
    direccion: str
    correo: str
    imagen: str
    fecha_creacion: date
    fecha_finalizacion: date
    estado: str
    id_usuario: str

    class Config:
        orm_mode = True

class RestauranteUpdateSchema(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    telefono: Optional[str]
    direccion: Optional[str]
    correo: Optional[str]
    imagen: Optional[str]
    fecha_creacion: Optional[date]
    fecha_finalizacion: Optional[date]
    estado: Optional[str]
    id_usuario: Optional[str]

    class Config:
        orm_mode = True

class UsuarioSchema(BaseModel):
    documento: str
    nombre: str
    correo: str
    rol: RolUsuario
    fecha_creacion: date
    sucursal: str
    restaurantes: Optional[List[RestauranteSchema]] = None

    class Config:
        orm_mode = True

class UsuarioCreateSchema(BaseModel):
    documento: str
    nombre: str
    correo: str
    password: str
    rol: RolUsuario
    fecha_creacion: date
    sucursal: str

    class Config:
        orm_mode = True

class UsuarioLoginSchema(BaseModel):
    correo: str
    password: str

    class Config:
        orm_mode = True
