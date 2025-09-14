from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional,List
import uuid
from sqlstartup import execute_query

router=APIRouter()


class Turf(BaseModel):
    turfid: Optional[str]=None
    turfname: str
    location: str
    timing: str
    ownerid: str
    rating: float

class TurfUpdate(BaseModel):
    turfname: Optional[str] = None
    location: Optional[str] = None
    timing: Optional[str] = None
    ownerid: Optional[str] = None
    rating: Optional[float] = None



turfs_db: List[Turf] = []

@router.post("/turfs",response_model = Turf)
def create_turf(turf: Turf):
    if any(existing_turf.turfname == turf.turfname for existing_turf in turfs_db):
        raise HTTPException(status_code=400, detail="Name already exists")
    turf.turfid=str(uuid.uuid4())
    create_turf_query = """
    INSERT INTO turfs(turfid, turfname, location, timing, ownerid, rating)
    Values(%s,%s,%s,%s,%s,%s)"""
    execute_query(create_turf_query, params=(turf.turfid,turf.turfname,turf.location,turf.timing,turf.ownerid,turf.rating))

    get_turfs_query= """
    SELECT * from turfs
    WHERE turfid=%s
    """
    turf = execute_query(get_turfs_query,params=(turf.turfid,),fetch="one")
    return Turf(**turf)
    turfs_db.append(turf)
    return turf

@router.get("/turfs",response_model=List[Turf])
def get_turfs():
    get_turfs_query= """
    SELECT * from turfs
    """
    turfs = execute_query(get_turfs_query, fetch ="all")
    return[Turf(**turf) for turf in turfs]
    return turfs_db

@router.get("/turfs/{turf_id}",response_model=Turf)
def get_turf(turf_id: str):
    get_turf_query = """
    SELECT * from turfs
    WHERE turfid =%s
    """
    turf = execute_query(get_turf_query,params=(turf_id,),fetch="one")
    if turf:
        return Turf(**turf)
    else:
        raise HTTPException(status_code=404,detail="Turf not found")
    
    for turf in turfs_db:
        if turf.turfid == turf_id:
            return turf
    raise HTTPException(status_code = 404, detail="Turf not found")

@router.put("/turfs/{turf_id}",response_model=Turf)
def update_turf(turf_id: str, turf_update: TurfUpdate):
    get_turf_query = """
    SELECT * from turfs
    WHERE turfid=%s
    """
    turf = execute_query(get_turf_query,params=(turf_id,),fetch="one")
    if turf:
        turfData = Turf(**turf)
        turfname=turfData.turfname
        location = turfData.location
        timing = turfData.timing
        ownerid = turfData.ownerid
        rating = turfData.rating
        if turf_update.turfname is not None:
            if any(turf.turfname == turf_update.turfname and turf.turfid != turf_id for turf in turfs_db):
                raise HTTPException(status_code=400,detail = "Name already exists")
            turfname = turf_update.turfname
        if turf_update.location is not None:
            location = turf_update.location
        if turf_update.timing is not None:
            timing = turf_update.timing
        if turf_update.ownerid is not None:
            ownerid = turf_update.ownerid
        if turf_update.rating is not None:
            rating = turf_update.rating
        
        update_turf_query = """
        Update turfs
        set turfname=%s, location=%s, timing=%s, ownerid=%s, rating=%s
        WHERE turfid=%s
        """

        execute_query(update_turf_query,params=(turfname,location,timing,ownerid,rating,turf_id))
        
        get_turf_query = """
        SELECT * from turfs
        WHERE turfid=%s
        """
        turf = execute_query(get_turf_query,params=(turf_id,),fetch="one")
        if turf:
            turfData = Turf(**turf)
            return turfData
    else:
        raise HTTPException(status_code = 404, detail="Turf not found")


@router.delete("/turfs/{turf_id}")
def delete_turf(turf_id: str):
    delete_turf_query = """
    Delete from turfs
    WHERE turfid = %s
    """
    
    execute_query(delete_turf_query,params=(turf_id,))

    return{"message":"Turf deleted"}
    for tdx, turf in enumerate(turfs_db):
        if turf.turfid == turf_id:
            del turfs_db[tdx]
            return{"message": "Turf deleted"}
    raise HTTPException(status_code=404, detail="Turf not found")
