from fastapi import FastAPI, Depends
from api import authentication, performance, user
from init_db import init_create_tables
from core.security import get_current_user



app = FastAPI(title="CycleTrack", description="API de gestion de club de cyclisme", version="1.0")

tags_metadata = [
    {"name": "Auth", "description": "Routes d'authentification"},
    {"name": "Users", "description": "Gestion des utilisateurs"},
    {"name": "Public Users", "description": "Création d'utilisateurs"},
    {"name": "Performances", "description": "Gestion des performance"},
]

app.include_router(authentication.router, prefix="", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)])
app.include_router(user.public_router, prefix="/users", tags=["Public Users"])
app.include_router(performance.router, prefix="/perfs", tags=["Performances"], dependencies=[Depends(get_current_user)])

@app.on_event("startup")
def startup_event():
    init_create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)