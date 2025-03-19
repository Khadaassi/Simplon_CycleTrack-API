from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PerformanceBase(BaseModel):
    user_id: int
    power_max: float
    vo2_max: float
    hr_max: float
    rf_max: float
    cadence_max: float
    feeling: Optional[str] = None

class PerformanceCreate(PerformanceBase):
    pass

class PerformanceRead(PerformanceBase):
    id: int
    created_at: datetime  # Supposant que votre table a une colonne timestamp

class PerformanceUpdate(BaseModel):
    power_max: Optional[float] = None
    vo2_max: Optional[float] = None
    hr_max: Optional[float] = None
    rf_max: Optional[float] = None
    cadence_max: Optional[float] = None
    feeling: Optional[str] = None