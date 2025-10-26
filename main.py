import uvicorn
from handlers.handler_server import server_app
from handlers.handler_logging import logger
from config.settings import settings
import os

if __name__ == "__main__":
    logger.info("🚀 Сервер запускается")
    logger.info(f"📍 Хост: {settings.HOST}, Порт: {settings.PORT}")
    logger.info(
        f"🔑 BOT_TOKEN: {'установлен' if settings.BOT_TOKEN else 'НЕ УСТАНОВЛЕН'}"
    )
    logger.info(f"🌐 WEBHOOK_HOST: {settings.WEBHOOK_HOST or 'не установлен'}")

    ssl_keyfile = settings.SSL_KEY_PATH
    ssl_certfile = settings.SSL_CERT_PATH
    ssl_enabled = False

    if settings.SSL_ENABLED:
        if os.path.exists(ssl_keyfile) and os.path.exists(ssl_certfile):
            ssl_enabled = True
            logger.info("🔐 SSL сертификаты найдены, запуск с HTTPS")
        else:
            logger.warning("⚠️ SSL сертификаты не найдены, запуск с HTTP")

    uvicorn.run(
        server_app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        access_log=True,
        ssl_keyfile=ssl_keyfile if ssl_enabled else None,
        ssl_certfile=ssl_certfile if ssl_enabled else None,
    )
