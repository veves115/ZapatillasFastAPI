from typing import Annotated
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .routers.api_zapatillas_router import router as api_router

from .models.zapatilla import Zapatilla, ZapatillaCreate, ZapatillaResponse,  map_zapatilla_to_response, map_create_to_zapatilla
from .data.db import init_db, get_session
from .data.zapatillas_repository import ZapatillasRepository

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan =lifespan)

# Configurar directorios para templates y archivos estáticos
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(api_router)
@app.get("/zapatillas", response_model=list[Zapatilla])
def lista_zapatillas(session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatillas = repo.get_all()
    return zapatillas

@app.post("/zapatillas", response_model=ZapatillaResponse)
def nueva_zapatilla(zapatilla_create: ZapatillaCreate, session : SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla = map_create_to_zapatilla(zapatilla_create)
    zapatilla_creada = repo.create(zapatilla)
    return map_zapatilla_to_response(zapatilla_creada)

@app.get("/zapatillas/{zapatilla_id}", response_model=Zapatilla)
def zapatilla_por_id(zapatilla_id: int, session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla_encontrada = repo.get_by_id(zapatilla_id)
    if not zapatilla_encontrada:
        raise HTTPException(status_code=404, detail="Zapatilla no encontrada")
    return zapatilla_encontrada

@app.delete("/zapatillas/{zapatilla_id}")
def eliminar_zapatilla(zapatilla_id: int, session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla_encontrada = repo.get_by_id(zapatilla_id)
    if not zapatilla_encontrada:
        raise HTTPException(status_code=404, detail="Zapatilla no encontrada")
    repo.delete(zapatilla_encontrada)
    return {"detail": "Zapatilla eliminada"}

@app.patch("/zapatillas/{zapatilla_id}", response_model=Zapatilla)
def cambia_zapatilla(zapatilla_id: int, zapatilla: Zapatilla, session: SessionDep):
    repo = ZapatillasRepository(session)
    zapatilla_encontrada = repo.get_by_id(zapatilla_id)
    if not zapatilla_encontrada:
        raise HTTPException(status_code=404, detail="Zapatilla no encontrada")
    zapatilla_data = zapatilla.model_dump(exclude_unset=True)
    zapatilla_encontrada.sqlmodel_update(zapatilla_data)
    repo.update(zapatilla_encontrada)
    return zapatilla_encontrada

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
