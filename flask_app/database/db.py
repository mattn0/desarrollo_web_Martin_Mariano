from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, DateTime, Text, func, extract
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload, selectinload
from datetime import datetime, timedelta

# copiado de lo pedido en la tarea y de la estructura de auxs
DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# igual que aux 6, pero agregando dos (pq son 2 tablas) y con las cosas que necesitaba cada una

class Region(Base):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    comunas = relationship("Comuna", back_populates="region", cascade="all, delete")


class Comuna(Base):
    __tablename__ = "comuna"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)

    region = relationship("Region", back_populates="comunas")
    avisos = relationship("AvisoAdopcion", back_populates="comuna", cascade="all, delete")


class AvisoAdopcion(Base):
    __tablename__ = "aviso_adopcion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False, default=datetime.now)
    comuna_id = Column(Integer, ForeignKey("comuna.id"), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    tipo = Column(Enum("gato", "perro"))
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum("a", "m"))  # años o meses
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(Text)

    comuna = relationship("Comuna", back_populates="avisos")
    fotos = relationship("Foto", back_populates="aviso", cascade="all, delete")
    contactos = relationship("ContactarPor", back_populates="aviso", cascade="all, delete")


class Foto(Base):
    __tablename__ = "foto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    aviso_id = Column(Integer, ForeignKey("aviso_adopcion.id"), nullable=False)

    aviso = relationship("AvisoAdopcion", back_populates="fotos")


class ContactarPor(Base):
    __tablename__ = "contactar_por"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum("whatsapp", "telegram", "X", "instagram", "tiktok", "otra"), nullable=False)
    identificador = Column(String(150), nullable=False)
    aviso_id = Column(Integer, ForeignKey("aviso_adopcion.id"), nullable=False)

    aviso = relationship("AvisoAdopcion", back_populates="contactos")

# Regiones y comunas
def get_regiones():
    session = SessionLocal()
    try:
        return session.query(Region).order_by(Region.nombre).all()
    finally:
        session.close()

def get_comunas_by_region(region_id):
    session = SessionLocal()
    try:
        return (
            session.query(Comuna)
            .filter_by(region_id=region_id)
            .order_by(Comuna.nombre)
            .all()
        )
    finally:
        session.close()

# Avisos
def get_last_avisos(limit=5):
    
    #ultimos avisos con relaciones
    
    session = SessionLocal()
    try:
        avisos = (
            session.query(AvisoAdopcion)
            .options(
                joinedload(AvisoAdopcion.comuna),     # acceso a aviso.comuna.nombre
                selectinload(AvisoAdopcion.fotos)    #joinenload y selectinload deberia no estar usandolo y hacer como "carga perezosa?"
            )
            .order_by(AvisoAdopcion.fecha_ingreso.desc())
            .limit(limit)
            .all()
        )
        # “tocar” atributos (opcional)
        for a in avisos:
            _ = a.comuna.nombre if a.comuna else None
            _ = len(a.fotos)
        return avisos
    finally:
        session.close()

def insert_aviso(comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion):
    session = SessionLocal()
    try:
        nuevo_aviso = AvisoAdopcion(
            comuna_id=comuna_id,
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            tipo=tipo,
            cantidad=cantidad,
            edad=edad,
            unidad_medida=unidad_medida,
            fecha_entrega=fecha_entrega,
            descripcion=descripcion
        )
        session.add(nuevo_aviso)
        session.commit()
        return nuevo_aviso.id
    finally:
        session.close()

def insert_foto(aviso_id, ruta_archivo, nombre_archivo):
    session = SessionLocal()
    try:
        nueva_foto = Foto(aviso_id=aviso_id, ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo)
        session.add(nueva_foto)
        session.commit()
    finally:
        session.close()

def insert_contacto(aviso_id, nombre, identificador):
    session = SessionLocal()
    try:
        nuevo_contacto = ContactarPor(aviso_id=aviso_id, nombre=nombre, identificador=identificador)
        session.add(nuevo_contacto)
        session.commit()
    finally:
        session.close()

def get_avisos_paginated(page, per_page=5):
    
    #Lista de avisos (no tupla)
    
    session = SessionLocal()
    try:
        avisos = (
            session.query(AvisoAdopcion)
            .options(
                joinedload(AvisoAdopcion.comuna),
                selectinload(AvisoAdopcion.fotos)
            )
            .order_by(AvisoAdopcion.fecha_ingreso.desc())
            .offset((page - 1) * per_page)  #??
            .limit(per_page)
            .all()
        )
        # no se para que hay que poner esto la verdad
        for a in avisos:
            _ = a.comuna.nombre if a.comuna else None
            _ = len(a.fotos)
        return avisos
    finally:
        session.close()

def get_aviso_by_id(aviso_id):
    
    #(detalle.html)
    
    session = SessionLocal()
    try:
        a = (
            session.query(AvisoAdopcion)
            .options(joinedload(AvisoAdopcion.comuna))
            .filter_by(id=aviso_id)
            .first()
        )
        if a and a.comuna:
            _ = a.comuna.nombre
        return a
    finally:
        session.close()

def get_fotos_by_aviso(aviso_id):
    session = SessionLocal()
    try:
        return session.query(Foto).filter_by(aviso_id=aviso_id).all()
    finally:
        session.close()

def get_contactos_by_aviso(aviso_id):
    session = SessionLocal()
    try:
        return session.query(ContactarPor).filter_by(aviso_id=aviso_id).all()
    finally:
        session.close()

def get_total_avisos():
    session = SessionLocal()
    try:
        return session.query(AvisoAdopcion).count()
    finally:
        session.close()

##estadisticas?? 

def get_stats_por_tipo():
    
    #Retorna lista: [{"tipo": "gato", "total": 10}, {"tipo": "perro", "total": 7}]
    
    session = SessionLocal()
    try:
        rows = (
            session.query(AvisoAdopcion.tipo, func.count(AvisoAdopcion.id))
            .group_by(AvisoAdopcion.tipo)
            .all()
        )
        return [{"tipo": t, "total": int(c)} for (t, c) in rows]
    finally:
        session.close()

def get_stats_por_dia(days=30):
    
    #Retorna lista : [{"dia": date, "total": 3}, ...] para los últimos `days` días.
    
    session = SessionLocal()
    try:
        desde = datetime.now() - timedelta(days=days)
        rows = (
            session.query(func.date(AvisoAdopcion.fecha_ingreso), func.count(AvisoAdopcion.id))
            .filter(AvisoAdopcion.fecha_ingreso >= desde)
            .group_by(func.date(AvisoAdopcion.fecha_ingreso))
            .order_by(func.date(AvisoAdopcion.fecha_ingreso))
            .all()
        )
        # rows: [(date, count)]
        return [{"dia": d, "total": int(c)} for (d, c) in rows]
    finally:
        session.close()

def get_stats_por_mes(year=None):
    
    #Retorna lista : [{"mes": 1, "total": 5}, ...] para el año indicado (por defecto, año actual).
    
    session = SessionLocal()
    try:
        if year is None:
            year = datetime.now().year
        rows = (
            session.query(extract('month', AvisoAdopcion.fecha_ingreso), func.count(AvisoAdopcion.id))
            .filter(extract('year', AvisoAdopcion.fecha_ingreso) == year)
            .group_by(extract('month', AvisoAdopcion.fecha_ingreso))
            .order_by(extract('month', AvisoAdopcion.fecha_ingreso))
            .all()
        )
        # rows: [(mes_float, count)] -> mes puede venir como 1.0
        return [{"mes": int(m), "total": int(c)} for (m, c) in rows]
    finally:
        session.close()
