from fastapi import FastAPI, Request, HTTPException
from handlers.handler_logging import logger
from handlers.handler_bot import setup_webhook, close_bot_session
from config.settings import settings

# Формируем URL вебхука
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = (
    f"{settings.WEBHOOK_HOST}:{settings.PORT}{WEBHOOK_PATH}"
    if settings.WEBHOOK_HOST
    else None
)

app = FastAPI(title="ShoppingBot API", version="0.0.1.0")


# Импортируем и регистрируем роутеры внутри функции чтобы избежать циклических импортов
def setup_routes():
    from routes.base_routes import base_router as api_base_router
    from routes.webhook_routes import webhook_router as api_webhook_router

    app.include_router(api_base_router)
    app.include_router(api_webhook_router)


# Настраиваем роутеры при создании приложения
setup_routes()


@app.on_event("startup")
async def on_startup():
    logger.info(f"Сервер запущен на {settings.HOST}:{settings.PORT}")

    if WEBHOOK_URL and WEBHOOK_URL.startswith("https://"):
        try:
            await setup_webhook(WEBHOOK_URL)
            logger.info(f"Вебхук установлен: {WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"Ошибка установки вебхука: {e}")
    else:
        logger.warning("Вебхук не настроен (требуется HTTPS)")


@app.on_event("shutdown")
async def on_shutdown():
    await close_bot_session()
    logger.info("Сервер остановлен")


@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
)
async def catch_all(request: Request, path: str):
    """Обработчик для всех несуществующих путей"""
    raise HTTPException(status_code=404, detail="Endpoint not found")


server_app = app
