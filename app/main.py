from app.database import SessionLocal
from fastapi import FastAPI
from router import router as tasks_router

app = FastAPI(
    title="Forms App")
app.include_router(tasks_router)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
