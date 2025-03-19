from fastapi import APIRouter, HTTPException, status, Depends
from app.db.CRUD.performance import (
    add_performance, 
    get_performance_by_id, 
    get_all_performances, 
    update_performance, 
    delete_performance
)
from app.schemas.performance import PerformanceCreate, PerformanceRead, PerformanceUpdate

router = APIRouter()

@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_performance(performance: PerformanceCreate):
    try:
        add_performance(
            user_id=performance.user_id,
            power_max=performance.power_max,
            vo2_max=performance.vo2_max,
            hr_max=performance.hr_max,
            rf_max=performance.rf_max,
            cadence_max=performance.cadence_max,
            feeling=performance.feeling
        )
        return {"message": "Performance ajoutée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get/{performance_id}", response_model=PerformanceRead)
def read_performance(performance_id: int):
    performance = get_performance_by_id(performance_id=performance_id)
    if performance is None:
        raise HTTPException(status_code=404, detail="Performance not found")
    return dict(performance)

@router.get("/all", response_model=dict)
def read_all_performances():
    performances_dict = {}
    for sqliterow in get_all_performances():
        performance = dict(sqliterow)
        performances_dict[performance["id"]] = performance
    return performances_dict

@router.put("/update/{performance_id}", response_model=PerformanceRead)
def update_performance_endpoint(
    performance_id: int, 
    performance_update: PerformanceUpdate
):
    # Vérifier si la performance existe
    existing_performance = get_performance_by_id(performance_id=performance_id)
    if existing_performance is None:
        raise HTTPException(status_code=404, detail="Performance not found")
    
    try:
        # Appeler la fonction de mise à jour
        update_performance(
            performance_id=performance_id,
            power_max=performance_update.power_max,
            vo2_max=performance_update.vo2_max,
            hr_max=performance_update.hr_max,
            rf_max=performance_update.rf_max,
            cadence_max=performance_update.cadence_max,
            feeling=performance_update.feeling
        )
        
        # Récupérer et retourner la performance mise à jour
        updated_performance = dict(get_performance_by_id(performance_id=performance_id))
        return updated_performance
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating performance: {str(e)}")

@router.delete("/del/{performance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_performance_endpoint(performance_id: int):
    # Vérifier si la performance existe
    existing_performance = get_performance_by_id(performance_id=performance_id)
    if existing_performance is None:
        raise HTTPException(status_code=404, detail="Performance not found")
    
    try:
        # Appeler la fonction de suppression
        delete_performance(performance_id=performance_id)
        
        # Retourner une réponse sans contenu (204 No Content)
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting performance: {str(e)}")