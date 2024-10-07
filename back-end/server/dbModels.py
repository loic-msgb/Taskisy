from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

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



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    projects = relationship("Project", back_populates="user")
    tasks = relationship("Task", back_populates="user")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tasks = relationship("Task", back_populates="project")
    user = relationship("User", back_populates="projects")

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    done = Column(Boolean, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    project = relationship("Project", back_populates="tasks")
    user = relationship("User", back_populates="tasks")
    

# Crée toutes les tables dans la base de données qui n'existent pas déjà
Base.metadata.create_all(bind=engine)
'''
Exécutez le code ci-dessus pour créer la base de données et la table.'''