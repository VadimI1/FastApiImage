from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    path = Column(String)
    data = Column(String)
    permission = Column(String)
    size = Column(String)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    email = Column(String)
    password = Column(String)