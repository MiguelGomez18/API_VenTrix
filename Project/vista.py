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
from schemas import Categoria as cat
from schemas import Mesas as me
from schemas import MesasActualizar as meas
from schemas import Sucursal as su
from schemas import TipoPago as TipoPago
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

@app.get("/propietario/documento/", response_model=list[str])
async def getidd(db:Session=Depends(get_db)):
    documentos=db.query(RegistroPropietario.documento).all()
    return[doc[0] for doc in documentos]


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

@app.get("/mesas/{nit}")
async def obtener_mesas(nit: str,db: Session = Depends(get_db)):
    # Consulta para obtener todas las mesas
    sql = text("SELECT * FROM mesa where estado='Fisica' AND id_sucursal = :nit")
    resultados = db.execute(sql, {"nit": nit}).fetchall()
  # Obtiene todas las mesas

    # Convierte los resultados en una lista de diccionarios
    mesas = [{
        "id": resultado.id,
        "nombre": resultado.nombre,
        "estado": resultado.estado,
        "id_sucursal": resultado.id_sucursal
    } for resultado in resultados]

    return mesas

@app.get("/mesarapida/{nit}")
async def obtener_mesa_rapida(nit: str,db: Session = Depends(get_db)):
    # Consulta para obtener todas las mesas
    sql = text("SELECT * FROM mesa where estado='Rapida' AND id_sucursal = :nit")
    resultados = db.execute(sql, {"nit": nit}).fetchall()
  # Obtiene todas las mesas

    # Convierte los resultados en una lista de diccionarios
    mesas = [{
        "id": resultado.id,
        "nombre": resultado.nombre,
        "estado": resultado.estado,
        "id_sucursal": resultado.id_sucursal
    } for resultado in resultados]

    return mesas

@app.get("/sucursales/{documento}")
def obtener_sucursales(documento: int, db: Session = Depends(get_db)):
    # Consulta para verificar si existen sucursales con el documento dado
    sql_existencia = text("SELECT 1 FROM sucursal WHERE documento = :documento LIMIT 1")
    documento_existente = db.execute(sql_existencia, {'documento': documento}).fetchone()

    if documento_existente:
        # Consulta para obtener todas las sucursales con el documento dado
        sql_sucursales = text("SELECT * FROM sucursal WHERE documento = :documento")
        resultados = db.execute(sql_sucursales, {'documento': documento}).fetchall()

        # Convierte los resultados en una lista de diccionarios
        sucursales = [{
            "nit": resultado.nit,
            "rut": resultado.rut,
            "nombre": resultado.nombre,
            "direccion": resultado.direccion,
            "telefono": resultado.telefono,
            "correo": resultado.correo,
            "documento": resultado.documento
        } for resultado in resultados]

        return sucursales
    
    else:
        raise HTTPException(status_code=400, detail="No se encontraron sucursales con el documento proporcionado.")

@app.get("/correo/{correo}")
def obtener_sucursal(correo: str, db: Session = Depends(get_db)):
    # Verificar si el correo existe
    sql_existencia = text("SELECT 1 FROM propietario WHERE correo = :correo LIMIT 1")
    correo_existente = db.execute(sql_existencia, {'correo': correo}).fetchone()

    if correo_existente:
        # Consulta para obtener la primera sucursal asociada al correo dado
        sql_propietario = text("SELECT documento FROM propietario WHERE correo = :correo LIMIT 1")
        resultado = db.execute(sql_propietario, {'correo': correo}).fetchone()

        if resultado:
            return resultado.documento  # Devuelve solo el documento como un valor simple

        raise HTTPException(status_code=404, detail="No se encontraron sucursales para el correo proporcionado.")
    
    else:
        raise HTTPException(status_code=400, detail="Correo no encontrado.")

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

@app.post("/registro_sucursal")
async def registrar_propietario(sucursal: su, db:Session = Depends(get_db)):
    nit_user = db.query(RegistroSucursal).filter(RegistroSucursal.documento == sucursal.nit).first()
    if nit_user:
        raise HTTPException(status_code=400, detail="El nit de esta Sucursal ya existe")

    nueva_sucursal = RegistroSucursal(
        nit=sucursal.nit,
        rut=sucursal.rut,
        nombre=sucursal.nombre,
        direccion=sucursal.direccion,
        telefono=sucursal.telefono,
        correo=sucursal.correo,
        documento=sucursal.documento
    )
    db.add(nueva_sucursal)
    db.commit()
    db.refresh(nueva_sucursal)
    
    return {
        "nit": nueva_sucursal.nit,
        "rut": nueva_sucursal.rut,
        "nombre": nueva_sucursal.nombre,
        "direccion": nueva_sucursal.direccion,
        "telefono": nueva_sucursal.telefono,
        "correo": nueva_sucursal.correo,
        "documento": nueva_sucursal.documento,
    }

