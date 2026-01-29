from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlmodel import Session
from ..models.zapatilla import Zapatilla, ZapatillaCreate, ZapatillaResponse, map_zapatilla_to_response, map_create_to_zapatilla

from ..data.zapatillas_repository import ZapatillasRepository
from ..data.db import init_db, get_session

router = APIRouter(prefix="/api/zapatillas", tags=["zapatillas"])

SessionDep = Annotated[Session, Depends(get_session)]

# Rutas de la API para gestionar zapatillas
@router.get("/", response_model=list[ZapatillaResponse])
async def lista_zapatillas(session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatillas = repo.get_all()
    return [map_zapatilla_to_response(zapatilla) for zapatilla in zapatillas]

@router.post("/", response_model=ZapatillaResponse)
async def nueva_zapatilla(zapatilla_create: ZapatillaCreate, session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla = map_create_to_zapatilla(zapatilla_create)
    zapatilla_creada = repo.create(zapatilla)
    return map_zapatilla_to_response(zapatilla_creada)


@router.get("/{zapatilla_id}", response_model=ZapatillaResponse)
async def zapatilla_por_id(zapatilla_id: int, session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla_encontrada = repo.get_by_id(zapatilla_id)
    if not zapatilla_encontrada:
        raise HTTPException(status_code=404, detail="Zapatilla no encontrada")
    return map_zapatilla_to_response(zapatilla_encontrada)

@router.delete("/{zapatilla_id}", status_code=204)
async def borrar_zapatilla(zapatilla_id: int, session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla_encontrada = repo.get_by_id(zapatilla_id)
    if not zapatilla_encontrada:
        raise HTTPException(status_code=404, detail="Zapatilla no encontrada")
    repo.delete(zapatilla_encontrada)
    return None

@router.patch("/{zapatilla_id}", response_model=ZapatillaResponse)
async def actualizar_zapatilla(zapatilla_id: int, zapatilla_update: ZapatillaCreate, session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla_encontrada = repo.get_by_id(zapatilla_id)
    if not zapatilla_encontrada:
        raise HTTPException(status_code=404, detail="Zapatilla no encontrada")
    zapatilla_actualizada = repo.update(zapatilla_encontrada, zapatilla_update)
    return map_zapatilla_to_response(zapatilla_actualizada)

@router.put("/",response_model=ZapatillaResponse)
async def cambia_zapatilla(zapatilla: Zapatilla, session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla_encontrada = repo.get_by_id(zapatilla.id)
    if not zapatilla_encontrada:
        raise HTTPException(status_code=404, detail="Zapatilla no encontrada")
    zapatilla_actualizada = repo.replace(zapatilla)
    return map_zapatilla_to_response(zapatilla_actualizada)