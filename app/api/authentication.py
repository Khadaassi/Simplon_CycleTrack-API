from fastapi import APIRouter, HTTPException
from schemas.user import UserConnection
from db.CRUD.user import get_user_by_username
from core.security import verify_token, create_access_token, verify_password

router = APIRouter()

@router.post("/login")
def login(user: UserConnection):
    """
    Authenticate a user and generate an access token.
    
    This endpoint verifies user credentials and returns a JWT access token if authentication is successful.
    
    Parameters:
    ----------
    user : UserConnection
        User credentials containing username and password
        
    Returns:
    -------
    dict
        A dictionary containing the access token and token type
        
    Raises:
    ------
    HTTPException (401)
        If the user is not registered or the password is incorrect
    """
    db_user = dict(get_user_by_username(user.username))
    if db_user is None:
        raise HTTPException(status_code=401, detail="This user is not registered")
    
    # If the password is incorrect
    elif not verify_password(user.password, db_user["password"]):  
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Generate an access token
    token = create_access_token({"sub": user.username})
    
    return {"access_token": token, "token_type": "bearer"}

