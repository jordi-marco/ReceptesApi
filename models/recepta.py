from sqlalchemy import Column, Integer, String, Text, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ReceptaDB(Base):
    __tablename__ = "receptes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    descripcio = Column(Text, nullable=False)
    minuts = Column(Integer, nullable=False)
    ingredients = Column(ARRAY(Text), default=[])
    likes = Column(Integer, default=0)
    url_imatge = Column(Text, nullable=True)
