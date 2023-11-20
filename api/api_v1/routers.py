from fastapi import APIRouter
from api.api_v1.endpoints import books, authors, clients, borrowed_by_clients
api_router = APIRouter()

api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(authors.router, prefix="/authors", tags=["authors"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(borrowed_by_clients.router, prefix="/borrow", tags=["borrowings"])