from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
"""ForeignKey — table name.

relationship — class name.

back_populates — match the attribute name in the other class."""
class Blog(Base):
    __tablename__='blogs'
    id= Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

    def update(self, request):
        self.title = request.title
        self.body = request.body

    creator=relationship("user",back_populates="blogs")
    user_id=Column(Integer,ForeignKey('users.id'))
class user(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)
    blogs=relationship('Blog',back_populates="creator")