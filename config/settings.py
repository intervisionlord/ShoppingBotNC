"""Файл настроек приложения"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация приложения"""

    VERSION: str = Field("0.0.3.0")

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

    # Настройки NextCloud Deck
    NC_URL: Optional[str] = Field(None, description="Адрес Nextcloud")
    NC_LOGIN: Optional[str] = Field(None, description="Логин Nextcloud")
    NC_PASSWORD: Optional[str] = Field(None, description="Пароль Nextcloud")

    # ID доски и стека для списка покупок
    DECK_BOARD_ID: int = Field(1, description="ID доски для списка покупок")
    DECK_STACK_ID: int = Field(1, description="ID стека для списка покупок")

    # Настройки логирования
    LOG_LEVEL: str = Field("INFO", description="Уровень логирования")

    class Config:  # pylint: disable=R0903
        """Конфигурация Pydantic"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
