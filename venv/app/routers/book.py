from fastapi import Response,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2
from ..database import engine,get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/book",
    tags=["Booking"]
)

@router.post("/",status_code=201)
def book(booking: schemas.Book, db: Session= Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    isflight=db.query(models.Flights).filter(models.Flights.id==booking.flight_id).first()
    if not isflight:
        raise HTTPException(status_code=404,detail=f"Flight with id {booking.flight_id} not found")
    book_query= db.query(models.Book).filter(models.Book.flight_id == booking.flight_id , models.Book.user_id==current_user.id)
    found_booking=book_query.first()
    if booking.dir:
        if found_booking:
            raise HTTPException(status_code=409 , detail=f"User {current_user.id} has already booked  the flight {found_booking.flight_id}")
        new_booking=models.Book(flight_id=booking.flight_id,user_id=current_user.id)
        db.add(new_booking)
        db.commit()
        return {"message":"Booking Successful"}

    else:
        if not found_booking:
            raise HTTPException(status_code=404 , detail=f"Booking not found")
        book_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Booking  Cancelled"}

