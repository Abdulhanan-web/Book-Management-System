from sqlalchemy import Column, Integer, String, Float
from database import Base

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String, index=True)
    Author = Column(String, index=True)
    Genre = Column(String, index=True)
    Price = Column(Float, index=True)
    PublicationYear = Column(String, index=True)
