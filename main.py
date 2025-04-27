from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
app=FastAPI()

""" fast api check the path line by line , 
if it gets matching decorator first it gives
output as per that
change position of blog/unpublisded with 
blod/id to see difference
place static above dynamic"""

@app.get('/blog')
#path paramete in function only
#query parameter change the strucure fo output 
#for same page/path
def index(limit=10, published: bool=True, sort: Optional[str]=None):
# only get 10 published blogs
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}
@app.get("/")
def read_root():
    return {"Hello":"World"}


@app.get("/about") #path 
def read_item():
    return {'data':"about page"}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

@app.get('/blog/{id}')
def show(id: int):
# fetch blog with id = id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id):
# fetch comments of blog with id = id
    return {'data': {'1', '2'}}

# @app.get("/items/{id}/{q}") #path parameter
# def read_item(id:int,q:str=None): #query parameter
#     return {q:id}

class Blog (BaseModel):
    title: str
    body: str
    published: Optional [bool]
@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f"Blog is created with title as {blog.title}"}

# if __name__=="__main__":
#     uvicorn.run(app,host="127.0.0.1", port=9000)