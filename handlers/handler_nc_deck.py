"""Обработчик для работы с карточками списка покупок"""

from typing import List, Optional
from config.settings import settings
from handlers.handler_logging import logger
from handlers.handler_requests import send_request
from models.model_card import ShoppingCard

DECK_ENDPOINT = "/apps/deck/api/v1.0/boards"


async def get_shopping_cards() -> Optional[List[ShoppingCard]]:
    """Получение карточек из стека списка покупок"""
    try:
        stacks_endpoint = (
            f"{settings.NC_URL}{DECK_ENDPOINT}/{settings.DECK_BOARD_ID}/stacks"
        )
        stacks_data = await send_request(url=stacks_endpoint, method="GET")

        if not stacks_data:
            logger.error("Не удалось получить данные стеков")
            return None

        target_stack = next(
            (
                stack
                for stack in stacks_data
                if stack.get("id") == settings.DECK_STACK_ID
            ),
            None,
        )

        if not target_stack:
            logger.error(f"Стек {settings.DECK_STACK_ID} не найден")
            return None

        cards_data = target_stack.get("cards", [])
        if not cards_data:
            logger.info("В стеке нет карточек")
            return []

        cards = []
        for card_data in cards_data:
            try:
                card = ShoppingCard(
                    id=card_data.get("id", 0),
                    title=card_data.get("title", ""),
                    description=card_data.get("description"),
                    stack_id=card_data.get("stackId", 0),
                )
                cards.append(card)
            except Exception as e:
                logger.warning(
                    f"Ошибка преобразования карточки {card_data.get('id')}: {e}"
                )
                continue

        logger.info(f"Успешно загружено {len(cards)} карточек")
        return cards

    except Exception as e:
        logger.error(f"Ошибка получения карточек: {e}")
        return None


async def update_card_description(card_id: int, description: str) -> bool:
    """Основная функция обновления карточки"""
    try:
        card_endpoint = (
            f"{settings.NC_URL}{DECK_ENDPOINT}/"
            f"{settings.DECK_BOARD_ID}/stacks/"
            f"{settings.DECK_STACK_ID}/cards/{card_id}"
        )

        # Получаем текущие данные карточки
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
        else:
            logger.error(f"Ошибка обновления карточки {card_id}")
            return False

    except Exception as e:
        logger.error(f"Ошибка при обновлении карточки {card_id}: {e}")
        return False
