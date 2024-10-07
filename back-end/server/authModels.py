from pydantic import BaseModel


# Schéma pour la création d'utilisateurs et la réponse d'authentification
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
