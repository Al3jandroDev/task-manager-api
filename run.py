# RUN SERVER (standalone)
import uvicorn

if __name__ == "__main__":
    """
    This allows running the FastAPI app directly with:
        python run.py
    Instead of using `uvicorn main:app --reload`.

    Parameters:
    - app: "main:app" → points to FastAPI instance in main.py
    - host: "127.0.0.1" → localhost
    - port: 8000 → default development port
    - reload: False → disables auto-reload (set True in dev if desired)
    """
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)