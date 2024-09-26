from sqlalchemy import String,Integer,Column,ForeignKey
from conexion import base 
from sqlalchemy.orm import relationship
from datetime import datetime

class RegistroPropietario(base):
    __tablename__="propietario"
    documento = Column(Integer, primary_key=True, index=True, unique=True)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(60), unique=True, nullable=False)
    password=Column(String(100), nullable=False)


class RegistroSucursal(base):
    __tablename__="sucursal"
    nit = Column(String(10),primary_key = True,index = True)
    rut = Column(String(10),nullable = False)
    nombre = Column(String(50),nullable = False)
    direccion = Column(String(100),nullable = False)
    telefono = Column(String(10),nullable = False)
    correo = Column(String(60),unique=True)
    documento = Column(Integer, ForeignKey('propietario.documento'))

