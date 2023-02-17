from typing import List
from fastapi import Response,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from ..database import engine,get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/sqlalchemy/users",
    tags=['Users'])

'''
@router.get("/",response_model=List[schemas.UserOut])
def get_all(db: Session= Depends(get_db)):
    all_data=db.query(models.User).all()
    return all_data
'''

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int,db: Session= Depends(get_db)):
     data= db.query(models.User).filter(models.User.id==id).first()
     if not data:
        raise HTTPException(status_code=404,detail=f"User with id: {id} not found"  )

     return data

@router.post("/",status_code = 201,response_model=schemas.UserOut)     
def add_user(user: schemas.UserCreate, db: Session= Depends(get_db)):

    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.dict())  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
   
    return new_user

@router.delete("/{id}")
def delete_user(id: int,db: Session= Depends(get_db)):
     data= db.query(models.User).filter(models.User.id==id)
     if not data.first():
        raise HTTPException(status_code=404,detail=f"User with id: {id} not found"  )
     data.delete(synchronize_session=False)
     db.commit()

     return Response(status_code=204) 


@router.put("/{id}",response_model=schemas.UserOut)
def update_user(user: schemas.UserCreate ,id: int,db: Session= Depends(get_db)):
     data= db.query(models.User).filter(models.User.id==id)
     if not data.first():
        raise HTTPException(status_code=404,detail=f"User with id: {id} not found"  )
     data.update(user.dict(),synchronize_session=False)
     db.commit()
     
     return  data.first()
