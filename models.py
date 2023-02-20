from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    hashed_pwd = Column(String(1024))
    mail = Column(String(255))
    phno = Column(Integer)