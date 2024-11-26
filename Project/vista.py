from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from conexion import crear, get_db
from modelo import base, Usuario, RolUsuario, Restaurante, Sucursal
from schemas import UsuarioSchema, UsuarioCreateSchema, UsuarioLoginSchema, RestauranteCreateSchema, RestauranteSchema, RestauranteUpdateSchema, SucursalSchema
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base.metadata.create_all(bind=crear)

@app.post("/usuario", response_model=UsuarioSchema, status_code=201)
async def crear_usuario(usuario: UsuarioCreateSchema, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.post("/usuario/login", response_model=UsuarioSchema)
async def login(usuario: UsuarioLoginSchema, db: Session = Depends(get_db)):
    db_usuario = (
        db.query(Usuario)
        .filter(Usuario.correo == usuario.correo, Usuario.password == usuario.password)
        .first()
    )
    if not db_usuario:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    return db_usuario

@app.get("/usuario/correo/{correo}", response_model=str)
async def obtener_usuario_por_correo(correo: str, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario.documento

@app.get("/usuario/sucursal/{documento}", response_model=str)
async def obtener_sucursal_por_documento(documento: str, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.documento == documento).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario.sucursal

@app.get("/usuario/documento/{correo}", response_model=RolUsuario)
async def obtener_rol_por_correo(correo: str, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario.rol

@app.get("/usuario", response_model=List[UsuarioSchema])
async def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

@app.get("/usuario/{id}", response_model=UsuarioSchema)
async def obtener_usuario_por_id(id: str, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.documento == id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.get("/usuario/nombre/{id}", response_model=str)
async def obtener_nombre_por_documento(id: str, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.documento == id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario.nombre

@app.put("/usuario/{id}", response_model=UsuarioSchema)
async def actualizar_usuario(id: str, usuario: UsuarioCreateSchema, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.documento == id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.delete("/usuario/{id}", status_code=204)
async def eliminar_usuario(id: str, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.documento == id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_usuario)
    db.commit()

@app.post("/restaurante", response_model=RestauranteSchema, status_code=201)
async def crear_restaurante(restaurante: RestauranteCreateSchema, db: Session = Depends(get_db)):
    nuevo_restaurante = Restaurante(**restaurante.dict())
    db.add(nuevo_restaurante)
    db.commit()
    db.refresh(nuevo_restaurante)
    return nuevo_restaurante

@app.get("/restaurante", response_model=List[RestauranteSchema])
async def listar_restaurantes(db: Session = Depends(get_db)):
    restaurantes = db.query(Restaurante).all()
    return restaurantes

@app.get("/restaurante/{id}", response_model=str)
async def obtener_restaurante_por_id(id: str, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.id == id).first()
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    return restaurante.nombre

@app.get("/restaurante/id_usuario/{id_usuario}", response_model=str)
async def obtener_id_usuario(id_usuario: str, db: Session = Depends(get_db)):
    restaurante = db.query(Restaurante).filter(Restaurante.id_usuario == id_usuario).first()
    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado para este usuario")
    return restaurante.id

@app.put("/restaurante/{id}", response_model=RestauranteSchema)
async def actualizar_restaurante(
    id: str, restaurante: RestauranteUpdateSchema, db: Session = Depends(get_db)
):
    db_restaurante = db.query(Restaurante).filter(Restaurante.id == id).first()
    if not db_restaurante:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    
    for key, value in restaurante.dict(exclude_unset=True).items():
        setattr(db_restaurante, key, value)
    
    db.commit()
    db.refresh(db_restaurante)
    return db_restaurante

@app.delete("/restaurante/{id}", status_code=204)
async def eliminar_restaurante(id: str, db: Session = Depends(get_db)):
    db_restaurante = db.query(Restaurante).filter(Restaurante.id == id).first()
    if not db_restaurante:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    db.delete(db_restaurante)
    db.commit()

@app.post("/sucursal", response_model=SucursalSchema, status_code=201)
async def crear_sucursal(sucursal: SucursalSchema, db: Session = Depends(get_db)):
    nueva_sucursal = Sucursal(**sucursal.dict())
    db.add(nueva_sucursal)
    db.commit()
    db.refresh(nueva_sucursal)
    return nueva_sucursal


@app.get("/sucursal/{id}", response_model=SucursalSchema)
async def obtener_sucursal(id: str, db: Session = Depends(get_db)):
    sucursal = db.query(Sucursal).filter(Sucursal.id == id).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal


@app.get("/sucursal/restaurante/{id_restaurante}", response_model=List[SucursalSchema])
async def obtener_sucursales_por_restaurante(id_restaurante: str, db: Session = Depends(get_db)):
    sucursales = db.query(Sucursal).filter(Sucursal.id_restaurante == id_restaurante).all()
    if not sucursales:
        raise HTTPException(status_code=404, detail="No se encontraron sucursales para este restaurante")
    return sucursales


@app.put("/sucursal/{id}", response_model=SucursalSchema)
async def actualizar_sucursal(id: str, sucursal: SucursalSchema, db: Session = Depends(get_db)):
    db_sucursal = db.query(Sucursal).filter(Sucursal.id == id).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    for key, value in sucursal.dict(exclude_unset=True).items():
        setattr(db_sucursal, key, value)
    
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal


@app.delete("/sucursal/{id}", status_code=204)
async def eliminar_sucursal(id: str, db: Session = Depends(get_db)):
    db_sucursal = db.query(Sucursal).filter(Sucursal.id == id).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    db.delete(db_sucursal)
    db.commit()


@app.get("/sucursal/administrador/{administrador}", response_model=str)
async def obtener_sucursal_por_administrador(administrador: str, db: Session = Depends(get_db)):
    sucursal = db.query(Sucursal).filter(Sucursal.administrador == administrador).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="No se encontró una sucursal para este administrador")
    return sucursal.id




'''@app.get("/productos/{nit}")
def obtener_productos( nit: str, db: Session = Depends(get_db)):
    # Consulta para obtener todos los productos
    sql = text("SELECT * FROM producto where id_sucursal = :nit")
    resultados = db.execute(sql,{"nit": nit}).fetchall()  # Obtiene todos los productos

    # Convierte los resultados en una lista de diccionarios
    productos = [{
        "id": resultado.id,
        "nombre": resultado.nombre,
        "precio": resultado.precio,
        "id_categoria": resultado.id_categoria,
        "id_sucursal":resultado.id_sucursal
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
    sql = text("SELECT * FROM mesa WHERE nombre = :nombre and id_sucursal = :id_sucursal")
    nombre_existente = db.execute(sql, {'nombre': mesa.nombre, 'id_sucursal': mesa.id_sucursal}).fetchone()

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

    sql = text("SELECT * FROM producto WHERE nombre = :nombre and id_sucursal = :id_sucursal")
    id_existente = db.execute(sql, {'nombre': producto.nombre,'id_sucursal': producto.id_sucursal}).fetchone()

    if id_existente:
        raise HTTPException(status_code=400, detail="El id de este producto ya existe en esta sucursal")

    sql1 = text("""
    INSERT INTO producto (id, nombre, precio, id_categoria,id_sucursal) 
    VALUES (:id, :nombre, :precio, :id_categoria, :id_sucursal)
    """)

    values = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'id_categoria': producto.id_categoria,
        'id_sucursal' : producto.id_sucursal
    }

    db.execute(sql1, values)
    db.commit()

    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "id_categoria": producto.id_categoria,
        "id_sucursal": producto.id_sucursal
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
async def actualizar_producto(producto: proedi, db: Session = Depends(get_db)):

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




@app.post("/insertardos")
async def registrar_cliente(producto: pro, db: Session = Depends(get_db)):

    # Verificar si el producto ya existe
    sql = text("SELECT * FROM producto WHERE nombre = :nombre AND id_sucursal = :id_sucursal")
    id_existente = db.execute(sql, {'nombre': producto.nombre, 'id_sucursal': producto.id_sucursal}).fetchone()

    if id_existente:
        raise HTTPException(status_code=400, detail="El id de este producto ya existe en esta sucursal")
    
    # Validar el tipo de archivo
    #if pro.imagen.content_type not in ["image/jpeg", "image/png"]:
        #raise HTTPException(status_code=400, detail="Formato de archivo no soportado")

    # Ruta de guardado del archivo
    folder_path = "imagenes"
    os.makedirs(folder_path, exist_ok=True)
    
    # Generar un nombre único para evitar sobrescribir archivos
    file_location = os.path.join(folder_path, f"{pro.imagen}_{pro.imagen.filename}")

    # Guarda el archivo en el servidor
    with open(file_location, "wb") as buffer:
        buffer.write(await pro.imagen.read())

    # Inserta el producto en la base de datos
    sql1 = text("""
    INSERT INTO producto (id, nombre, precio, id_categoria, id_sucursal, imagen) 
    VALUES (:id, :nombre, :precio, :id_categoria, :id_sucursal, :imagen)
    """)

    values = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'id_categoria': producto.id_categoria,
        'id_sucursal': producto.id_sucursal,
        'imagen': producto.imagen  
    }

    db.execute(sql1, values)
    db.commit()

    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "id_categoria": producto.id_categoria,
        "id_sucursal": producto.id_sucursal,
        "imagen": producto.imagen  
    }'''
