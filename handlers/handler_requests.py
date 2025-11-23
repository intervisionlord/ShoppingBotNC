"""Обработчик отправки запросов к серверу NextCloud"""

from typing import Any, Dict, Optional
from httpx import AsyncClient, BasicAuth, HTTPStatusError, RequestError

from config.settings import settings
from handlers.handler_logging import logger

TIMEOUT = 20

headers = {
    "OCS-APIRequest": "true",
    "accept": "application/json",
    "Content-Type": "application/json",
}
auth = BasicAuth(username=settings.NC_LOGIN, password=settings.NC_PASSWORD)


async def send_request(
    url: str, method: str, data: Optional[Dict] = None
) -> Optional[Dict[Any, Any]]:
    """
    Клиент для отправки запросов в API NextCloud

    :param url: Полный адрес вебхука куда отправляются данные
    :type url: str
    :param method: Используемый метод (GET/POST/PUT)
    :type method: str
    :param data: Данные для отправки (опционально)
    :type data: Optional[Dict]
    :return: JSON ответа от сервера
    :rtype: Dict[Any, Any] | None
    """
    if not url:
        logger.error("Не определен URL!")
        return None

    async with AsyncClient(auth=auth, headers=headers, timeout=30.0) as client:
        try:
            method_upper = method.upper()
            match method_upper:
                case "GET":
                    response = await client.get(url=url)
                case "POST":
                    response = await client.post(url=url, json=data)
                case "PUT":
                    response = await client.put(url=url, json=data)
                case _:
                    logger.error(f"Неподдерживаемый метод: {method}")
                    return None
            response.raise_for_status()
            return response.json()
        except (RequestError, HTTPStatusError) as error:
            logger.error(f'Ошибка запроса к "{url}" : {error}')
        return None
