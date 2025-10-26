import os

import uvicorn

from config.settings import settings
from handlers.handler_logging import logger
from handlers.handler_server import server_app

if __name__ == "__main__":
    logger.info("🚀 Сервер запускается")
    logger.info(f"📍 Хост: {settings.HOST}, Порт: {settings.PORT}")
    logger.info(f"🌐 WEBHOOK_HOST: {settings.WEBHOOK_HOST or 'не установлен'}")

    ssl_keyfile = settings.SSL_KEY_PATH
    ssl_certfile = settings.SSL_CERT_PATH
    SSL_ENABLED = False

    if settings.SSL_ENABLED:
        if os.path.exists(ssl_keyfile) and os.path.exists(ssl_certfile):
            SSL_ENABLED = True
            logger.info("🔐 SSL сертификаты найдены, запуск с HTTPS")
        else:
            logger.warning("⚠️ SSL сертификаты не найдены, запуск с HTTP")

    uvicorn.run(
        server_app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        access_log=True,
        ssl_keyfile=ssl_keyfile if SSL_ENABLED else None,
        ssl_certfile=ssl_certfile if SSL_ENABLED else None,
    )
