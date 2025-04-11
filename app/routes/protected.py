from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates  # reutilizando
from datetime import datetime
from app.auth.utils import get_current_user
from app.auth.decorators import login_required

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/simple", response_class=HTMLResponse)
@login_required
async def root(request: Request):
    return templates.TemplateResponse("protected/protected.html", {
        "request": request,
        "title": "Rota protegida",
        "alerts":[],
        "now": datetime.now(),

        "user" : get_current_user(request)
    })
