from sqlalchemy import Column,Integer,String
from database import Base

class Users(Base):
    __tablename__='user'

