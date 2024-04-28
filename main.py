from fastapi import FastAPI
from app.routers.users_router import router as users_router
from app.routers.forms_router import router as forms_router

app = FastAPI(
    title="Forms App")

app.include_router(users_router)
app.include_router(forms_router)
