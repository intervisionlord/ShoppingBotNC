"""Обработчик настройки и запуска сервера"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from config.settings import settings
from core import create_application
from handlers.handler_bot import BOT_INSTANCE, close_bot_session, setup_webhook
from handlers.handler_logging import logger

# Формируем URL вебхука
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = (
    f"{settings.WEBHOOK_HOST}:{settings.PORT}{WEBHOOK_PATH}"  # noqa: E231
    if settings.WEBHOOK_HOST
    else None
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan manager для управления событиями приложения"""
    # Startup
    logger.success(f"Сервер запущен на {settings.HOST}:{settings.PORT}")  # noqa: E231

    if WEBHOOK_URL and WEBHOOK_URL.startswith("https://"):
        try:
            await setup_webhook(WEBHOOK_URL)
            if BOT_INSTANCE:
                webhook_info = await BOT_INSTANCE.get_webhook_info()
                logger.info(f"Статус вебхука: {webhook_info.url}")
                logger.info(
                    f"Ожидающие обновления: {webhook_info.pending_update_count}"
                )

        except Exception as err:  # pylint: disable=broad-except
            logger.error(f"Ошибка установки вебхука: {err}")
    else:
        logger.warning("Вебхук не настроен (требуется HTTPS)")

    yield

    # Shutdown
    await close_bot_session()
    logger.info("Сервер остановлен")


# Создаем приложение с lifespan
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
