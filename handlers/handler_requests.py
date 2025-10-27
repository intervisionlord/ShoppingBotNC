"""Обработчик отправки запросов к серверу NextCloud"""

from typing import Any, Dict, Optional

from httpx import AsyncClient, BasicAuth, RequestError

from config.settings import settings
from handlers.handler_logging import logger

headers = {
    "OCS-APIRequest": "true",
    "accept": "application/json",
}
auth = BasicAuth(username=settings.NC_LOGIN, password=settings.NC_PASSWORD)


async def send_request(url: str, method: str) -> Optional[Dict[Any, Any]]:
    """
    Клиент для отправки запросов в API NextCloud

    :param url: Полный адрес вебхука куда отправляются данные
    :type url: str
    :param method: Используемый метод (пока GET / POST)
    :type method: str
    :return: JSON ответа от сервера
    :rtype: Dict[Any, Any] | None
    """
    if not url:
        logger.critical("Не определен URL!")
        return None
    async with AsyncClient(auth=auth, headers=headers) as client:
        try:
            match method.upper():
                case "GET":
                    response = await client.get(url=url)
                case "POST":
                    response = await client.post(url=url)
                case _:
                    logger.critical(f"Неподдерживаемый метод: {method}")
                    return None
            response.raise_for_status()
            return response.json()
        except RequestError as err:
            logger.critical(f'Ошибка запроса к "{settings.NC_URL}": {err}')
    return None
