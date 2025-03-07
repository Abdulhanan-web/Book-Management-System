from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import Sessionlocal, engine
from models import Base, Books
from schemas import BookCreate


# Initialize Database
Base.metadata.create_all(bind=engine)


# Initialize FastAPI App
app = FastAPI()


# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Jinja2 Templates
templates = Jinja2Templates(directory="templates")


# Dependency to get the database session
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    books = db.query(Books).all()
    return templates.TemplateResponse("index.html", {"request": request, "Books": books})

# Add Book Page
@app.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

# Add Book POST
@app.post("/add")
def add_book(Title: str = Form(...), Author: str = Form(...), Genre: str = Form(...), Price: float = Form(...), PublicationYear: str = Form(...), db: Session = Depends(get_db)):
    new_book = Books(Title=Title, Author=Author, Genre=Genre, Price=Price, PublicationYear=PublicationYear)
    db.add(new_book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# ✏️ Edit Book Page
@app.get("/edit/{book_id}")
def edit_page(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = db.query(Books).filter(Books.id == book_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "book": book})

# ✏️ Edit Book - POST
@app.post("/edit/{book_id}")
def edit_Book(book_id: int, Title: str = Form(...), Author: str = Form(...), Genre: str = Form(...), Price: float = Form(...), PublicationYear: str = Form(...), db: Session = Depends(get_db)):
    db_books = db.query(Books).filter(Books.id == book_id).first()
    db_books.Title = Title
    db_books.Author = Author
    db_books.Genre = Genre
    db_books.Price = Price
    db_books.PublicationYear = PublicationYear
    db.commit()
    return RedirectResponse(url="/", status_code=303)


# 🗑 Delete Book
@app.get("/delete/{book_id}")
def delete_item(book_id: int, db: Session = Depends(get_db)):
    db_books = db.query(Books).filter(Books.id == book_id).first()
    db.delete(db_books)
    db.commit()
    return RedirectResponse(url="/", status_code=303)