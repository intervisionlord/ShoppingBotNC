"""Файл настроек приложения"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация приложения"""

    VERSION: str = "v.:0.0.3.0"

    # Токен бота Telegram
    BOT_TOKEN: Optional[str] = Field(None, description="Токен бота от @BotFather")

    # Настройки сервера
    HOST: str = "0.0.0.0"
    PORT: int = 8443

    # SSL
    SSL_ENABLED: bool = False
    SSL_KEY_PATH: Optional[str] = None
    SSL_CERT_PATH: Optional[str] = None

    # Настройки вебхука
    WEBHOOK_HOST: Optional[str] = None

    # Настройки NextCloud Deck
    NC_URL: Optional[str] = Field(None, description="Адрес Nextcloud")
    NC_LOGIN: Optional[str] = Field(None, description="Логин Nextcloud")
    NC_PASSWORD: Optional[str] = Field(None, description="Пароль Nextcloud")

    # ID доски и стека для списка покупок
    DECK_BOARD_ID: int = 1
    DECK_STACK_ID: int = 1

    # Настройки логирования
    LOG_LEVEL: str = "INFO"

    class Config:
        """Конфигурация Pydantic"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
