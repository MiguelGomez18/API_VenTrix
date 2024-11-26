from sqlalchemy import Column, String, Enum as SQLAlchemyEnum, Date, ForeignKey
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

class Usuario(base):
    __tablename__ = "usuario"

    documento = Column(String(10), primary_key=True, unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(100), nullable=False)
    password = Column(String(50), nullable=False)
    rol = Column(SQLAlchemyEnum(RolUsuario), nullable=False)
    fecha_creacion = Column(Date, nullable=False)
    sucursal = Column(String(100), nullable=True)
    
    # Relación con la tabla Restaurante
    restaurantes = relationship("Restaurante", back_populates="usuario")

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
    fecha_creacion = Column(Date, nullable=False)
    fecha_finalizacion = Column(Date, nullable=False)
    estado = Column(SQLAlchemyEnum(EstadoRestaurante), nullable=False)

    # Relación con Usuario
    id_usuario = Column(String(10), ForeignKey('usuario.documento'), nullable=False)
    usuario = relationship("Usuario", back_populates="restaurantes")

    # Relación con Sucursal
    sucursales = relationship("Sucursal", back_populates="restaurante")

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
    fecha_apertura = Column(Date, nullable=False)
    estado = Column(SQLAlchemyEnum(EstadoSucursal), nullable=False)
    administrador = Column(String(10), nullable=True)

    # Relación con Restaurante
    id_restaurante = Column(String(100), ForeignKey('restaurante.id'), nullable=False)
    restaurante = relationship("Restaurante", back_populates="sucursales")