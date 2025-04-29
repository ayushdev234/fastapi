from fastapi import FastAPI
from pydantic import BaseModel
import schemas,models,hashing
from hashing import Hash
from typing import List
from fastapi import status
from sqlalchemy.orm import joinedload
#ther is status code as pe the response
from fastapi import Depends,Response,HTTPException
#we explict change the response insted of implict one
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app=FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(engine)
@app.post('/blog',tags=['blog'])
#Depends() --->> dependecy injection
#You don't manually create the database session inside your function.
#✅ You don't manually close/destroy the database session inside your function.
def create(request:schemas.Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title = request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog',status_code=status.HTTP_201_CREATED,response_model=List[schemas.showblog],tags=['blog'])
def all(db: Session = Depends(get_db)):
    #One object of models.Blog = represents one row in that table.
    blogs = db.query(models.Blog).all()
    return blogs
#we need to have .all(),.first() somening after db.query(models.Blog)
@app.get('/blog/{id}',status_code=status.HTTP_302_FOUND,response_model=schemas.showblog,tags=['blog'])
def get_data(id,response:Response,db: Session = Depends(get_db)):
    #response_model=schemas.showblog expect a single row not list
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"details":f"file not found of id={id}"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"file not found of id={id}")
    return blogs
#Automatic Status Code Management: When you raise an HTTPException in FastAPI with a specific status code (like 404, 400, etc.), FastAPI automatically sets that status code in the response.

@app.delete('/blog/{id}', status_code=status. HTTP_204_NO_CONTENT,tags=['blog'])
def destroy(id, db: Session = Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"file not found of id={id}")
    db.query(models.Blog).filter(models.Blog.id ==id).delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['blog'])
def update(id, request: schemas.Blog,db:Session = Depends (get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" Blog with id {id} not found")
    #explicit menitoned update function
    blog.update(request)
    # blog.title = request.title
    # blog.body = request.body
    db.commit()
    db.refresh(blog)
    return 'updated'


"""The User class automatically registers itself with Base.metadata when Python loads the file.
When you call create_all(engine_user), SQLAlchemy looks inside Base.metadata for all registered models and tries to create those tables in the database connected via engine_user."""
models.Base.metadata.create_all(engine)
@app.post('/user',response_model=schemas.showuser,tags=['user'])
# why response if we have return:
#Validates outgoing data
#Protects sensitive fields(like password)
def create(request:schemas.user,db_user:Session=Depends(get_db)):
    new_user=models.user(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db_user.add(new_user)
    db_user.commit()
    db_user.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.showuser,tags=['user'])
def get_user(id:int, db: Session=Depends(get_db)) :
    user = db.query(models.user).filter(models.user.id==id).first()
    if not user:
        raise HTTPException(status_code=status. HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    return user