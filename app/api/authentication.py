from fastapi import APIRouter, HTTPException
from app.schemas.user import UserConnection
from app.db.CRUD.user import get_user_by_username
from app.core.security import verify_token, create_access_token, verify_password

router = APIRouter()

@router.post("/login")
def login(user: UserConnection):
    db_user = dict(get_user_by_username(user.username))
    if db_user is None:
        raise HTTPException(status_code=401, detail="This user is not registered")
    
    # If the password is incorrect
    elif not verify_password(user.password, db_user["password"]):  
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Generate an access token
    token = create_access_token({"sub": user.username})
    
    return {"access_token": token, "token_type": "bearer"}

