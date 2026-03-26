# main_debug.py
from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.task import router as task_router
from app.db.database import create_db_and_tables

# Create FastAPI application instance
app = FastAPI()


# STARTUP EVENT
@app.on_event("startup")
def on_startup():
    """
    Event triggered when the application starts.

    Responsibilities:
    - Initialize the database
    - Create tables if they do not exist
    """
    try:
        create_db_and_tables()
        print(" Database and tables created successfully")
    except Exception as e:
        # Catch and log any database initialization errors
        print("Error while creating database or tables:")
        print(e)


# REGISTER ROUTERS
try:
    # Register authentication routes (/auth)
    app.include_router(auth_router)

    # Register task routes (/tasks)
    app.include_router(task_router)
    print("Routers loaded successfully")
except Exception as e:
    # Catch errors if routers fail to load
    print("Error loading routers:")
    print(e)

# ROOT ENDPOINT
@app.get("/")
def read_root():
    """
    Root endpoint for basic API health check.
    Useful for:
    - Verifying the API is running
    - Providing quick documentation links
    """
    return {
        "message": "API is running successfully",
        "guide": "You can test the API here: /docs",
        "endpoints": {
            "register": "/auth/register",
            "login": "/auth/login"
        }
    }