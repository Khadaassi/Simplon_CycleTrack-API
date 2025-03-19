from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    role: str
    age: Optional[int] = None
    weight: Optional[float] = None
    size: Optional[float] = None
    vo2max: Optional[float] = None
    power_max: Optional[float] = None
    hr_max: Optional[float] = None
    rf_max: Optional[float] = None
    cadence_max: Optional[float] = None

class UserRead(BaseModel):
    id: int 
    username: str
    first_name: str
    last_name: str
    role: str
    age: Optional[int] = None
    weight: Optional[float] = None
    size: Optional[float] = None
    vo2max: Optional[float] = None
    power_max: Optional[float] = None
    hr_max: Optional[float] = None
    rf_max: Optional[float] = None
    cadence_max: Optional[float] = None

class UserConnection(BaseModel):
    """
    Schema for user authentication (login).

    This schema is used when a user tries to log in by providing their username and password.
    """
    username: str  # username of the user
    password: str  # Plain text password for login