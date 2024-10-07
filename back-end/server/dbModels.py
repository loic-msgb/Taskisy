from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from typing import Generator

Base = declarative_base()
# Crée un moteur qui correspond à ta base de données
engine = create_engine('sqlite:///mydatabase.db')
# Crée une fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance pour obtenir la session de base de données
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crée toutes les tables dans la base de données qui n'existent pas déjà
Base.metadata.create_all(bind=engine)

class User(Base):
    __tablename__ = 'users'  # Nom de la table dans la base de données

    id = Column(Integer, primary_key=True, index=True)  # L'attribut id
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

'''
Exécutez le code ci-dessus pour créer la base de données et la table.'''