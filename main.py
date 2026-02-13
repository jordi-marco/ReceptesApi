import os
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, ARRAY, update, delete, select
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel, Field

# --- CONFIGURACIÓ DE LA BASE DE DADES ---
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODEL DE LA BASE DE DADES (SQLAlchemy) ---
class ReceptaDB(Base):
    __tablename__ = "receptes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    descripcio = Column(Text, nullable=False)
    minuts = Column(Integer, nullable=False)
    ingredients = Column(ARRAY(Text), default=[])
    likes = Column(Integer, default=0)
    url_imatge = Column(Text, nullable=True)

# Crea la taula només si no existeix (Persistent)
Base.metadata.create_all(bind=engine)

# --- ESQUEMES DE DADES (Pydantic - Python 3.9+ style) ---
class ReceptaBase(BaseModel):
    nom: str
    descripcio: str
    minuts: int
    ingredients: list[str] = []
    likes: int = 0
    url_imatge: Optional[str] = Field(None, alias="urlImatge")
    class Config:
        populate_by_name = True
        from_attributes = True

class ReceptaCreate(ReceptaBase):
    pass

class ReceptaResponse(ReceptaBase):
    id: int

# --- DEPENDÈNCIA PER LA DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- INSTÀNCIA DE L'API ---
app = FastAPI(title="API Receptes 1.0")

# --- MÈTODES CRUD (Estil SQLAlchemy 2.0 Atòmic) ---

# 1. Crear una recepta
@app.post("/receptes", response_model=ReceptaResponse)
def create_recepta(recepta: ReceptaCreate, db: Session = Depends(get_db)):
    nova_recepta = ReceptaDB(**recepta.model_dump())
    db.add(nova_recepta)
    db.commit()
    db.refresh(nova_recepta)
    return nova_recepta

# 2. Consultar totes les receptes (Usant select + execute)
@app.get("/receptes", response_model=list[ReceptaResponse])
def read_receptes(db: Session = Depends(get_db)):
    stmt = select(ReceptaDB)
    return db.execute(stmt).scalars().all()

# 3. Consultar una sola recepta per ID (Usant select + execute)
@app.get("/receptes/{id}", response_model=ReceptaResponse)
def read_recepta(id: int, db: Session = Depends(get_db)):
    stmt = select(ReceptaDB).where(ReceptaDB.id == id)
    resultat = db.execute(stmt)
    recepta = resultat.scalar_one_or_none()
    
    if not recepta:
        raise HTTPException(status_code=404, detail="Recepta no trobada")
    return recepta

# 4. Actualitzar una recepta (PUT Atòmic)
@app.put("/receptes/{id}", response_model=ReceptaResponse)
def update_recepta(id: int, recepta: ReceptaCreate, db: Session = Depends(get_db)):
    stmt = (
        update(ReceptaDB)
        .where(ReceptaDB.id == id)
        .values(**recepta.model_dump())
        .returning(ReceptaDB)
    )
    
    resultat = db.execute(stmt)
    recepta_actualitzada = resultat.scalar_one_or_none()
    db.commit()

    if not recepta_actualitzada:
        raise HTTPException(status_code=404, detail="No existeix la recepta per actualitzar")
    
    return recepta_actualitzada

# 5. Esborrar una recepta (DELETE Atòmic)
@app.delete("/receptes/{id}", response_model=ReceptaResponse)
def delete_recepta(id: int, db: Session = Depends(get_db)):
    stmt = delete(ReceptaDB).where(ReceptaDB.id == id).returning(ReceptaDB)
    resultat = db.execute(stmt)
    recepta_esborrada = resultat.scalar_one_or_none()
    db.commit()

    if not recepta_esborrada:
        raise HTTPException(status_code=404, detail="No s'ha trobat la recepta per esborrar")
    
    return recepta_esborrada

# 6. Bonus: Fer Like (Increment atòmic)
@app.post("/receptes/{id}/like", response_model=ReceptaResponse)
def fer_like(id: int, db: Session = Depends(get_db)):
    stmt = (
        update(ReceptaDB)
        .where(ReceptaDB.id == id)
        .values(likes=ReceptaDB.likes + 1)
        .returning(ReceptaDB)
    )
    resultat = db.execute(stmt)
    recepta_actualitzada = resultat.scalar_one_or_none()
    db.commit()

    if not recepta_actualitzada:
        raise HTTPException(status_code=404, detail="Recepta no trobada")
    
    return recepta_actualitzada