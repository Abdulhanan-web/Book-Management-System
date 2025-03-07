from pydantic import BaseModel

class BookCreate(BaseModel):
    Title: str
    Author: str
    Genre: str
    Price: float
    PublicationYear: str

class ResponseItem(BookCreate):
    id: int

    class Config:
        from_attributes = True
