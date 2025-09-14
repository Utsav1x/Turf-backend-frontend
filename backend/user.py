from typing import Optional,List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import uuid
from sqlstartup import execute_query

router = APIRouter()

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    password: str
    number: int
    type: str

class UserUpdate(BaseModel):
    name: Optional[str]= None
    email: Optional[str] = None

users_db: List[User] = []


@router.post("/users",response_model = User)
def create_user(user: User):
    if any(existing_user.email == user.email for existing_user in users_db):
        raise HTTPException(status_code=400, detail="Email already exists")
    user.id=str(uuid.uuid4())
    create_users_query ="""
    INSERT INTO  users (id, name, email, password, number, type)
    Values(%s, %s, %s, %s, %s, %s)"""
    execute_query(create_users_query, params=(user.id, user.name, user.email, user.password, user.number, user.type))

    get_users_query= """
    SELECT * from users
    WHERE id=%s
    """
    user = execute_query(get_users_query, params=(user.id,), fetch="one")
    return User(**user)
    
@router.get("/users",response_model=List[User])
def get_users():
    get_users_query= """
    SELECT * from users
    """
    users = execute_query(get_users_query, fetch="all")
    return [User(**user) for user in users]

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    get_user_query = """
    SELECT * from users
    WHERE id=%s
    """
    user = execute_query(get_user_query,params=(user_id,),fetch="one")
    if user:
        return User(**user)
    else:
        raise HTTPException(status_code = 404, detail="User not found")
    # print(user_id)
    # for user in users_db:
    #     print(user.id)
    #     if user.id == user_id:
    #         return user
    # raise HTTPException(status_code = 404, detail="User not found")
    
@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user_update: UserUpdate):
    get_user_query = """
    SELECT * from users
    WHERE id=%s
    """
    user = execute_query(get_user_query,params=(user_id,),fetch="one")
    userData = User(**user)
    name = userData.name
    email = userData.email
    if user_update.name is not None:
        name = user_update.name
    if user_update.email is not None:
        email = user_update.email

    update_user_query = """
    Update users 
    set email=%s , name=%s
    where id=%s
    """
    execute_query(update_user_query,params=(email, name, user_id))

    get_user_query = """
    SELECT * from users
    WHERE id=%s
    """
    user = execute_query(get_user_query,params=(user_id,),fetch="one")
    userData = User(**user)
    return userData
    

    
@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    delete_user_query = """
    Delete from users
    Where id=%s
    """

    execute_query(delete_user_query,params=(user_id,))
    
    return{"message": "User deleted"}