@app.post("/registrar_categoria")
async def registrar_categoria(categoria: cat, db: Session = Depends(get_db)):
    sql = text("SELECT * FROM categoria WHERE nombre = :nombre")
    nombre_existente = db.execute(sql, {'nombre': categoria.nombre}).fetchone()

    if nombre_existente:
        raise HTTPException(status_code=400, detail="El nombre de la categoría ya existe")
    
    sqlingresar = text("""
                       INSERT INTO categoria (nombre)
                       values (:nombre)
                       """)
    
    values = {
        'nombre': categoria.nombre
    }
    
    result = db.execute(sqlingresar, values)
    db.commit()
    
    # Obtener el id generado automáticamente
    nuevo_id = result.lastrowid
    
    return {
        "id": nuevo_id,
        "nombre": categoria.nombre
    }

@app.post("/registrar_mesa")
async def registrar_mesa(mesa: me, db: Session = Depends(get_db)):
    # Verificar si ya existe una mesa con el mismo nombre
    sql = text("SELECT * FROM mesa WHERE nombre = :nombre")
    nombre_existente = db.execute(sql, {'nombre': mesa.nombre}).fetchone()

    if nombre_existente:
        raise HTTPException(status_code=400, detail="El nombre de la mesa ya existe")

    # Insertar nueva mesa
    sqlingresar = text("""
                        INSERT INTO mesa (nombre,estado, id_sucursal)
                        VALUES (:nombre, :estado, :id_sucursal)
                       """)

    values = {
        'nombre': mesa.nombre,
        'estado': mesa.estado,
        'id_sucursal': mesa.id_sucursal,
    }

    result = db.execute(sqlingresar, values)
    db.commit()

    # Obtener el ID generado automáticamente
    nuevo_id = result.lastrowid

    return {
        "id": nuevo_id,
        "nombre": mesa.nombre,
        "estado": mesa.estado,
        "id_sucursal": mesa.id_sucursal
    }


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

@app.put("/actualizar_mesa/")
async def actualizar_mesa(mesa: meas, db: Session = Depends(get_db)):

    # Verifica si la mesa con el ID proporcionado existe
    sql = text("SELECT * FROM mesa WHERE id = :id")
    id_existente = db.execute(sql, {'id': mesa.id}).fetchone()

    if not id_existente:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")

    # Actualiza los datos de la mesa
    sql1 = text("""
    UPDATE mesa 
    SET nombre = :nombre
    WHERE id = :id
    """)

    values = {
        'id': mesa.id,
        'nombre': mesa.nombre,
    }

    db.execute(sql1, values)
    db.commit()

    return {
        "id": mesa.id,
        "nombre": mesa.nombre
    }

