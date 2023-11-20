from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import settings
from utils.database import create_tables
from api.api_v1.routers import api_router
from utils.database import database

def init_app():
    create_tables()

    app = FastAPI(
        title=settings.PROJECT_NAME, 
        description=settings.PROJECT_DESC, 
        version=settings.API_v1_STR
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    @app.on_event("startup")
    async def startup():
        await database.connect()


    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()
    
    app.include_router(router=api_router, prefix=settings.API_v1_STR)
    
    return app