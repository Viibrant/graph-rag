from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from loguru import logger

from src.api import router
from src.store import health_check


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Health check
    logger.info("Performing health check...")
    health: dict[str, bool] = health_check()
    logger.debug(f"Health check results: {health}")
    if not all(health.values()):
        logger.error("Health check failed. Exiting...")
        raise RuntimeError("Health check failed.")
    logger.info("Health check passed.")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
