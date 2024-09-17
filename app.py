from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exists

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/efi_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Marca, Fabricante, Modelo, Caracteristica, Equipo, Proveedor, Stock, Accesorio
from flask import request, redirect, url_for



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lista_fabricantes', methods=['GET', 'POST'])
def lista_fabricantes():
    fabricantes = Fabricante.query.all()
    if request.method == 'POST':
        # Crear un nuevo fabricante
        nombre = request.form['nombre']
        pais_origen = request.form['pais_origen']

        # Comprobar si el nombre del fabricante ya existe
        fabricante_existente = Fabricante.query.filter_by(nombre=nombre).first()
        if fabricante_existente:
            # Mostrar mensaje de error al usuario (por ejemplo, con Flask-WTF)
            return render_template('lista_fabricantes.html', fabricantes=fabricantes, error="Ya existe un fabricante con ese nombre")
        
        nuevo_fabricante = Fabricante(nombre=nombre, pais_origen=pais_origen)
        db.session.add(nuevo_fabricante)
        db.session.commit()
        return redirect(url_for('lista_fabricantes'))
    else:
        fabricantes = Fabricante.query.all()
        return render_template('lista_fabricantes.html', fabricantes=fabricantes)

@app.route('/fabricante/<id>/editar', methods=['GET', 'POST'])
def editar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_pais_origen = request.form['pais_origen']

        # Comprobar si el nombre del fabricante ya existe, excluyendo el actual
        fabricante_existente = Fabricante.query.filter(Fabricante.nombre == nuevo_nombre, Fabricante.id != id).first()
        if fabricante_existente:
            error = "El nombre del fabricante ya existe. Por favor, elige otro."
            return render_template('editar_fabricante.html', fabricante=fabricante, error=error)
        
        # Actualizar fabricante
        fabricante.nombre = nuevo_nombre
        fabricante.pais_origen = nuevo_pais_origen
        try:
            db.session.commit()
            return redirect(url_for('lista_fabricantes'))
        except IntegrityError:
            db.session.rollback()  # Revertir la transacción
            error = "No se pudo guardar el fabricante. Inténtalo de nuevo."
            return render_template('editar_fabricante.html', fabricante=fabricante, error=error)
    
    return render_template('editar_fabricante.html', fabricante=fabricante)

@app.route('/fabricante/<id>/eliminar', methods=['POST'])
def eliminar_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    db.session.delete(fabricante)
    db.session.commit()
    return redirect(url_for('lista_fabricantes'))


@app.route('/lista_marcas', methods=['GET', 'POST'])
def lista_marcas():
    marcas = Marca.query.all()
    fabricantes = Fabricante.query.all()  # Asegúrate de que los fabricantes estén disponibles siempre
    if request.method == 'POST':
        nombre = request.form['nombre']
        fabricante_id = request.form['fabricante_id']

        # Comprobar si el nombre de la marca ya existe
        marca_existente = Marca.query.filter_by(nombre=nombre).first()
        if marca_existente:
            # Mostrar mensaje de error al usuario
            return render_template('lista_marcas.html', marcas=marcas, fabricantes=fabricantes, fabricante_id=fabricante_id, error="Ya existe una marca con ese nombre")

        nueva_marca = Marca(nombre=nombre, fabricante_id=fabricante_id)
        db.session.add(nueva_marca)
        db.session.commit()
        return redirect(url_for('lista_marcas'))
    else:
        return render_template('lista_marcas.html', marcas=marcas, fabricantes=fabricantes)

@app.route("/marca/<id>/editar", methods=['POST', 'GET'])
def editar_marca(id):
    marca = Marca.query.get_or_404(id)
    fabricantes = Fabricante.query.all()  # Obtener la lista de fabricantes

    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        marca.fabricante_id = request.form['fabricante_id']  # Actualizar el fabricante si es necesario

        try:
            db.session.commit()
            return redirect(url_for('lista_marcas'))
        except IntegrityError:
            db.session.rollback()  # Revertir la transacción en caso de error
            error = "El nombre de la marca ya existe. Por favor, elige otro."
            return render_template('editar_marca.html', marca=marca, fabricantes=fabricantes, error=error)
    
    return render_template('editar_marca.html', marca=marca, fabricantes=fabricantes)


@app.route('/lista_modelos', methods=['GET', 'POST'])
def lista_modelos():
    modelos = Modelo.query.all()
    marcas = Marca.query.all()  # Cargar todas las marcas para usarlas en el formulario

    if request.method == 'POST':
        nombre = request.form['nombre']
        marca_id = request.form['marca_id']

        # Comprobar si el nombre del modelo ya existe
        modelo_existente = Modelo.query.filter_by(nombre=nombre).first()
        if modelo_existente:
            # Mostrar mensaje de error si el modelo ya existe
            return render_template('lista_modelos.html', modelos=modelos, marcas=marcas, error="Ya existe un modelo con ese nombre")

        nuevo_modelo = Modelo(nombre=nombre, marca_id=marca_id)
        db.session.add(nuevo_modelo)
        db.session.commit()
        return redirect(url_for('lista_modelos'))

    return render_template('lista_modelos.html', modelos=modelos, marcas=marcas)

