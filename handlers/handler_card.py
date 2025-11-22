from config.settings import settings
from handlers.handler_logging import logger
from handlers.handler_requests import send_request
from models.model_card import Card

NC_API_BASE = "/apps/deck/api/v1.0"


async def get_card(card_id: int) -> Card | None:
    webhook_url = (
        f"{settings.NC_URL}{NC_API_BASE}/boards/"
        f"{settings.DECK_BOARD_ID}/stacks/"
        f"{settings.DECK_STACK_ID}/cards/{card_id}"
    )
    card_data = await send_request(url=webhook_url, method="get")
    if card_data is not None:
        logger.success("Данные по карточке получены")
        card = Card(**card_data)
        return card
    else:
        logger.error("Данные по карточке не получены")
    return None
