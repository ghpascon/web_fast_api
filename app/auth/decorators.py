# app/auth/decorators.py
from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app.auth.utils import get_current_user

def login_required(route_function):
    @wraps(route_function)
    async def wrapper(request: Request, *args, **kwargs):
        user = get_current_user(request)
        if user:
            return await route_function(request, *args, **kwargs)
        
        rota = str(request.url.path)
        mensagem = f"Necessário autenticação para acessar a rota: {rota}"
        
        return RedirectResponse(
            url=f"/auth/login?mensagem={mensagem}&next_page={rota}",
            status_code=HTTP_303_SEE_OTHER
        )
    return wrapper
