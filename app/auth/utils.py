# app/auth/utils.py

from passlib.context import CryptContext
from fastapi import Request
import secrets
from app.db.database import get_db
from app.models.auth import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Senha ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# --- Sessão ---
def get_current_user(request: Request):
    return request.session.get("user")


def login_user(request: Request, user: dict):
    request.session["user"] = user


def logout_user(request: Request):
    request.session.clear()


# --- CSRF ---
def get_csrf_token(request: Request) -> str:
    token = request.session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf_token"] = token
    return token


def validate_csrf_token(request: Request, token: str) -> bool:
    return token == request.session.get("csrf_token")

# ---Registro e conferencia de usuario
def register_user(username: str, password: str) -> User:
    # Verificar se o nome de usuário já existe
    with get_db() as db:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise ValueError("Usuário já existe")

        # Criptografar a senha
        hashed_password = get_password_hash(password)

        # Criar o novo usuário
        new_user = User(username=username, password=hashed_password)

        # Adicionar o novo usuário no banco de dados
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
