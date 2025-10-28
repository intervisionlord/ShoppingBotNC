"""Обработчик получения досок"""

from typing import List, Optional

from pydantic import ValidationError

from config.settings import settings
from handlers.handler_logging import logger
from handlers.handler_requests import send_request
from models.model_board import ModelBoard

DECK_ENDPOINT = "/apps/deck/api/v1.0"


async def get_decks() -> Optional[List[ModelBoard]]:
    """
    Получение всех Дэк

    :return: JSON со списком Дэк
    :rtype: List[ModelBoard] | None
    """
    boards_endpoint = f"{settings.NC_URL}{DECK_ENDPOINT}/boards"
    decklist = await send_request(url=boards_endpoint, method="GET")
    if decklist is not None:
        try:
            decks = [ModelBoard(**deck) for deck in decklist]
            return decks
        except ValidationError as err:
            logger.critical(f"Получены невалидные данные: {err}")
    else:
        logger.critical("Данные не получены")
    return None
