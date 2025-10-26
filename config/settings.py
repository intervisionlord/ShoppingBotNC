from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Конфигурация приложения"""

    # Токен бота Telegram
    BOT_TOKEN: Optional[str] = Field(None, description="Токен бота от @BotFather")

    # Настройки сервера
    HOST: str = Field("0.0.0.0", description="Хост для запуска сервера")
    PORT: int = Field(8443, description="Порт для запуска сервера")

    # SSL
    SSL_ENABLED: bool = Field(False, description="Использование локального SSL")
    SSL_KEY_PATH: Optional[str] = Field(None, description="Ключ сертификата")
    SSL_CERT_PATH: Optional[str] = Field(None, description="Сертификат")

    # Настройки вебхука (опционально для продакшена)
    WEBHOOK_HOST: Optional[str] = Field(None, description="Публичный URL для вебхука")

    # Настройки логирования
    LOG_LEVEL: str = Field("INFO", description="Уровень логирования")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Создаем глобальный экземпляр настроек
settings = Settings()
