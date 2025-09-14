from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional,List
import uuid
from sqlstartup import execute_query

router=APIRouter()

class Booking(BaseModel):
    bookingid: Optional[str]=None
    userid: str
    slotid: str
    bookingtime: str
    paymentmethod: str
    paymentdonestatus: bool
    approved: bool

class BookingUpdate(BaseModel):
    userid: Optional[str]=None
    slotid: Optional[str]=None
    bookingtime: Optional[str]=None
    paymentmethod: Optional[str]=None
    paymentdonestatus: Optional[bool]=None
    approved: Optional[bool]=None

booking_db: List[Booking] = []

@router.post("/booking", response_model=Booking)
def create_booking(booking: Booking):
    booking.bookingid=str(uuid.uuid4())
    create_booking_query = """
    INSERT INTO booking(bookingid, userid, slotid, bookingtime, paymentmethod, paymentdonestatus, approved)
    Values(%s,%s,%s,%s,%s,%s,%s)"""
    execute_query(create_booking_query, params=(booking.bookingid,booking.userid,booking.slotid,booking.bookingtime,booking.paymentmethod,booking.paymentdonestatus,booking.approved))


    get_booking_query= """
    SELECT * from booking
    WHERE bookingid=%s
    """
    booking = execute_query(get_booking_query,params=(booking.bookingid,),fetch="one")
    return Booking(**booking)
    booking_db.append(booking)
    return booking

@router.get("/booking",response_model=List[Booking])
def get_booking():
    get_booking_query= """
    SELECT * from booking
    """
    booking = execute_query(get_booking_query, fetch="all")
    return [Booking(**booking) for booking in booking]
    return booking_db

@router.get("/booking/{booking_id}",response_model=Booking)
def get_booking(booking_id: str):
    get_booking_query = """
    SELECT * from booking
    WHERE bookingid=%s
    """
    booking = execute_query(get_booking_query,params=(booking_id,),fetch="one")
    if booking:
        return Booking(**booking)
    else:
        raise HTTPException(status_code = 404, detail="Booking not found")
    for booking in booking_db:
        if booking.bookingid == booking_id:
            return booking
    raise HTTPException(status_code=404, detail="Booking not found")

@router.put("/booking/{booking_id}",response_model=Booking)
def update_booking(booking_id: str,booking_update: BookingUpdate):
    get_booking_query = """
    SELECT * from booking
    WHERE bookingid=%s
    """
    booking = execute_query(get_booking_query,params=(booking_id,),fetch="one")
    bookingData = Booking(**booking)
    userid=bookingData.userid
    slotid=bookingData.slotid
    bookingtime=bookingData.bookingtime
    paymentmethod=bookingData.paymentmethod
    paymentdonestatus=bookingData.paymentdonestatus
    approved=bookingData.approved
    if booking_update.userid is not None:
        userid = booking_update.userid
    if booking_update.slotid is not None:
        slotid = booking_update.slotid
    if booking_update.bookingtime is not None:
        bookingtime = booking_update.bookingtime
    if booking_update.paymentmethod is not None:
        paymentmethod = booking_update.paymentmethod
    if booking_update.paymentdonestatus is not None:
        paymentdonestatus = booking_update.paymentdonestatus
    if booking_update.approved is not None:
        approved = booking_update.approved
    
    update_booking_query = """
    Update booking 
    set userid=%s , slotid=%s , bookingtime=%s , paymentmethod=%s, paymentdonestatus=%s, approved=%s
    where bookingid=%s
    """
    execute_query(update_booking_query,params=(userid, slotid, bookingtime, paymentmethod, paymentdonestatus, approved, booking_id))
    
    get_booking_query = """
    SELECT * from booking
    WHERE bookingid=%s
    """
    booking = execute_query(get_booking_query,params=(booking_id,),fetch="one")
    bookingData = Booking(**booking)
    return bookingData


@router.delete("/booking/{booking_id}")
def delete_booking(booking_id: str):
    delete_booking_query = """
    Delete from booking
    Where bookingid=%s
    """

    execute_query(delete_booking_query,params=(booking_id,))
    
    return{"message": "Booking removed"}
    for bdx, booking in enumerate(booking_db):
        if booking.bookingid == booking_id:
            del booking_db[bdx]
            return{"message":"Booking removed"}
    raise HTTPException(status_code=404, detail="Booking not found")


