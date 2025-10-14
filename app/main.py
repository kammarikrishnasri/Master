# app/main.py
import os
from fastapi import FastAPI
from app.configurations.database import Base, engine
from app.api.routes import user_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Registration API")
app.include_router(user_router.router)

PORT = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
