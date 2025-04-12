from fastapi import APIRouter, Request, Form, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.templates import templates
from app.auth.utils import (
    login_user,
    logout_user,
    verify_password,
    get_csrf_token,
    validate_csrf_token,
    register_user,
)
from app.db.database import get_db
from app.schemas.auth import UserSchema
from datetime import datetime
from app.models.auth import User
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

# Login GET route
@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request, mensagem: str = Query(None), next_page: str = Query(None)):
    csrf_token = get_csrf_token(request)
    if mensagem:
        msg_alert = {"text":mensagem, "class": "alert-primary"}
    else:msg_alert = None
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "title": "Login",
        "alerts": [msg_alert],

        "csrf_token": csrf_token,
        "next_page":next_page
    })

# Login POST route
@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    next_page: str = Form(...),
):
    # CSRF token validation
    if not validate_csrf_token(request, csrf_token):
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "title": "Login",
            "alerts": [{"text": "Token CSRF inválido.", "class": "alert-danger"}],

            "csrf_token": get_csrf_token(request),
            "next_page":next_page
        })

    try:
        # Validating form data using Pydantic UserSchema
        form_data = UserSchema(username=username, password=password)
    except ValueError as e:
        # Handle validation errors for the form fields
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "title": "Login",
            "alerts": [{"text": str(e), "class": "alert-danger"}],

            "csrf_token": get_csrf_token(request),
            "next_page":next_page
        })

    # Check if the user exists and password matches
    with get_db() as db:
        user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "title": "Login",
            "alerts": [{"text": "Usuário ou senha incorretos.", "class": "alert-danger"}],

            "csrf_token": get_csrf_token(request),
            "next_page":next_page
        })

    # Log the user in if credentials are valid
    user_dict = {
        "id":user.id,
        "username":user.username
    }
    login_user(request, user_dict)
    if next_page and not next_page == "None":
        page = next_page
    else:
        page = "/"
    return RedirectResponse(page, status_code=status.HTTP_302_FOUND)

# Logout route
@router.get("/logout")
async def logout(request: Request):
    logout_user(request)
    return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

# Register GET route
@router.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    csrf_token = get_csrf_token(request)
    return templates.TemplateResponse("auth/register.html", {
        "request": request,
        "title": "Registro de usuário",
        "alerts": [],

        "csrf_token": csrf_token,
    })

# Register POST route
@router.post("/register", response_class=HTMLResponse)
async def register_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    secret_key: str = Form(...),
    csrf_token: str = Form(...)
):
    # CSRF token validation
    if not validate_csrf_token(request, csrf_token):
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "title": "Registro de usuário",
            "alerts": [{"text": "Token CSRF inválido.", "class": "alert-danger"}],

            "csrf_token": get_csrf_token(request),
        })

    try:
        # Validate user registration form data
        form_data = UserSchema(username=username, password=password, secret_key=secret_key)
    except ValueError as e:
        # Handle validation errors for the form fields
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "title": "Registro de usuário",
            "alerts": [{"text": str(e), "class": "alert-danger"}],
            "now": datetime.now(),
            "csrf_token": get_csrf_token(request),
        })
    # Validar secret_key
    if not form_data.secret_key == settings.SECRET_KEY:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "title": "Registro de usuário",
            "alerts": [{"text": "SECRET_KEY invalida", "class": "alert-danger"}],
            "now": datetime.now(),
            "csrf_token": get_csrf_token(request),
        })        

    # Try to register the user in the database
    try:
        new_user = register_user(form_data.username, form_data.password)
    except ValueError as e:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "title": "Registro de usuário",
            "alerts": [{"text": str(e), "class": "alert-danger"}],
            "now": datetime.now(),
            "csrf_token": get_csrf_token(request),
        })
    
    mensagem = f"Usuário: {form_data.username} criado com sucesso"
    return RedirectResponse(f"/auth/login?mensagem={mensagem}", status_code=status.HTTP_302_FOUND)
