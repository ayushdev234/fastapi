from sqlalchemy.orm import Session
#ther is status code as pe the response
from fastapi import Depends,Response,HTTPException,status
import schemas,models,hashing

def create(request:schemas.Blog, db:Session):
    new_blog = models.Blog(title = request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def all(db: Session):
    #One object of models.Blog = represents one row in that table.
    blogs = db.query(models.Blog).all()
    return blogs


def get_data(id,response:Response,db: Session):
    #response_model=schemas.showblog expect a single row not list
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"details":f"file not found of id={id}"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"file not found of id={id}")
    return blogs
#Automatic Status Code Management: When you raise an HTTPException in FastAPI with a specific status code (like 404, 400, etc.), FastAPI automatically sets that status code in the response.



def destroy(id, db: Session):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"file not found of id={id}")
    db.query(models.Blog).filter(models.Blog.id ==id).delete(synchronize_session=False)
    db.commit()
    return 'done'




def update(id, request: schemas.Blog,db:Session):
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