from app import db


class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pais_origen = db.Column(db.String(100), nullable=False)

    marcas = db.relationship('Marca', backref='fabricante', cascade="all, delete-orphan")

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)
    equipos = db.relationship('Equipo', backref='marca', cascade="all, delete-orphan") #importante
    
    

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)

    marca = db.relationship('Marca', backref=db.backref('modelos', lazy=True, cascade="all, delete-orphan"))
    caracteristicas = db.relationship('Caracteristica', backref='modelo', cascade="all, delete-orphan") 
    accesorios = db.relationship('Accesorio', back_populates='modelo', cascade="all, delete-orphan")
    equipos = db.relationship('Equipo', backref='modelo', cascade="all, delete-orphan") #importante

class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False) 
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id', ondelete='CASCADE'), nullable=False)
    

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id', ondelete='CASCADE'), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id', ondelete='CASCADE'), nullable=False)
    costo = db.Column(db.Float, nullable=False)

    # marca = db.relationship('Marca', backref='equipos')
    # modelo = db.relationship('Modelo', backref='equipos')

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_accesorio = db.Column(db.String(50), nullable=False)
    modelo_dispositivo = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)
    ubicacion_almacen = db.Column(db.String(100), nullable=False)

class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # Ejemplo: 'funda', 'cargador'
    color = db.Column(db.String(30), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'))  # Añadido modelo_id
    
    modelo = db.relationship('Modelo', back_populates='accesorios')