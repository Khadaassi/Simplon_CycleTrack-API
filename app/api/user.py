from fastapi import APIRouter, HTTPException, status, Depends
from db.CRUD.user import add_user, get_user_by_id, get_all_users, update_user, delete_user
from schemas.user import UserCreate, UserRead, UserUpdate
from core.security import get_current_user

router = APIRouter()
public_router = APIRouter()

@public_router.post("/register")
def register_user(user: UserCreate, status_code=status.HTTP_201_CREATED):
    """
    Register a new user in the system.
    
    This endpoint creates a new user account with personal and performance metrics.
    
    Parameters:
    ----------
    user : UserCreate
        User data including username, password, personal details (first_name, last_name, role, age, 
        weight, size) and performance metrics (vo2max, power_max, hr_max, rf_max, cadence_max)
    
    Returns:
    -------
    dict
        A success message confirmation
    
    Raises:
    ------
    HTTPException (400)
        If there's an error during the registration process
    """
    try:
        add_user(
            user.username, user.password, user.first_name, user.last_name, user.role,
            user.age, user.weight, user.size, user.vo2max, user.power_max,
            user.hr_max, user.rf_max, user.cadence_max
        )
        return {"message": "Utilisateur ajouté avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get/{user_id}", response_model=UserRead)
def read_user(user_id: int):
    """
    Retrieve a user by their ID.
    
    Parameters:
    ----------
    user_id : int
        The unique identifier of the user
    
    Returns:
    -------
    UserRead
        The user data corresponding to the provided ID
    
    Raises:
    ------
    HTTPException (404)
        If the user with the specified ID is not found
    """
    user = get_user_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

@router.get("/self", response_model=UserRead)
def read_self_user(current_user = Depends(get_current_user)):
    """
    Retrieve the currently authenticated user's information.
    
    Parameters:
    ----------
    current_user : dict
        The current authenticated user (provided by the dependency)
    
    Returns:
    -------
    UserRead
        The authenticated user's data
    
    Raises:
    ------
    HTTPException (404)
        If the user is not found
    """
    user = dict(get_user_by_id(user_id=current_user))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/all")
def read_all_users():
    """
    Retrieve all users in the system.
    
    Returns:
    -------
    dict
        A dictionary where keys are usernames and values are the corresponding user data
    """
    users = dict()
    for sqliterow in get_all_users():
        user = dict(sqliterow)
        users[user["username"]] = user
    return users

@router.put("/update/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id: int, user_update: UserUpdate):
    """
    Update an existing user.
    
    Parameters:
    ----------
    user_id : int
        The unique identifier of the user to update
    user_update : UserUpdate
        Object containing the fields to update (username, password, personal details, 
        and performance metrics)
    
    Returns:
    -------
    UserRead
        The updated user data
    
    Raises:
    ------
    HTTPException (404)
        If the user with the specified ID is not found
    HTTPException (400)
        If there's an error during the update process
    """
    existing_user = get_user_by_id(user_id=user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        update_user(
            user_id=user_id,
            username=user_update.username,
            password=user_update.password,
            first_name=user_update.first_name,
            last_name=user_update.last_name,
            role=user_update.role,
            age=user_update.age,
            weight=user_update.weight,
            size=user_update.size,
            vo2max=user_update.vo2max,
            power_max=user_update.power_max,
            hr_max=user_update.hr_max,
            rf_max=user_update.rf_max,
            cadence_max=user_update.cadence_max
        )
        
        updated_user = dict(get_user_by_id(user_id=user_id))
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int):
    """
    Delete a user from the system.
    
    Parameters:
    ----------
    user_id : int
        The unique identifier of the user to delete
    
    Returns:
    -------
    None
        Returns no content upon successful deletion
    
    Raises:
    ------
    HTTPException (404)
        If the user with the specified ID is not found
    HTTPException (400)
        If there's an error during the deletion process
    """
    existing_user = get_user_by_id(user_id=user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        delete_user(user_id=user_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting user: {str(e)}")