from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PerformanceBase(BaseModel):
    user_id: int
    power_max: float = Field(..., gt=0)
    vo2_max: float = Field(..., gt=0)
    hr_max: float = Field(..., gt=0)
    rf_max: float = Field(..., gt=0)
    cadence_max: float = Field(..., gt=0)
    feeling: Optional[int] = Field(None, ge=0, le=10)

class PerformanceCreate(PerformanceBase):
    pass

class PerformanceRead(PerformanceBase):
    id: int
    date: str

class PerformanceUpdate(BaseModel):
    power_max: Optional[float] = Field(None, gt=0)
    vo2_max: Optional[float] = Field(None, gt=0)
    hr_max: Optional[float] = Field(None, gt=0)
    rf_max: Optional[float] = Field(None, gt=0)
    cadence_max: Optional[float] = Field(None, gt=0)
    feeling: Optional[int] = Field(None, ge=0, le=10)