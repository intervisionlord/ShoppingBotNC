"""Базовые API эндпоинты приложения"""

from fastapi import APIRouter

# Создаем роутер для базовых API эндпоинтов
base_router = APIRouter(tags=["base"])


@base_router.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "ShoppingBot API работает",
        "status": "ok",
        "endpoints": {"api": "/api", "health": "/api/health", "test": "/api/test"},
    }


@base_router.get("/api")
async def api_root():
    """Корневой эндпоинт API"""
    return {"message": "API работает", "status": "ok"}


@base_router.get("/api/health")
async def health_check():
    """Проверка здоровья сервера"""
    return {"status": "healthy", "service": "ShoppingBot API", "version": "1.0.0"}


@base_router.get("/api/test")
async def api_test():
    """Тестовый эндпоинт"""
    return {"message": "API тест пройден!", "endpoint": "/api/test"}


@base_router.get("/favicon.ico")
async def favicon():
    """Обработка favicon запросов"""
    return {"message": "No favicon"}
