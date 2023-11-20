from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Book(BaseModel):
    __tablename__ = "books"

    title = Column(String, index=True)
    year = Column(Integer, index=True)
    publisher = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books', uselist=False)
    borrowed_by_clients = relationship("BorrowedByClient", back_populates="book")

class Author(BaseModel):
    __tablename__ = "authors"

    fullname = Column(String, index=True)
    books = relationship('Book', back_populates='author')

class Client(BaseModel):
    __tablename__ = "clients"
    
    username = Column(String, index=True, unique=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    sex = Column(String, index=True)
    password = Column(String(255), nullable=False)

    borrowed_by_clients = relationship("BorrowedByClient", back_populates="client")

class BorrowedByClient(BaseModel):
    __tablename__ = "borrowed_by_clients"

    borrow_date = Column(Date)
    return_date = Column(Date)
    client_id = Column(ForeignKey("clients.id", ondelete="CASCADE"))
    book_id = Column(ForeignKey("books.id", ondelete="CASCADE"))
    
    client = relationship("Client", back_populates="borrowed_by_clients")
    book = relationship("Book", back_populates="borrowed_by_clients")