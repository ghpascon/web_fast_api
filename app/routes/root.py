from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates  
from app.auth.utils import get_current_user

import markdown

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

        "message": "Bem-vindo à aplicação FastAPI com login!",
        "user" : get_current_user(request)
    })

@router.get("/readme", response_class=HTMLResponse)
async def readme():
    try:
        with open("README.md", "r", encoding="utf-8") as file:
            content = file.read()
        html_content = markdown.markdown(content)
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Erro ao carregar README.md</h1><p>{str(e)}</p>", status_code=500)