"""Обработчик получения досок и данных в них"""

from typing import List, Optional

from pydantic import ValidationError

from config.settings import settings
from handlers.handler_logging import logger
from handlers.handler_requests import send_request
from models.model_board import ModelBoard
from models.model_stack import ModelStack

DECK_ENDPOINT = "/apps/deck/api/v1.0/boards"


async def get_boards() -> Optional[List[ModelBoard]]:
    """
    Получение всех Дэк

    :return: JSON со списком Дэк
    :rtype: List[ModelBoard] | None
    """
    boards_endpoint = f"{settings.NC_URL}{DECK_ENDPOINT}"
    decklist = await send_request(url=boards_endpoint, method="GET")
    if decklist is not None:
        try:
            decks = [ModelBoard(**deck) for deck in decklist]
            return decks
        except ValidationError as err:
            logger.critical(f"Получены невалидные данные: {err}")
    else:
        logger.critical("Данные по доскам не получены")
    return None


async def get_stacks(board_id: int) -> Optional[List[ModelStack]]:
    """
    Получение стеков в доске

    :param board_id: ID доски
    :type board_id: int
    :return: Список стеков в доске
    :rtype: List[ModelStack] | None
    """
    if board_id is not None:
        stacks_endpoint = f"{settings.NC_URL}{DECK_ENDPOINT}/{board_id}/stacks"
        stacklist = await send_request(url=stacks_endpoint, method="GET")
        if stacklist is not None:
            try:
                stacks = [ModelStack(**stack) for stack in stacklist]
                return stacks
            except ValidationError as err:
                logger.critical(f"Получены невалидные данные: {err}")
        else:
            logger.critical("Данные по стекам не получены")
    else:
        logger.critical('"board_id" не задан')
    return None
