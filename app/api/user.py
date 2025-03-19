from fastapi import APIRouter, HTTPException, status
from app.db.CRUD.user import add_user, get_user_by_id
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, status_code=status.HTTP_201_CREATED):
    try:
        add_user(
            user.username, user.password, user.first_name, user.last_name, user.role,
            user.age, user.weight, user.size, user.vo2max, user.power_max,
            user.hr_max, user.rf_max, user.cadence_max
        )
        return {"message": "Utilisateur ajouté avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int):
    user = dict(get_user_by_id(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user