@app.route('/modelo/<id>/editar', methods=['GET', 'POST'])
def editar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    marcas = Marca.query.all()  # Cargar todas las marcas para usarlas en el formulario

    if request.method == 'POST':
        modelo.nombre = request.form['nombre']
        modelo.marca_id = request.form['marca_id']

        try:
            db.session.commit()
            return redirect(url_for('lista_modelos'))
        except IntegrityError:
            db.session.rollback()
            error = "El nombre del modelo ya existe. Por favor, elige otro."
            return render_template('editar_modelo.html', modelo=modelo, marcas=marcas, error=error)

    return render_template('editar_modelo.html', modelo=modelo, marcas=marcas)

@app.route('/modelo/<id>/eliminar', methods=['POST'])
def eliminar_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    db.session.delete(modelo)
    db.session.commit()
    return redirect(url_for('lista_modelos'))

@app.route('/lista_caracteristicas', methods=['GET', 'POST'])
def lista_caracteristicas():
    caracteristicas = Caracteristica.query.all()
    modelos = Modelo.query.all()
    
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        modelo_id = request.form['modelo_id']

        # Comprobar si la característica ya existe para ese modelo y tipo
        caracteristica_existente = Caracteristica.query.filter_by(tipo=tipo, modelo_id=modelo_id).first()
        if caracteristica_existente:
            return render_template('lista_caracteristicas.html', caracteristicas=caracteristicas, modelos=modelos, error="Ya existe una característica con ese tipo para el modelo seleccionado")

        nueva_caracteristica = Caracteristica(tipo=tipo, descripcion=descripcion, modelo_id=modelo_id)
        db.session.add(nueva_caracteristica)
        db.session.commit()
        return redirect(url_for('lista_caracteristicas'))
    else:
        caracteristicas = Caracteristica.query.all()
        return render_template('lista_caracteristicas.html', caracteristicas=caracteristicas, modelos=modelos)

@app.route('/caracteristica/<id>/editar', methods=['GET', 'POST'])
def editar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    modelos = Modelo.query.all()
    
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        modelo_id = request.form['modelo_id']

        # Comprobar si la nueva combinación de tipo y modelo ya existe
        caracteristica_existente = Caracteristica.query.filter_by(tipo=tipo, modelo_id=modelo_id).first()
        if caracteristica_existente and caracteristica_existente.id != id:
            error = "Ya existe una característica con ese tipo para el modelo seleccionado"
            return render_template('editar_caracteristica.html', caracteristica=caracteristica, modelos=modelos, error=error)
        
        caracteristica.tipo = tipo
        caracteristica.descripcion = descripcion
        caracteristica.modelo_id = modelo_id

        try:
            db.session.commit()
            return redirect(url_for('lista_caracteristicas'))
        except IntegrityError:
            db.session.rollback()
            error = "Error al editar la característica. Por favor, intenta de nuevo."
            return render_template('editar_caracteristica.html', caracteristica=caracteristica, modelos=modelos, error=error)
    
    return render_template('editar_caracteristica.html', caracteristica=caracteristica, modelos=modelos)

@app.route('/caracteristica/<int:id>/eliminar', methods=['POST'])
def eliminar_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    db.session.delete(caracteristica)
    db.session.commit()
    return redirect(url_for('lista_caracteristicas'))

@app.route('/lista_equipos', methods=['GET', 'POST'])
def lista_equipos():
    modelos = Modelo.query.all()
    marcas = Marca.query.all() 
    equipos = Equipo.query.all()
    if request.method == 'POST':
        marca_id = request.form.get('marca_id')
        modelo_id = request.form.get('modelo_id')
        costo = request.form.get('costo')

        # Comprobar si el modelo del equipo ya existe
        equipo_existente = Equipo.query.filter_by(modelo_id = modelo_id).first()
        if equipo_existente:
            # Mostrar mensaje de error si el equipo ya existe
            return render_template('lista_equipos.html', equipos=equipos,modelos=modelos, marcas=marcas, error="Ya existe un equipo con ese modelo")

        nuevo_equipo = Equipo(
            marca_id=marca_id,
            modelo_id=modelo_id,
            costo=costo
        )
        db.session.add(nuevo_equipo)
        db.session.commit()
        return redirect(url_for('lista_equipos'))
    
    else:
        modelos = Modelo.query.all()
        marcas = Marca.query.all() 
        return render_template('lista_equipos.html', equipos=equipos, modelos=modelos, marcas=marcas)


