from db.session import Base
from sqlalchemy import Column, String, Integer


class Hello(Base):
    __table__ = "hello"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
