from pydantic import BaseModel, Field, field_validator

class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3)
    secret_key: str = None

    # Validação do nome de usuário para garantir que não contenha espaços
    @field_validator('username')
    def no_spaces(cls, v):
        if " " in v:
            raise ValueError("O nome de usuário não pode conter espaços.")
        return v

    # Validação da senha para garantir que tenha pelo menos 3 caracteres
    @field_validator('password')
    def password_length(cls, v):
        if len(v) < 3:
            raise ValueError("A senha deve ter pelo menos 3 caracteres.")
        return v
