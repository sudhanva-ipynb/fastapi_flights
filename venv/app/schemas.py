from datetime import datetime
from pydantic import BaseModel,EmailStr, conint
from typing import Optional
class FlightBase(BaseModel):  #api specification (pydantic)
    no_of_seats: Optional[int] = None
    src: str
    dest: str

class FlightCreate(FlightBase):
    pass
class UserOut(BaseModel):
    email : EmailStr
    id : int
    created_at: datetime
    class Config:
        orm_mode =True

class Flight(FlightBase):
    id: int  
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode =True

# class FlightOut(FlightBase):
#     flights : Flight
#     bookings: int

#     class Config:
#         orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str



class UserLogin(BaseModel):
    email : EmailStr
    password : str 


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id  : Optional[str]= None

class Book(BaseModel):
    flight_id : int
    dir : conint(le=1)