@app.put("/actualizar_categoria/")
async def actualizar_categoria(categoria: cat, db: Session = Depends(get_db)):

    # Verifica si la categoría con el ID proporcionado existe
    sql = text("SELECT * FROM categoria WHERE id = :id")
    id_existente = db.execute(sql, {'id': categoria.id}).fetchone()

    if not id_existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Actualiza los datos de la categoría
    sql1 = text("""
    UPDATE categoria 
    SET nombre = :nombre
    WHERE id = :id
    """)

    values = {
        'id': categoria.id,
        'nombre': categoria.nombre
    }

    db.execute(sql1, values)
    db.commit()

    return {
        "id": categoria.id,
        "nombre": categoria.nombre
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

@app.delete("/eliminar_mesa/{id}")
async def eliminar_mesa(id: int, db: Session = Depends(get_db)):

    # Verifica si la mesa con el ID proporcionado existe
    sql = text("SELECT * FROM mesa WHERE id = :id")
    id_existente = db.execute(sql, {'id': id}).fetchone()

    if not id_existente:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")

    # Elimina la mesa
    sql1 = text("""
    DELETE FROM mesa
    WHERE id = :id
    """)

    db.execute(sql1, {'id': id})
    db.commit()

    return {
        "detail": "Mesa eliminada exitosamente"
    }


@app.delete("/eliminar_categoria/{id}")
async def eliminar_categoria(id: int, db: Session = Depends(get_db)):

    # Verifica si la categoría con el ID proporcionado existe
    sql = text("SELECT * FROM categoria WHERE id = :id")
    id_existente = db.execute(sql, {'id': id}).fetchone()

    if not id_existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Elimina la categoría
    sql1 = text("""
    DELETE FROM categoria
    WHERE id = :id
    """)

    db.execute(sql1, {'id': id})
    db.commit()

    return {
        "detail": "Categoría eliminada exitosamente"
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

@app.get("/ventas")
def obtener_ventas(db: Session = Depends(get_db)):
    # Ajusta la consulta SQL según la estructura de tu base de datos
    sql = text("""
        SELECT 
            v.fecha_hora, 
            v.cantidad, 
            v.total 
        FROM 
            venta v
    """)
    resultados = db.execute(sql).fetchall()

    # Procesar los resultados
    ventas = [{
        "fecha_hora": resultado.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),  # Convertir a string si es necesario
        "cantidad": resultado.cantidad,
        "total": resultado.total,
    } for resultado in resultados]

    return ventas

@app.get("/mayorproductodia")
def obtener_ventas(db: Session = Depends(get_db)):
    # Consulta SQL ajustada para obtener los productos más vendidos
    sql = text("""
        SELECT 
            p.id AS id_producto, 
            p.nombre, 
            SUM(v.cantidad) AS cantidad
        FROM 
            venta v
        JOIN 
            producto p ON v.id_producto = p.id
        GROUP BY 
            p.id, p.nombre
        ORDER BY 
            cantidad DESC
        LIMIT 5
    """)
    resultados = db.execute(sql).fetchall()

    # Procesar los resultados
    ventas = [{
        "id_producto": resultado.id_producto,
        "nombre": resultado.nombre,
        "cantidad": resultado.cantidad,
    } for resultado in resultados]

    return ventas
@app.get("/productocategoria") 
def obtener_ventas(db: Session = Depends(get_db)):
    try:
        # Consulta SQL ajustada para obtener los productos más vendidos, incluyendo la categoría
        sql = text(""" 
            SELECT 
                p.id AS id_producto, 
                p.nombre, 
                SUM(v.cantidad) AS cantidad,
                c.nombre AS categoria  -- Cambiado para referirse a la tabla 'categoria'
            FROM 
                venta v
            JOIN 
                producto p ON v.id_producto = p.id
            JOIN 
                categoria c ON p.id_categoria = c.id  -- Agregar JOIN con la tabla categoria
            GROUP BY 
                p.id, p.nombre, c.nombre  -- Cambiado para usar 'c.nombre' en lugar de 'p.categoria'
            ORDER BY 
                cantidad DESC
            LIMIT 5
        """)
        resultados = db.execute(sql).fetchall()

        # Procesar los resultados
        ventas = [{
            "id_producto": resultado.id_producto,
            "nombre": resultado.nombre,
            "cantidad": resultado.cantidad,
            "categoria": resultado.categoria,  # Incluir la categoría
        } for resultado in resultados]

        return ventas
    except Exception as e:
        return {"error": str(e)}, 500


#-----------------------------pagos---------------------------
@app.get("/tipo_pago")
async def obtener_tipos_pago(db: Session = Depends(get_db)):
   
    sql = text("SELECT * FROM tipo_pago")
    resultados = db.execute(sql).fetchall() 

  
    tipos_pago = [{
        "id": resultado.id,
        "descripcion": resultado.descripcion,
    } for resultado in resultados]

    return tipos_pago

@app.get("/tipo_pago/{id}")
async def obtener_tipo_pago(id: int, db: Session = Depends(get_db)):
    
    sql = text("SELECT * FROM tipo_pago WHERE id = :id")
    resultado = db.execute(sql, {"id": id}).fetchone()  

    if not resultado:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")

    tipo_pago = {
        "id": resultado.id,
        "descripcion": resultado.descripcion
    }

    return tipo_pago

@app.post("/registrar_tipo_pago")
async def registrar_tipo_pago(tipo_pago: TipoPago, db: Session = Depends(get_db)):
   
    sql = text("SELECT * FROM tipo_pago WHERE id = :id")
    id_existente = db.execute(sql, {'id': tipo_pago.id}).fetchone()

    if id_existente:
        raise HTTPException(status_code=400, detail="El id de este tipo de pago ya existe")

    
    sql1 = text("""
    INSERT INTO tipo_pago (id, descripcion) 
    VALUES (:id, :descripcion)
    """)

    values = {
        'id': tipo_pago.id,
        'descripcion': tipo_pago.descripcion
    }

    db.execute(sql1, values)
    db.commit()

    return {
        "id": tipo_pago.id,
        "descripcion": tipo_pago.descripcion
    }


@app.put("/tipo_pago/{id}")
async def actualizar_tipo_pago(id: int, tipo_pago: TipoPago, db: Session = Depends(get_db)):
    
    sql_select = text("SELECT * FROM tipo_pago WHERE id = :id")
    resultado = db.execute(sql_select, {"id": id}).fetchone()

    if not resultado:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")

 
    sql_update = text("UPDATE tipo_pago SET descripcion = :descripcion WHERE id = :id")
    db.execute(sql_update, {"descripcion": tipo_pago.descripcion, "id": id})
    db.commit()

    return {"message": "Tipo de pago actualizado correctamente"}


@app.delete("/tipo_pago/{id}")
async def eliminar_tipo_pago(id: int, db: Session = Depends(get_db)):
    
    sql_select = text("SELECT * FROM tipo_pago WHERE id = :id")
    resultado = db.execute(sql_select, {"id": id}).fetchone()

    if not resultado:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")

    
    sql_delete = text("DELETE FROM tipo_pago WHERE id = :id")
    db.execute(sql_delete, {"id": id})
    db.commit()

    return {"message": "Tipo de pago eliminado correctamente"}
