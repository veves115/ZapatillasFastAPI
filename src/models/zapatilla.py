from datetime import date
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Zapatilla(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    talla: float
    precio: float
    tipo: str
    color: str
    fecha_lanzamiento: date

#dto classes 
class ZapatillaCreate(BaseModel):
    marca: str
    modelo: str
    talla: float
    precio: float
    tipo: str
    color: str
    fecha_lanzamiento: date

class ZapatillaUpdate(BaseModel):
    marca: str | None = None
    modelo: str | None = None
    talla: float | None = None
    precio: float | None = None
    tipo: str | None = None
    color: str | None = None
    fecha_lanzamiento: date | None = None

class ZapatillaResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    talla: float
    precio: float
    tipo: str
    color: str


# mapping functions 
def map_zapatilla_to_response(zapatilla: Zapatilla) -> ZapatillaResponse:
    return ZapatillaResponse(
        id=zapatilla.id,
        marca=zapatilla.marca,
        modelo=zapatilla.modelo,
        talla=zapatilla.talla,
        precio=zapatilla.precio,
        tipo=zapatilla.tipo,
        color=zapatilla.color
    )

def map_create_to_zapatilla(zapatilla_create: ZapatillaCreate) -> Zapatilla:
    return Zapatilla(
        marca=zapatilla_create.marca,
        modelo=zapatilla_create.modelo,
        talla=zapatilla_create.talla,
        precio=zapatilla_create.precio,
        tipo=zapatilla_create.tipo,
        color=zapatilla_create.color,
        fecha_lanzamiento=zapatilla_create.fecha_lanzamiento
    )

def map_update_to_zapatilla(zapatilla: Zapatilla, zapatilla_update: ZapatillaUpdate) -> Zapatilla:
    if zapatilla_update.precio is not None:
        zapatilla.precio = zapatilla_update.precio

        return zapatilla
