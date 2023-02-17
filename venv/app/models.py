from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship



class Flights(Base):
    __tablename__="flights"

    id= Column(Integer , primary_key=True, nullable = False)
    src= Column(String ,nullable = False)
    dest= Column(String ,nullable = False)
    no_of_seats=Column(Integer, nullable =False, server_default='100')
    created_at=Column(TIMESTAMP(timezone=True),nullable = False, server_default= text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")

class User(Base):
    __tablename__="users"
    
    id= Column(Integer , primary_key=True, nullable = False)
    email= Column(String ,nullable = False,unique=True)
    password= Column(String ,nullable = False)
    created_at=Column(TIMESTAMP(timezone=True),nullable = False, server_default= text('now()'))


class Book(Base):
    __tablename__="booking"

    flight_id=Column(Integer,ForeignKey("flights.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)

  

