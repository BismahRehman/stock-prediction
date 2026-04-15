
# app/main.py

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.model.user import User

from app.routes.user import router as user_router
from app.routes.google_auth import router as google_router
from app.routes.prediction import router as prediction_router
from app.routes.history import router as history_router
from app.routes.stripe import router as stripe_router
from app.routes.admin import router as admin_router

from app.config import settings
from app.service.auth import hash_password


app = FastAPI()


# ---------------------------
# Routers
# ---------------------------
app.include_router(user_router)
app.include_router(google_router)
app.include_router(prediction_router)
app.include_router(history_router)
app.include_router(stripe_router)
app.include_router(admin_router)


# ---------------------------
# Startup event (NO create_all)
# ---------------------------
@app.on_event("startup")
async def on_startup():
    async with AsyncSessionLocal() as db:
        await create_default_admin(db)


# ---------------------------
# Admin seeder
# ---------------------------
async def create_default_admin(db: AsyncSession):

    result = await db.execute(
        select(User).where(User.email == settings.ADMIN_EMAIL)
    )

    admin = result.scalar_one_or_none()

    if admin:
        return

    new_admin = User(
        email=settings.ADMIN_EMAIL,
        hashed_password=hash_password(settings.ADMIN_PASSWORD),
        role="admin"
    )

    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)


# ---------------------------
# Root endpoint
# ---------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Predictor API!"}