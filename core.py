"""Создание и конфигурация FastAPI приложения"""

from fastapi import FastAPI

from config.settings import settings
from routes.routes_base import base_router
from routes.routes_webhook import webhook_router


def create_application() -> FastAPI:
    """Создание и настройка FastAPI приложения"""
    application = FastAPI(
        title="ShoppingBot API",
        version=settings.VERSION,
        description="API для Telegram Shopping Bot",
    )

    # Регистрируем роутеры
    application.include_router(base_router)
    application.include_router(webhook_router)

    return application