@app.route('/editar_equipo/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    modelos = Modelo.query.all()
    marcas = Marca.query.all()

    if request.method == 'POST':
        nuevo_marca_id = request.form['marca_id']
        nuevo_modelo_id = request.form['modelo_id']
        nuevo_costo = request.form['costo']

        # Comprobar si el modelo del equipo ya existe, excluyendo el actual equipo
        equipo_existente = Equipo.query.filter(Equipo.modelo_id == nuevo_modelo_id, Equipo.id != id).first()
        if equipo_existente:
            error = "Ya existe un equipo con ese modelo. Por favor, elige otro."
            return render_template('editar_equipo.html', equipo=equipo, modelos=modelos, marcas=marcas, error=error)

        # Actualizar el equipo
        equipo.marca_id = nuevo_marca_id
        equipo.modelo_id = nuevo_modelo_id
        equipo.costo = nuevo_costo

        try:
            db.session.commit()
            return redirect(url_for('lista_equipos'))
        except IntegrityError:
            db.session.rollback()
            error = "No se pudo guardar el equipo. Inténtalo de nuevo."
            return render_template('editar_equipo.html', equipo=equipo, modelos=modelos, marcas=marcas, error=error)

    return render_template('editar_equipo.html', equipo=equipo, modelos=modelos, marcas=marcas)

@app.route('/eliminar_equipo/<int:id>', methods=['POST'])
def eliminar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo eliminado exitosamente.', 'success')
    return redirect(url_for('lista_equipos'))


# Ruta para lista de stocks y creación de nuevo stock
@app.route('/lista_stocks', methods=['POST', 'GET'])
def lista_stocks():
    stocks = Stock.query.all()
    if request.method == 'POST':
        tipo_accesorio = request.form['tipo_accesorio']
        modelo_dispositivo = request.form['modelo_dispositivo']
        color = request.form['color']
        cantidad_disponible = int(request.form['cantidad_disponible'])
        ubicacion_almacen = request.form['ubicacion_almacen']

        # Verificar si el producto ya existe
        stock_existente = Stock.query.filter_by(tipo_accesorio=tipo_accesorio, modelo_dispositivo=modelo_dispositivo, color=color).first()

        if stock_existente:
            flash('Este stock ya existe. Por favor, use la opción de agregar cantidad.', 'danger')
            return redirect(url_for('lista_stocks'))
        
        # Crear nuevo stock
        nuevo_stock = Stock(tipo_accesorio=tipo_accesorio, modelo_dispositivo=modelo_dispositivo, color=color, cantidad_disponible=cantidad_disponible, ubicacion_almacen=ubicacion_almacen)
        db.session.add(nuevo_stock)
        db.session.commit()

        flash('Stock creado exitosamente.', 'success')
        return redirect(url_for('lista_stocks'))

    return render_template('lista_stocks.html', stocks=stocks)

# Ruta para agregar cantidad a un stock existente
@app.route('/agregar_cantidad_stock', methods=['POST'])
def agregar_cantidad_stock():
    tipo_accesorio = request.form['tipo_accesorio']
    modelo_dispositivo = request.form['modelo_dispositivo']
    color = request.form['color']
    cantidad_a_agregar = int(request.form['cantidad_a_agregar'])

    # Buscar si el stock ya existe
    stock_existente = Stock.query.filter_by(tipo_accesorio=tipo_accesorio, modelo_dispositivo=modelo_dispositivo, color=color).first()

    if stock_existente:
        stock_existente.cantidad_disponible += cantidad_a_agregar
        db.session.commit()

        flash('Cantidad agregada exitosamente.', 'success')
        return redirect(url_for('lista_stocks'))


# Ruta para editar un stock existente
@app.route('/stock/editar/<int:id>', methods=['GET', 'POST'])
def stock_editar(id):
    stock = Stock.query.get_or_404(id)  # Obtiene el stock o devuelve 404 si no existe

    if request.method == 'POST':
        # Procesa los datos del formulario enviados para actualizar el stock
        stock.tipo_accesorio = request.form['tipo_accesorio']
        stock.modelo_dispositivo = request.form['modelo_dispositivo']
        stock.color = request.form['color']
        stock.cantidad_disponible = request.form['cantidad_disponible']
        stock.ubicacion_almacen = request.form['ubicacion_almacen']

        try:
            db.session.commit()  # Guarda los cambios en la base de datos
            flash('El stock ha sido actualizado exitosamente.', 'success')
            return redirect(url_for('lista_stocks'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar el stock: {str(e)}', 'danger')

    # Renderiza la plantilla con los datos actuales del stock
    return render_template('editar_stock.html', stock=stock)


# Ruta para eliminar un stock
@app.route('/stock/<id>/eliminar', methods=['POST'])
def stock_eliminar(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    flash('Stock eliminado exitosamente.', 'success')
    return redirect(url_for('lista_stocks'))


@app.route('/lista_proveedores', methods=['POST', 'GET'])
def lista_proveedores():
    proveedores = Proveedor.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']

        # Verificar si ya existe un proveedor con el mismo nombre y contacto
        proveedor_existente = Proveedor.query.filter_by(nombre=nombre, contacto=contacto).first()
        if proveedor_existente:
            error = "Ya existe un proveedor con este nombre y contacto. Elige otro."
            return render_template('lista_proveedores.html', proveedores=proveedores, error=error)

        # Crear el nuevo proveedor si no hay conflicto
        nuevo_proveedor = Proveedor(nombre=nombre, contacto=contacto)
        db.session.add(nuevo_proveedor)
        db.session.commit()

        return redirect(url_for('lista_proveedores'))

    return render_template('lista_proveedores.html', proveedores=proveedores)

@app.route("/proveedor/<id>/editar", methods=['POST', 'GET'])
def proveedor_editar(id):
    proveedor = Proveedor.query.get_or_404(id)

    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_contacto = request.form['contacto']

        # Verificar si ya existe otro proveedor con el mismo nombre y contacto, excluyendo el actual
        proveedor_existente = Proveedor.query.filter(
            Proveedor.nombre == nuevo_nombre,
            Proveedor.contacto == nuevo_contacto,
            Proveedor.id != id  # Excluir el proveedor actual
        ).first()

        if proveedor_existente:
            error = "Ya existe otro proveedor con este nombre y contacto. Elige otro."
            return render_template('editar_proveedor.html', proveedor=proveedor, error=error)

        # Actualizar el proveedor si no hay conflicto
        proveedor.nombre = nuevo_nombre
        proveedor.contacto = nuevo_contacto
        db.session.commit()

        return redirect(url_for('lista_proveedores'))

    return render_template('editar_proveedor.html', proveedor=proveedor)


@app.route("/proveedor/<id>/eliminar", methods=['POST'])
def proveedor_eliminar(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    return redirect(url_for('lista_proveedores'))

@app.route('/lista_accesorios', methods=['POST', 'GET'])
def lista_accesorios():
    accesorios = Accesorio.query.all()
    modelos = Modelo.query.all()

    if request.method == 'POST':
        color = request.form['color']
        tipo = request.form['tipo']
        modelo_id = request.form['modelo_id']

        # Verificar si ya existe un accesorio con el mismo tipo, color y modelo
        accesorio_existente = Accesorio.query.filter_by(tipo=tipo, color=color, modelo_id=modelo_id).first()
        if accesorio_existente:
            error = "Ya existe un accesorio con este tipo, color y modelo. Elige otro."
            return render_template('lista_accesorios.html', accesorios=accesorios, modelos=modelos, error=error)

        # Crear nuevo accesorio si no existe uno con las mismas características
        nuevo_accesorio = Accesorio(color=color, tipo=tipo, modelo_id=modelo_id)
        db.session.add(nuevo_accesorio)
        db.session.commit()
        return redirect(url_for('lista_accesorios'))

    return render_template('lista_accesorios.html', accesorios=accesorios, modelos=modelos)

@app.route("/accesorio/<id>/editar", methods=['POST', 'GET'])
def accesorio_editar(id):
    accesorio = Accesorio.query.get_or_404(id)
    modelos = Modelo.query.all()

    if request.method == 'POST':
        nuevo_color = request.form['color']
        nuevo_tipo = request.form['tipo']
        nuevo_modelo_id = request.form['modelo_id']

        # Verificar si ya existe otro accesorio con el mismo tipo, color y modelo, excluyendo el actual
        accesorio_existente = Accesorio.query.filter(
            Accesorio.tipo == nuevo_tipo,
            Accesorio.color == nuevo_color,
            Accesorio.modelo_id == nuevo_modelo_id,
            Accesorio.id != id  # Excluir el accesorio actual
        ).first()

        if accesorio_existente:
            error = "Ya existe un accesorio con este tipo, color y modelo. Elige otro."
            return render_template('editar_accesorio.html', accesorio=accesorio, modelos=modelos, error=error)

        # Actualizar el accesorio si no hay conflictos
        accesorio.color = nuevo_color
        accesorio.tipo = nuevo_tipo
        accesorio.modelo_id = nuevo_modelo_id

        db.session.commit()
        return redirect(url_for('lista_accesorios'))

    return render_template('editar_accesorio.html', accesorio=accesorio, modelos=modelos)

@app.route("/accesorio/<id>/eliminar", methods=['POST'])
def accesorio_eliminar(id):
    accesorio = Accesorio.query.get_or_404(id)
    db.session.delete(accesorio)
    db.session.commit()
    return redirect(url_for('lista_accesorios'))

