from fastapi import APIRouter, HTTPException
from app.db.CRUD.user import add_user
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate):
    try:
        add_user(
            user.username, user.password, user.first_name, user.last_name, user.role,
            user.age, user.weight, user.size, user.vo2max, user.power_max,
            user.hr_max, user.rf_max, user.cadence_max
        )
        return {"message": "Utilisateur ajouté avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))