from fastapi import APIRouter
import schemas,models,hashing
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import Depends,Response,HTTPException
from typing import List
from fastapi import status


# why response if we have return:
#Validates outgoing data
#Protects sensitive fields(like password)
def create(request:schemas.user,db_user:Session):
    new_user=models.user(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db_user.add(new_user)
    db_user.commit()
    db_user.refresh(new_user)
    return new_user


def get_user(id:int, db: Session) :
    user = db.query(models.user).filter(models.user.id==id).first()
    if not user:
        raise HTTPException(status_code=status. HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    return user