from fastapi import APIRouter
import schemas,models,hashing,oauth2
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
#ther is status code as pe the response
from fastapi import Depends,Response,HTTPException
#we explict change the response insted of implict one
from typing import List
from fastapi import status


from repository import blog,user

router=APIRouter()


#router is used to reduce code, proper strucure 
router = APIRouter(
    prefix="/blog",
    tags=['blog']
    #prefix and tags has been passed to all path parameter associated with router
)

@router.post('/')
#Depends() --->> dependecy injection
#You don't manually create the database session inside your function.
#✅ You don't manually close/destroy the database session inside your function.
def create(request:schemas.Blog, db:Session=Depends(get_db),current_user: schemas.user = Depends(oauth2.get_current_user)):
    return blog.create(request,db)


@router.get('/',status_code=status.HTTP_201_CREATED,response_model=List[schemas.showblog])
def all(db: Session = Depends(get_db),current_user: schemas.user = Depends(oauth2.get_current_user)):
    return blog.all(db)



#we need to have .all(),.first() somening after db.query(models.Blog)
@router.get('/{id}',status_code=status.HTTP_302_FOUND,response_model=schemas.showblog)
def get_data(id,response:Response,db: Session = Depends(get_db),current_user: schemas.user = Depends(oauth2.get_current_user)):
    return blog.get_data(id,response,db)


@router.delete('/{id}', status_code=status. HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db),current_user: schemas.user = Depends(oauth2.get_current_user)):
    return blog.destroy(id,db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog,db:Session = Depends (get_db),current_user: schemas.user = Depends(oauth2.get_current_user)):
    return blog.update(id,request,db)

