import asyncio
from httpx import (
    AsyncClient,
    BasicAuth,
    HTTPStatusError,
    ConnectError,
    ConnectTimeout,
    ReadTimeout,
    NetworkError,
)
from config.settings import settings
from handlers.handler_logging import logger


headers = {
    "OCS-APIRequest": "true",
    "accept": "application/json",
}

auth = BasicAuth(username=settings.NC_LOGIN, password=settings.NC_PASSWORD)

DECK_ENDPOINT = "/apps/deck/api/v1.0"


async def get_decks_in_workspace():
    BOARD_ENDPOINT = f"{settings.NC_URL}{DECK_ENDPOINT}/boards"
    async with AsyncClient(auth=auth, headers=headers) as client:
        try:
            response = await client.get(url=BOARD_ENDPOINT)
            response.raise_for_status()
        except HTTPStatusError as err:
            logger.error(f"Ошибка статуса: {err}")
        except ConnectError:
            logger.error(
                f"Не удалось установить соединение с сервером {settings.NC_URL}"
            )
        except ConnectTimeout:
            logger.error(f"Таймаут от сервера {settings.NC_URL}")
        except ReadTimeout:
            logger.error(f"Таймаут при чтении ответа {settings.NC_URL}")
        except NetworkError as err:
            logger.error(f"Ошибка сети: {err}")
    return response.json()
