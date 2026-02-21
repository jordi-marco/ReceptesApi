import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, insert, select, update, delete
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import Optional, List
from models.recepta import ReceptaDB
from schemas.recepta import ReceptaCreate, ReceptaResponse

class ReceptesDataService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReceptesDataService, cls).__new__(cls)
            load_dotenv()
            db_url = os.getenv("DATABASE_URL")
            # El motor (engine) gestiona el pool de connexions automàticament
            cls._instance.engine = create_engine(db_url, pool_pre_ping=True)
            cls._instance.SessionLocal = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=cls._instance.engine
            )
            # Crea la taula només si no existeix (Persistent)
            ReceptaDB.metadata.create_all(bind=cls._instance.engine)
        return cls._instance

    @contextmanager
    def _get_session(self):
        # Gestiona el cicle de vida de la sessió amb yield i finally.
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # CRUD methods
    def create_recepta(self, recepta: ReceptaCreate) -> Optional[ReceptaDB]:
        with self._get_session() as session:
            stmt = (
                insert(ReceptaDB)
                .values(**recepta.model_dump())
                .returning(ReceptaDB)
            )                
            nova_recepta = session.execute(stmt)
            session.commit()
            return nova_recepta.scalar_one_or_none()
 
    def read_receptes(self) -> List[ReceptaDB]:
        with self._get_session() as session:
            stmt = select(ReceptaDB)
            return session.execute(stmt).scalars().all()
 
    def read_recepta(self, id: int) -> Optional[ReceptaDB]:
        with self._get_session() as session:
            stmt = select(ReceptaDB).where(ReceptaDB.id == id)
            return session.execute(stmt).scalar_one_or_none()
        
    def update_recepta(self, id: int, recepta: ReceptaCreate) -> Optional[ReceptaDB]:
        with self._get_session() as session:
            stmt = (
                update(ReceptaDB)
                .where(ReceptaDB.id == id)
                .values(**recepta.model_dump())
                .returning(ReceptaDB)
            )            
            recepta_actualitzada = session.execute(stmt)
            session.commit()
            return recepta_actualitzada.scalar_one_or_none()


    def delete_recepta(self, id: int) -> Optional[ReceptaDB]:
        with self._get_session() as session:
            stmt = (
                delete(ReceptaDB)
                .where(ReceptaDB.id == id)
                .returning(ReceptaDB)
            )
            recepta_eliminada = session.execute(stmt)
            session.commit()
            return recepta_eliminada.scalar_one_or_none()
            
    def incrementar_likes(self, id: int) -> Optional[ReceptaDB]:
        with self._get_session() as session:
            stmt = (
                update(ReceptaDB)
                .where(ReceptaDB.id == id)
                .values(likes=ReceptaDB.likes + 1)
                .returning(ReceptaDB)
            )
            recepta_actualitzada = session.execute(stmt)
            session.commit()
            return recepta_actualitzada.scalar_one_or_none()