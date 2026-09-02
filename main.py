"""
Application Root Entrypoint.
"""
import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.APP_NAME} on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=False)
