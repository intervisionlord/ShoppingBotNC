from fastapi import FastAPI
from routes.routes_base import base_router
from routes.routes_webhook import webhook_router


def create_application() -> FastAPI:
    """Создание и настройка FastAPI приложения"""
    application = FastAPI(
        title="ShoppingBot API",
        version="1.0.0",
        description="API для Telegram Shopping Bot",
    )

    # Регистрируем роутеры
    application.include_router(base_router)
    application.include_router(webhook_router)

    return application
