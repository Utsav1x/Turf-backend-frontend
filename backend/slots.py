from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional,List
import uuid
from sqlstartup import execute_query

router=APIRouter()

class Slots(BaseModel):
    slotid: Optional[str]=None
    datetime: str
    turfid: str
    price: int
    available: bool

class SlotsUpdate(BaseModel):
    datetime: Optional[str] = None
    turfid: Optional[str] = None
    price: Optional[int] = None
    available: Optional[bool] = None

slots_db: List[Slots] = []

@router.post("/slots",response_model=Slots)
def create_slots(slots: Slots):
    slots.slotid=str(uuid.uuid4())
    create_slots_query = """
    INSERT INTO slots (slotid, datetime, turfid, price, available)
    Values(%s,%s,%s,%s,%s)"""
    execute_query(create_slots_query,params=(slots.slotid, slots.datetime,slots.turfid, slots.price,slots.available))

    get_slots_query = """
    SELECT * from slots
    WHERE slotid=%s
    """
    slots = execute_query(get_slots_query,params=(slots.slotid,),fetch="one")
    return Slots(**slots)
    slots_db.append(slots)
    return slots

@router.get("/slots",response_model=List[Slots])
def get_slots():
    get_slots_query= """
    SELECT * from slots
    """
    slots = execute_query(get_slots_query, fetch="all")
    return [Slots(**slots) for slots in slots]
    return slots_db

@router.get("/slots/{slots_id}",response_model=Slots)
def get_slots(slots_id: str):
    get_slots_query = """
    SELECT * from slots
    WHERE slotid=%s
    """
    slots = execute_query(get_slots_query,params=(slots_id,),fetch="one")
    if slots:
        return Slots(**slots)
    else:
        raise HTTPException(status_code = 404, detail="Slot not found")
    for slots in slots_db:
        if slots.slotid == slots_id:
            return slots
    raise HTTPException(status_code=404, detail="Slot not found")

@router.put("/slots/{slots_id}",response_model=Slots)
def update_slots(slots_id: str, slot_update: SlotsUpdate):
    get_slots_query = """
    SELECT * from slots
    WHERE slotid=%s
    """
    slots = execute_query(get_slots_query,params=(slots_id,),fetch="one")
    slotData = Slots(**slots)
    datetime=slotData.datetime
    turfid=slotData.turfid
    price=slotData.price
    available=slotData.available
    if slot_update.datetime is not None:
        datetime = slot_update.datetime
    if slot_update.turfid is not None:
        turfid = slot_update.turfid
    if slot_update.price is not None:
        price = slot_update.price
    if slot_update.available is not None:
        available = slot_update.available

    update_slots_query = """
    Update slots 
    set datetime=%s , turfid=%s , price=%s , available=%s
    where slotid=%s
    """
    execute_query(update_slots_query,params=(datetime, turfid, price, available, slots_id))
    
    get_slots_query = """
    SELECT * from slots
    WHERE slotid=%s
    """
    slots = execute_query(get_slots_query,params=(slots_id,),fetch="one")
    slotData = Slots(**slots)
    return slotData
    

@router.delete("/slots/{slots_id}")
def delete_slot(slots_id: str):
    delete_slots_query = """
    Delete from slots
    Where slotid=%s
    """

    execute_query(delete_slots_query,params=(slots_id,))
    
    return{"message": "Slot deleted"}
    for sdx, slots in enumerate(slots_db):
        if slots.slotid == slots_id:
            del slots_db[sdx]
            return{"message":"Slot removed"}
    raise HTTPException(status_code=404, detail="Slot not found")
    