from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import router
from src.store import health_check
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Health check
    logger.info("Performing health check...")
    health: bool = health_check()
    if not health:
        logger.error("Health check failed. Exiting...")
        raise RuntimeError("Health check failed.")
    logger.info("Health check passed.")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
