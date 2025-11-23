"""Обработчик для работы с карточками списка покупок"""

from typing import List, Optional
from config.settings import settings
from handlers.handler_logging import logger
from handlers.handler_requests import send_request
from models.model_card import ModelCard

DECK_ENDPOINT = "/apps/deck/api/v1.0/boards"


async def get_shopping_cards() -> Optional[List[ModelCard]]:
    """
    Получение карточек из стека списка покупок

    :return: Список карточек или None при ошибке
    :rtype: Optional[List[ShoppingCard]]
    """
    base_url = f"{settings.NC_URL}{DECK_ENDPOINT}"
    stacks_endpoint = f"{base_url}/{settings.DECK_BOARD_ID}/stacks"

    stacks_data = await send_request(url=stacks_endpoint, method="GET")

    if not stacks_data:
        logger.error("Не удалось получить данные стеков")
        return None

    target_stack = next(
        (stack for stack in stacks_data if stack.get("id") == settings.DECK_STACK_ID),
        None,
    )

    if not target_stack:
        logger.error(f"Стек {settings.DECK_STACK_ID} не найден")
        return None

    cards_data = target_stack.get("cards", [])
    cards = []

    for card_data in cards_data:
        try:
            shopping_card = ModelCard(
                id=card_data.get("id", 0),
                title=card_data.get("title", ""),
                description=card_data.get("description"),
                stack_id=card_data.get("stackId", 0),
            )
            cards.append(shopping_card)
        except Exception as error:
            logger.warning(
                f"Ошибка преобразования карточки {card_data.get('id')}: {error}"
            )
            continue

    logger.info(f"Успешно загружено {len(cards)} карточек")
    return cards


async def update_card_description(card_id: int, description: str) -> bool:
    """
    Обновление описания карточки

    :param card_id: ID карточки для обновления
    :type card_id: int
    :param description: Новое описание карточки
    :type description: str
    :return: True если обновление успешно, иначе False
    :rtype: bool
    """
    base_url = f"{settings.NC_URL}{DECK_ENDPOINT}"
    card_endpoint = (
        f"{base_url}/{settings.DECK_BOARD_ID}/stacks/"
        f"{settings.DECK_STACK_ID}/cards/{card_id}"
    )

    # Получаем текущие данные карточки для сохранения всех полей
    card_data = await send_request(url=card_endpoint, method="GET")
    if not card_data:
        logger.error(f"Не удалось получить данные карточки {card_id}")
        return False

    # Обновляем только описание, сохраняя остальные поля
    update_data = {**card_data, "description": description}
    result = await send_request(url=card_endpoint, method="PUT", data=update_data)

    if result:
        logger.info(f"Карточка {card_id} успешно обновлена")
        return True

    logger.error(f"Ошибка обновления карточки {card_id}")
    return False
