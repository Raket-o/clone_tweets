"""the main module"""
import os

from asyncpg.exceptions import InvalidCatalogNameError
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from app.api import medias, metrics_grafana, tweets, users
from config_data.config import DB_FILLING
from app.database.connect import Base, engine, session
from app.database.transactions import create_db
from app.utils.filling_data_base import filling_db

appFastAPI = FastAPI()

Instrumentator().instrument(appFastAPI).expose(appFastAPI)

api_router = APIRouter(prefix='/api')

api_router.include_router(medias.router)
api_router.include_router(tweets.router)
api_router.include_router(users.router)

appFastAPI.include_router(metrics_grafana.router)
appFastAPI.include_router(api_router)


@appFastAPI.on_event("startup")
async def startup() -> None:
    """the function is triggered when the application is launched"""
    try:
        async with engine.begin() as conn:
            pass

    except InvalidCatalogNameError:
        await create_db()

    finally:
        if DB_FILLING == "True":
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
            await filling_db()

        else:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)


@appFastAPI.on_event("shutdown")
async def shutdown() -> None:
    """the function is triggered when the application is terminated"""
    print("shutdown")
    await session.close()
    await engine.dispose()
