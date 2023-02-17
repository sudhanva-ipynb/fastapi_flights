from typing import List,Optional
from fastapi import Response,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
import json

router = APIRouter(
   prefix="/sqlalchemy/flights",
   tags=['Flights'])


@router.get("/")
def get_all_flights( db: Session= Depends(get_db),limit: int = 10,skip: int=0,src: Optional[str]="",dest: Optional[str]=""):
#    all_data=db.query(models.Flights).filter(models.Flights.src.contains(src)).filter(models.Flights.dest.contains(dest)).limit(limit).offset(skip).all()
    results=db.query(models.Flights, func.count(models.Book.flight_id).label("bookings")).join(models.Book, models.Book.flight_id==models.Flights.id,isouter=True).group_by(models.Flights.id)
    print(results)
    return results.all()

@router.get("/{id}")
def get_flight(id: int,db: Session= Depends(get_db)):
     data=db.query(models.Flights).filter(models.Flights.id==id).first()
     if not data:
        raise HTTPException(status_code=404,detail=f"Flight with id: {id} not found"  )

     return data



@router.post("/",status_code = 201,response_model=schemas.Flight)     
def add_flight(flight: schemas.FlightCreate, db: Session= Depends(get_db),current_user : int = Depends(
    oauth2.get_current_user)):
   print(current_user.email)
   added_flight=models.Flights(owner_id=current_user.id, **flight.dict())  
   db.add(added_flight)
   db.commit() 
   db.refresh(added_flight)
   
   return added_flight


@router.delete("/{id}")
def delete_flight(id: int,db: Session= Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
     data_query= db.query(models.Flights).filter(models.Flights.id==id)
     data=data_query.first()
     if not data:
        raise HTTPException(status_code=404,detail=f"Flight with id: {id} not found"  )
     if data.owner_id != current_user.id:
         raise HTTPException(status_code=403 , detail= "Unauthorized operation")
     data_query.delete(synchronize_session=False)
     db.commit()

     return Response(status_code=204) 

@router.put("/{id}",response_model=schemas.Flight)
def update_flight(flight: schemas.FlightCreate ,id: int,db: Session= Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
     data_query= db.query(models.Flights).filter(models.Flights.id==id)
     data=data_query.first()
     if not data:
        raise HTTPException(status_code=404,detail=f"Flight with id: {id} not found"  )
     if data.owner_id != current_user.id:
         raise HTTPException(status_code=403 , detail= "Unauthorized operation")
     data_query.update(flight.dict(),synchronize_session=False)
     db.commit()
     
     return  data.first()
