from fastapi import FastAPI
from app.api import authentication, performance, user
from app.init_db import init_create_tables



app = FastAPI(title="CycleTrack", description="API de gestion de club de cyclisme", version="1.0")

tags_metadata = [
    {"name": "Auth", "description": "Routes d'authentification"},
    {"name": "Users", "description": "Gestion des utilisateurs"},
    {"name": "Performances", "description": "Gestion des performance"},
]

app.include_router(authentication.router, prefix="", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(user.router, prefix="/perfs", tags=["Performances"])

@app.on_event("startup")
def startup_event():
    init_create_tables()