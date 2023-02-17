from fastapi import APIRouter,status,HTTPException,Depends,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils,oauth2
router = APIRouter( tags=['Authentication'])


@router.post("/login",response_model=schemas.Token)
def login(user_info : OAuth2PasswordRequestForm=Depends() , db : Session=Depends(get_db)):
    req_user=db.query(models.User).filter(user_info.username==models.User.email).first()
    if not req_user:
        raise HTTPException(status_code=403,detail=f"User not found"  )
    if not utils.verify(user_info.password,req_user.password):
        raise HTTPException(status_code=403,detail=f"User not found"  )
    
    access_token= oauth2.create_access_token( data={"user_id": req_user.id} )

    return {"access_token": access_token, "token_type":"bearer"}

