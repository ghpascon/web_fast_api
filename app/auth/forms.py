# app/auth/forms.py

from pydantic import BaseModel, field_validator

class LoginForm(BaseModel):
    username: str
    password: str
    csrf_token: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Usuário deve ter pelo menos 3 caracteres.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not v or len(v) < 4:
            raise ValueError("Senha deve ter pelo menos 4 caracteres.")
        return v
