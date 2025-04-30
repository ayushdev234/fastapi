from fastapi import APIRouter
import schemas,models,hashing
from router import token
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Depends,Response,HTTPException
from typing import List
from fastapi import status
from repository import blog,user


router=APIRouter(
    tags=["Authentication"]
)

@router.post('/login')

def login(request:OAuth2PasswordRequestForm = Depends() ,db:Session=Depends(get_db)):
    user=db.query(models.user).filter(models.user.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no user")
    if not hashing.Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"wrong password")
    
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token":access_token, "token_type":"bearer"}