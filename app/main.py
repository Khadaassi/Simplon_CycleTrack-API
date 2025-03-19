from fastapi import FastAPI
from app.api import authentication, performance, user



app = FastAPI(title="CycleTrack", description="API de gestion de club de cyclisme", version="1.0")

tags_metadata = [
    {"name": "Auth", "description": "Routes d'authentification"},
    {"name": "Users", "description": "Gestion des utilisateurs"},
    {"name": "Performances", "description": "Gestion des performance"},
]

app.include_router(authentication.router, prefix="", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(user.router, prefix="/perfs", tags=["Performances"])