from fastapi import APIRouter, HTTPException, status, Depends
from db.CRUD.performance import (
    add_performance, 
    get_performance_by_id, 
    get_all_performances, 
    update_performance, 
    delete_performance,
    get_performances_by_user
)
from schemas.performance import PerformanceCreate, PerformanceRead, PerformanceUpdate

router = APIRouter()

@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_performance(performance: PerformanceCreate):
    """
    Create a new performance record.
    
    This endpoint stores a new performance entry with various metrics in the database.
    
    Parameters:
    ----------
    performance : PerformanceCreate
        Object containing performance metrics including user_id, power_max, vo2_max, 
        hr_max, rf_max, cadence_max, and feeling
    
    Returns:
    -------
    dict
        A success message confirmation
    
    Raises:
    ------
    HTTPException (400)
        If there's an error during the creation process
    """
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
    """
    Retrieve a specific performance by its ID.
    
    Parameters:
    ----------
    performance_id : int
        The unique identifier of the performance record
    
    Returns:
    -------
    PerformanceRead
        The performance data corresponding to the provided ID
    
    Raises:
    ------
    HTTPException (404)
        If the performance with the specified ID is not found
    """
    performance = get_performance_by_id(performance_id=performance_id)
    print(dict(performance))
    if performance is None:
        raise HTTPException(status_code=404, detail="Performance not found")
    return dict(performance)

@router.get("/all", response_model=dict)
def read_all_performances():
    """
    Retrieve all performance records.
    
    Returns:
    -------
    dict
        A dictionary where keys are performance IDs and values are the corresponding 
        performance data
    """
    performances_dict = {}
    for sqliterow in get_all_performances():
        performance = dict(sqliterow)
        performances_dict[performance["id"]] = performance
    return performances_dict

@router.get("/user/{user_id}", response_model=dict)
def get_user_performances(user_id: int):
    """
    Retrieve all performances for a specific user.
    
    Parameters:
    ----------
    user_id : int
        The unique identifier of the user
    
    Returns:
    -------
    dict
        A dictionary where keys are performance IDs and values are the corresponding 
        performance data for the specified user
    """
    performances = get_performances_by_user(user_id)
    
    performances_dict = {}
    for sqliterow in performances:
        performance = dict(sqliterow)
        performances_dict[performance["id"]] = performance
    
    return performances_dict

@router.put("/update/{performance_id}", response_model=PerformanceRead)
def update_performance_endpoint(
    performance_id: int, 
    performance_update: PerformanceUpdate
):
    """
    Update an existing performance record.
    
    Parameters:
    ----------
    performance_id : int
        The unique identifier of the performance to update
    performance_update : PerformanceUpdate
        Object containing the fields to update (power_max, vo2_max, hr_max, rf_max, 
        cadence_max, feeling)
    
    Returns:
    -------
    PerformanceRead
        The updated performance data
    
    Raises:
    ------
    HTTPException (404)
        If the performance with the specified ID is not found
    HTTPException (400)
        If there's an error during the update process
    """
    existing_performance = get_performance_by_id(performance_id=performance_id)
    if existing_performance is None:
        raise HTTPException(status_code=404, detail="Performance not found")
    
    try:
        update_performance(
            performance_id=performance_id,
            power_max=performance_update.power_max,
            vo2_max=performance_update.vo2_max,
            hr_max=performance_update.hr_max,
            rf_max=performance_update.rf_max,
            cadence_max=performance_update.cadence_max,
            feeling=performance_update.feeling
        )
        
        updated_performance = dict(get_performance_by_id(performance_id=performance_id))
        return updated_performance
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating performance: {str(e)}")

@router.delete("/del/{performance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_performance_endpoint(performance_id: int):
    """
    Delete a performance record.
    
    Parameters:
    ----------
    performance_id : int
        The unique identifier of the performance to delete
    
    Returns:
    -------
    None
        Returns no content upon successful deletion
    
    Raises:
    ------
    HTTPException (404)
        If the performance with the specified ID is not found
    HTTPException (400)
        If there's an error during the deletion process
    """
    existing_performance = get_performance_by_id(performance_id=performance_id)
    if existing_performance is None:
        raise HTTPException(status_code=404, detail="Performance not found")
    try:
        delete_performance(performance_id=performance_id)
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting performance: {str(e)}")