from sqlalchemy import Boolean, Column, Float, Integer, String, Enum as SQLAlchemyEnum, Date, ForeignKey, Time
from sqlalchemy.orm import relationship
from datetime import date
from conexion import base
from enum import Enum

class RolUsuario(Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    CAJERO = "CAJERO"
    MESERO = "MESERO"
    COCINA = "COCINA"
    ADMINISTRADOR_SUCURSAL = "ADMINISTRADOR_SUCURSAL"

class EstadoUsuario(Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

class Usuario(base):
    __tablename__ = "usuario"

    documento = Column(String(10), primary_key=True, unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(100), nullable=False)
    password = Column(String(50), nullable=False)
    rol = Column(SQLAlchemyEnum(RolUsuario), nullable=False)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    sucursal = Column(String(100), nullable=True)
    estado = Column(SQLAlchemyEnum(EstadoUsuario), nullable=False, default=EstadoUsuario.ACTIVO)

    # Relación uno a uno con Restaurante
    restaurante = relationship("Restaurante", back_populates="usuario")


class EstadoRestaurante(Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

class Restaurante(base):
    __tablename__ = "restaurante"

    id = Column(String(100), primary_key=True, unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200), nullable=True)
    telefono = Column(String(10), nullable=False)
    direccion = Column(String(200), nullable=False)
    correo = Column(String(100), nullable=False)
    imagen = Column(String(200), nullable=False)
    fecha_creacion = Column(Date, nullable=False, default=date.today)
    fecha_finalizacion = Column(Date, nullable=False)
    estado = Column(SQLAlchemyEnum(EstadoRestaurante), nullable=False)

    # Relación con Usuario (uno a uno)
    id_usuario = Column(String(10), ForeignKey('usuario.documento'), nullable=False)
    usuario = relationship("Usuario", back_populates="restaurante")

    # Relación con Sucursal (uno a muchos)
    sucursales = relationship("Sucursal", back_populates="restaurante", cascade="all, delete-orphan")


class EstadoSucursal(Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

class Sucursal(base):
    __tablename__ = "sucursal"

    id = Column(String(100), primary_key=True, unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    ciudad = Column(String(100), nullable=False)
    telefono = Column(String(10), nullable=False)
    fecha_apertura = Column(Date, nullable=False, default=date.today)
    estado = Column(SQLAlchemyEnum(EstadoSucursal), nullable=False)
    administrador = Column(String(10), nullable=True)

    # Relación con Restaurante
    id_restaurante = Column(String(100), ForeignKey('restaurante.id'), nullable=False)
    restaurante = relationship("Restaurante", back_populates="sucursales")
    
class Producto(base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    imagen = Column(String(1000), nullable=True)
    disponibilidad = Column(Boolean, nullable=False)

    # Relación con Detalle_Pedido
    detalle_pedido = relationship("Detalle_Pedido", back_populates="producto", lazy="select")

    # Relación con Sucursal
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"), nullable=False)
    sucursal = relationship("Sucursal", back_populates="productos")

    # Relación con Categoria
    id_categoria = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    categoria = relationship("Categoria", back_populates="productos")
    
    
class EstadoPedido(str, Enum):
    ORDENADO = "ORDENADO"
    COMANDADO = "COMANDADO"
    LISTO = "LISTO"
    PAGADO = "PAGADO"
    
    
class Pedido(base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    fecha_pedido = Column(Date, nullable=False)
    hora_pedido = Column(Time, nullable=False)
    estado = Column(SQLAlchemyEnum(EstadoPedido), nullable=False, default=EstadoPedido.ORDENADO)
    total_pedido = Column(Float, nullable=True, default=0.0)
    nombre = Column(String, nullable=True)
    sucursal = Column(String, nullable=False)

    # Relación con Mesa
    id_mesa = Column(Integer, ForeignKey("mesa.id"), nullable=True)
    mesa = relationship("Mesa", back_populates="pedidos")

    # Relación con TipoPago
    id_tipo_pago = Column(Integer, ForeignKey("tipo_pago.id"), nullable=True)
    tipo_pago = relationship("TipoPago", back_populates="pedidos")

    # Relación con Detalle_Pedido
    detalle_pedido = relationship("DetallePedido", back_populates="pedido", lazy="select")
    

class DetallePedido(base):
    __tablename__ = "detalle_pedido"

    # Atributos de la tabla DetallePedido
    id_detalle_pedido = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    hora_detalle = Column(Time, nullable=False)
    descripcion = Column(String(200), nullable=True)
    precio_total = Column(Float, nullable=False)
    sucursal = Column(String, nullable=False)

    # Relación con Producto
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    producto = relationship("Producto", back_populates="detalle_pedido")

    # Relación con Pedido
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), nullable=False)
    pedido = relationship("Pedido", back_populates="detalle_pedido")



#----------------------mesas-----------------
class EstadoMesa(Enum):
    FISICA= "FISICA"
    RAPIDA = "RAPIDA"

class Mesa(base):
    __tablename__ = 'mesas'

    id= Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(SQLAlchemyEnum(EstadoMesa), nullable=False)
    id_sucursal = Column(String(100), ForeignKey("sucursal.id"), nullable=False)

    # Relación con la entidad Sucursal
    sucursal = relationship("Sucursal", back_populates="mesas")
    
    # Relación con la entidad Pedido
    pedidos = relationship("Pedido", back_populates="mesa")


#----------------------categoria----------------

class Categoria(base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    sucursal = Column(String(100), nullable=False)

    # Relación con la entidad Producto
    productos = relationship("Producto", back_populates="categoria", lazy="select")



#----------------------Tipos de pago----------------

class TipoPago(base):
    __tablename__ = 'tipo_pago'

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    sucursal = Column(String, nullable=False)

    # Relación con la entidad Pedido
    pedidos = relationship("Pedido", back_populates="tipo_pago", lazy="select")