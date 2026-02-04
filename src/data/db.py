from sqlmodel import SQLModel, create_engine, Session, select
from ..models.zapatilla import Zapatilla
from dotenv import load_dotenv
from datetime import date
import os

load_dotenv()

db_user: str = os.getenv("DB_USER", "pablo")
db_password: str = os.getenv("DB_PASSWORD", "1234")
db_host: str = os.getenv("DB_HOST", "zapatillas-db")
db_port: str = os.getenv("DB_PORT", "3306")
db_name: str = os.getenv("DB_NAME", "zapatillas-db")

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True, pool_recycle=300)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Solo si no hay datos existentes, insertar datos de ejemplo
        existing = session.exec(select(Zapatilla)).first()
        if existing is None:
            session.add(Zapatilla(id=1,marca="Nike", modelo="Air Max", talla=42.5, precio=120.0, tipo="Deportivo", color="Rojo", fecha_lanzamiento=date(2022, 1, 15)))
            session.add(Zapatilla(id=2,marca="Adidas", modelo="Ultraboost", talla=43.0, precio=150.0, tipo="Running", color="Negro", fecha_lanzamiento=date(2021, 11, 20)))
            session.add(Zapatilla(id=3,marca="Puma", modelo="Suede Classic", talla=41.0, precio=80.0, tipo="Casual", color="Blanco", fecha_lanzamiento=date(2020, 5, 10)))
            session.add(Zapatilla(id=4,marca="Reebok", modelo="Club C 85", talla=42.0, precio=90.0, tipo="Casual", color="Verde", fecha_lanzamiento=date(2019, 8, 25)))
            session.add(Zapatilla(id=5,marca="New Balance", modelo="574", talla=44.0, precio=100.0, tipo="Deportivo", color="Azul", fecha_lanzamiento=date(2021, 3, 30)))
            session.commit()
        
