from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings

import os
import importlib
from pathlib import Path
readme_path = Path("README.md") 
readme_content = readme_path.read_text(encoding="utf-8")


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session",           # Nome do cookie
    https_only=True,                    # Garante HTTPS (ideal em produção)
    same_site="lax",                    # Proteção contra CSRF básica
    max_age=3600                        # Tempo de vida da sessão em segundos
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def include_all_routes(current_path):
    routes_path = os.path.join(os.path.dirname(__file__), current_path)

    for filename in os.listdir(routes_path):
        if not filename == "__pycache__" and not "." in filename:
            include_all_routes(current_path + '/' + filename)
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            file_path = os.path.join(routes_path, filename)

            spec = importlib.util.spec_from_file_location(f"app.routes.{module_name}", file_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                if hasattr(module, "router"):
                    app.include_router(module.router)
                    print(f"✅ Rota incluída: {module_name}")
                else:
                    print(f"⚠️  Arquivo {filename} não contém um 'router'")
            except Exception as e:
                print(f"❌ Erro ao importar {filename}: {e}")

include_all_routes("routes")

# python -m app.db.database
# uvicorn app.main:app --reload
# uvicorn app.main:app --host 0.0.0.0 --port $PORT
