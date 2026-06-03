from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.auth import router as auth_router

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FlowSpace API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "database_configured": bool(settings.DATABASE_URL)}
