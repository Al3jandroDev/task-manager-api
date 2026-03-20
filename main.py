from fastapi import FastAPI
from app.routes.auth import router as auth_router  # Importa tu router
from app.db.database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)

# Endpoint de prueba para la raíz
@app.get("/")
def read_root():
    return {
        "message": "API funcionando correctamente 🚀",
        "guia": "Puedes probar la API aquí: /docs (Swagger UI interactivo)",
        "endpoints": {
            "registro": "/auth/register",
            "login": "/auth/login"
        }
    }