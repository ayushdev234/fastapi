from fastapi import APIRouter
import schemas,models,hashing,oauth2
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import Depends,Response,HTTPException
from typing import List
from fastapi import status
from repository import blog,user

router=APIRouter()

router = APIRouter(
    prefix="/user",
    tags=['user']
    #prefix and tags has been passed to all path parameter associated with router
)

"""The User class automatically registers itself with Base.metadata when Python loads the file.
When you call create_all(engine_user), SQLAlchemy looks inside Base.metadata for all registered models and tries to create those tables in the database connected via engine_user."""
models.Base.metadata.create_all(engine)



@router.post('/',response_model=schemas.showuser)
def create(request:schemas.user,db_user:Session=Depends(get_db),current_user: schemas.user = Depends(oauth2.get_current_user)):
    return user.create(request,db_user)

@router.get('/{id}', response_model=schemas.showuser)
def get_user(id:int, db: Session=Depends(get_db),current_user: schemas.user = Depends(oauth2.get_current_user)) :
    return user.get_user(id,db)