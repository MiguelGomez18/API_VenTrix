from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional
from modelo import EstadoPedido, RolUsuario, EstadoRestaurante, EstadoSucursal,EstadoMesa

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


class DetallePedidoSchema(BaseModel):
    id_detalle_pedido: int  # ID del detalle del pedido
    cantidad: int  # Cantidad de productos
    hora_detalle: time  # Hora del detalle del pedido
    descripcion: Optional[str] = None  # Descripción opcional del detalle
    precio_total: float  # Precio total del detalle
    sucursal: str  # Sucursal donde se realizó el pedido
    id_producto: int  # ID del producto asociado
    id_pedido: int  # ID del pedido al que pertenece este detalle

    class Config:
        orm_mode = True

# Si deseas incluir información del producto, puedes crear otro esquema
class ProductoSchema(BaseModel):
    id_producto: int  # ID del producto
    nombre: str  # Nombre del producto
    precio: float  # Precio del producto

    class Config:
        orm_mode = True

# Si deseas anidar el producto dentro del detalle del pedido
class DetallePedidoConProductoSchema(BaseModel):
    id_detalle_pedido: int
    cantidad: int
    hora_detalle: time
    descripcion: Optional[str] = None
    precio_total: float
    sucursal: str
    producto: ProductoSchema  # Detalles del producto asociado
    id_pedido: int




class PedidoSchema(BaseModel):
    id_pedido: Optional[int] = None
    fecha_pedido: date
    hora_pedido: time
    estado: EstadoPedido = EstadoPedido.ORDENADO
    total_pedido: Optional[float] = 0.0
    nombre: Optional[str] = None
    sucursal: str
    id_mesa: Optional[int] = None
    id_tipo_pago: Optional[int] = None
    
    
    
class ProductoSchema(BaseModel):
    id_producto: Optional[int] = None
    nombre: str
    precio: float
    imagen: Optional[str] = None
    disponibilidad: bool
    id_sucursal: int
    id_categoria: int

    class Config:
        orm_mode = True


#----------------------MESAS--------------------------


class MesaSchema(BaseModel):
    nombre: str
    estado: EstadoMesa
    id_sucursal: int

    class Config:
        orm_mode = True


#----------------------CATEGORIA---------------------
class CategoriaSchema(BaseModel):
    nombre: str
    sucursal: str

    class Config:
        orm_mode = True


#----------------------Tipos de pago----------------

class TipoPagoSchema(BaseModel):
    descripcion: str
    sucursal: str

    class Config:
        orm_mode = True