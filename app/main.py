from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.admin_router import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication Service"
)

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(admin_router)

@app.get("/")
def root():
    return {
        "message": "Authentication API is running"
    }