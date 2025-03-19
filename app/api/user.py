from fastapi import APIRouter, HTTPException
from app.db.CRUD.user import add_user

router = APIRouter()

@router.post("/register")
def register_user(username: str, password: str, first_name: str, last_name: str, role: str, age: int, weight: float, size: float, vo2max:float, power_max: float, hr_max: float, rf_max: float, cadence_max: float):
    try:
        add_user(username, password, first_name, last_name, role, age, weight, size, vo2max, power_max, hr_max, rf_max, cadence_max)
        return {"message": "Utilisateur ajouté avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))