from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates  # reutilizando
from datetime import datetime
from app.auth.utils import get_current_user

router = APIRouter(prefix="", tags=["Root"])

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    alerts = [
        {
            "text":"Seja bem vindo",
            "class":"alert-primary"
        },
        {
            "text":"👍",
            "class":"alert-success"
        },        
    ]
    return templates.TemplateResponse("root/index.html", {
        "request": request,
        "title": "Home",
        "alerts":alerts,
        "now": datetime.now(),

        "message": "Bem-vindo à aplicação FastAPI com login!",
        "user" : get_current_user(request)
    })