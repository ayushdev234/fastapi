from fastapi import FastAPI
from pydantic import BaseModel
import schemas,models
from fastapi import status
#ther is status code as pe the response
from fastapi import Depends,Response,HTTPException
#we explict change the response insted of implict one
from database import engine,SessionLocal
from sqlalchemy.orm import Session
app=FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(engine)
@app.post('/blog')

#Depends() --->> dependecy injection
#You don't manually create the database session inside your function.
#✅ You don't manually close/destroy the database session inside your function.
def create(request:schemas.Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title= request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog',status_code=status.HTTP_201_CREATED)
def all(db: Session = Depends(get_db)):
    #One object of models.Blog = represents one row in that table.
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_302_FOUND)
def get_data(id,response:Response,db: Session = Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).all()
    if not blogs:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"details":f"file not found of id={id}"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"file not found of id={id}")
    return blogs
#Automatic Status Code Management: When you raise an HTTPException in FastAPI with a specific status code (like 404, 400, etc.), FastAPI automatically sets that status code in the response.

@app.delete('/blog/{id}', status_code=status. HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"file not found of id={id}")
    db.query(models. Blog).filter(models.Blog.id ==id).delete(synchronize_session=False)
    db.commit()
    return 'done'