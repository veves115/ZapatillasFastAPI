from sqlmodel import Session, select
from ..models.zapatilla import Zapatilla

class ZapatillasRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self) -> list[Zapatilla]:
        zapatillas = self.session.exec(select(Zapatilla)).all()
        return zapatillas   

    def get_by_id(self, zapatilla_id: int) -> Zapatilla:
        zapatilla = self.session.get(Zapatilla, zapatilla_id)
        return zapatilla
    
    def create(self, zapatilla: Zapatilla) -> Zapatilla:
        self.session.add(zapatilla)
        self.session.commit()
        self.session.refresh(zapatilla)
        return zapatilla
    
    def update(self, zapatilla: Zapatilla) -> Zapatilla:
        self.session.add(zapatilla)
        self.session.commit()
        self.session.refresh(zapatilla)
        return zapatilla

    def delete(self, zapatilla: Zapatilla) -> None:
        self.session.delete(zapatilla)
        self.session.commit()