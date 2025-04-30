from fastapi import FastAPI
import schemas,models
from database import engine
from  router import blog,user,authentication

app=FastAPI()


models.Base.metadata.create_all(engine)


#router
#"Handles API routes — what should happen when a URL is called (like GET /users)."
#Example: When someone visits /users, this tells what response to give.
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
