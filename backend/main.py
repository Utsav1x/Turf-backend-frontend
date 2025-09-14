from fastapi import FastAPI
from user import router as user_router 
from turf import router as turf_router
from slots import router as slots_router
from booking import router as booking_router
from sqlstartup import execute_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:5500"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def create_tables_users():
    create_tableuser_query = """
    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        number INT, 
        type VARCHAR(255)
    )
    """

    execute_query(create_tableuser_query)
    create_tables_turfs()
    create_tables_slots()
    create_tables_booking()

def create_tables_turfs():
    create_tableturf_query = """
    CREATE TABLE IF NOT EXISTS turfs (
        turfid VARCHAR(255) PRIMARY KEY,
        turfname VARCHAR(255),
        location VARCHAR(255),
        timing VARCHAR(255),
        ownerid VARCHAR(255), 
        rating FLOAT
    )
    """

    execute_query(create_tableturf_query)

def create_tables_slots():
    create_tableslot_query = """
    CREATE TABLE IF NOT EXISTS slots (
        slotid VARCHAR(255) PRIMARY KEY,
        datetime VARCHAR(255),
        turfid VARCHAR(255),
        price INT, 
        available BOOL
    )
    """
    execute_query(create_tableslot_query) 

def create_tables_booking():
    create_tablebooking_query = """
    CREATE TABLE IF NOT EXISTS booking (
        bookingid VARCHAR(255) PRIMARY KEY,
        userid VARCHAR(255),
        slotid VARCHAR(255),
        bookingtime VARCHAR(255),
        paymentmethod VARCHAR(255),
        paymentdonestatus BOOL, 
        approved BOOL   
    )
    """

    execute_query(create_tablebooking_query) 

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user_router)
app.include_router(turf_router)
app.include_router(slots_router)
app.include_router(booking_router)