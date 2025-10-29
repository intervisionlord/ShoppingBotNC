"""Обработчик отправки запросов к серверу NextCloud"""

from typing import Any, Dict, Optional
import json
from httpx import AsyncClient, BasicAuth, HTTPStatusError, RequestError

from config.settings import settings
from handlers.handler_logging import logger

headers = {
    "OCS-APIRequest": "true",
    "accept": "application/json",
    "Content-Type": "application/json",
}
auth = BasicAuth(username=settings.NC_LOGIN, password=settings.NC_PASSWORD)


async def send_request(
    url: str, method: str, data: Optional[Dict] = None
) -> Optional[Dict[Any, Any]]:
    """Клиент для отправки запросов в API NextCloud"""
    if not url:
        logger.error("Не определен URL!")
        return None

    async with AsyncClient(auth=auth, headers=headers, timeout=30.0) as client:
        try:
            method_upper = method.upper()
            if method_upper == "GET":
                response = await client.get(url=url)
            elif method_upper == "POST":
                response = await client.post(url=url, json=data)
            elif method_upper == "PUT":
                response = await client.put(url=url, json=data)
            elif method_upper == "DELETE":
                response = await client.delete(url=url)
            else:
                logger.error(f"Неподдерживаемый метод: {method}")
                return None

            response.raise_for_status()

            # Пытаемся прочитать ответ как JSON
            try:
                return response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка декодирования JSON от {url}: {e}")
                logger.error(f"Response text: {response.text}")
                return None
            except HTTPStatusError as e:
                logger.error(f"Неожиданная ошибка при обработке ответа от {url}: {e}")
                return None

        except RequestError as err:
            logger.error(f'Ошибка запроса к "{url}": {err}')
            return None
