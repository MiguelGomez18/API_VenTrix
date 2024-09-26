import bcrypt
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from conexion import crear,get_db
from modelo import base,RegistroPropietario,RegistroSucursal
from schemas import Sucursal as su
from schemas import Propietario as pr
from schemas import Login 
from schemas import Producto as pro
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

base.metadata.create_all(bind=crear)

@app.post("/registros_tiendas", response_model=su)
async def registrar_sucursal(tiendamodel:su,db:Session=Depends(get_db)):
    datos=RegistroSucursal(**tiendamodel.dict())
    db.add(datos)
    db.commit()
    db.refresh(datos)
    return datos

@app.get("/propietario/documento/", response_model=list[str])
async def getidd(db:Session=Depends(get_db)):
    documentos=db.query(RegistroPropietario.documento).all()
    return[doc[0] for doc in documentos]


@app.post("/registro_propietario")
async def registrar_propietario(propietario: pr, db:Session = Depends(get_db)):
    documento_user = db.query(RegistroPropietario).filter(RegistroPropietario.documento == propietario.documento).first()
    if documento_user:
        raise HTTPException(status_code=400, detail="El documento de este Propietario ya existe")

    encriptacion = bcrypt.hashpw(propietario.password.encode('utf-8'), bcrypt.gensalt())

    nuevo_propietario = RegistroPropietario(
        documento=propietario.documento,
        nombre=propietario.nombre,
        correo=propietario.correo,
        password=encriptacion.decode('utf-8')
    )
    db.add(nuevo_propietario)
    db.commit()
    db.refresh(nuevo_propietario)
    
    return {
        "documento": nuevo_propietario.documento,
        "nombre": nuevo_propietario.nombre,
        "correo": nuevo_propietario.correo
    }

@app.post("/login")
async def login(propietario:Login,db:Session=Depends(get_db)):
    db_user=db.query(RegistroPropietario).filter(RegistroPropietario.correo==propietario.correo).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Correo no existe")
    if not bcrypt.checkpw(propietario.password.encode('utf-8'),db_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    return{
        "mensaje":"Inicio de Sesion OK",
        "nombre":db_user.nombre,
        "correo":db_user.correo
    }

@app.get("/productos")
def obtener_productos(db: Session = Depends(get_db)):
    # Consulta para obtener todos los productos
    sql = text("SELECT * FROM producto")
    resultados = db.execute(sql).fetchall()  # Obtiene todos los productos

    # Convierte los resultados en una lista de diccionarios
    productos = [{
        "id": resultado.id,
        "nombre": resultado.nombre,
        "precio": resultado.precio,
        "id_categoria": resultado.id_categoria
    } for resultado in resultados]

    return productos

@app.get("/categoria")
def obtener_productos(db: Session = Depends(get_db)):
    # Consulta para obtener todos las categorias
    sql = text("SELECT * FROM categoria")
    resultados = db.execute(sql).fetchall()  # Obtiene todos las categorias

    # Convierte los resultados en una lista de diccionarios
    categorias = [{
        "id": resultado.id,
        "nombre": resultado.nombre,
    } for resultado in resultados]

    return categorias

@app.post("/registrar_producto")
async def registrar_producto(producto: pro, db: Session = Depends(get_db)):

    sql = text("SELECT * FROM producto WHERE id = :id")
    id_existente = db.execute(sql, {'id': producto.id}).fetchone()

    if id_existente:
        raise HTTPException(status_code=400, detail="El id de este producto ya existe")

    sql1 = text("""
    INSERT INTO producto (id, nombre, precio, id_categoria) 
    VALUES (:id, :nombre, :precio, :id_categoria)
    """)

    values = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'id_categoria': producto.id_categoria
    }

    db.execute(sql1, values)
    db.commit()

    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "id_categoria": producto.id_categoria
    }


@app.put("/actualizar_producto/")
async def actualizar_producto(producto: pro, db: Session = Depends(get_db)):

    sql1 = text("""
    UPDATE producto 
    SET nombre = :nombre, 
        precio = :precio, 
        id_categoria = :id_categoria
    WHERE id = :id
    """)

    set = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'id_categoria': producto.id_categoria
    }

    db.execute(sql1, set)
    db.commit()

    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "id_categoria": producto.id_categoria
    }

@app.delete("/eliminar_producto/{id}")
async def eliminar_producto(id: int, db: Session = Depends(get_db)):

    sql = text("""
    DELETE FROM producto
    WHERE id = :id
    """)

    db.execute(sql, {'id': id})
    db.commit()

    return {
        "detail": "Producto eliminado exitosamente"
    }
