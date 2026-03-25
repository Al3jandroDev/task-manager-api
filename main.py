# main_debug.py
from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.task import router as task_router
from app.db.database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
        print("✅ Base de datos y tablas creadas correctamente")
    except Exception as e:
        # Capturamos cualquier error en la creación de la DB
        print("❌ Error al crear la base de datos o tablas:")
        print(e)


# Incluimos los routers dentro de un try para ver si fallan
try:
    app.include_router(auth_router)
    app.include_router(task_router)
    print("✅ Routers cargados correctamente")
except Exception as e:
    print("❌ Error al cargar routers:")
    print(e)

# Endpoint raíz de prueba
@app.get("/")
def read_root():
    return {
        "message": "API funcionando correctamente 🚀",
        "guia": "Puedes probar la API aquí: /docs",
        "endpoints": {
            "registro": "/auth/register",
            "login": "/auth/login"
        }
    }