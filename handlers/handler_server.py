"""Обработчик настройки и запуска сервера"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from config.settings import settings
from core import create_application
from handlers.handler_bot import bot
from handlers.handler_logging import logger

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = (
    f"{settings.WEBHOOK_HOST}:{settings.PORT}{WEBHOOK_PATH}"
    if settings.WEBHOOK_HOST
    else None
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan manager"""
    await startup()
    yield
    await shutdown()


async def startup() -> None:
    """Все операции запуска"""
    logger.success(f"Сервер запущен на {settings.HOST}:{settings.PORT}")
    await bot.initialize()
    await bot.setup_webhook(WEBHOOK_URL)


async def shutdown() -> None:
    """Все операции остановки"""
    await bot.close()
    logger.info("Сервер остановлен")


app = create_application()
app.router.lifespan_context = lifespan


@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
)
async def catch_all(request: Request, path: str):
    """Обработчик для всех несуществующих путей"""
    del request, path
    raise HTTPException(status_code=404, detail="Endpoint not found")


server_app = app
