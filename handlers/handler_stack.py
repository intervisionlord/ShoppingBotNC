from config.settings import settings
from handlers.handler_logging import logger
from handlers.handler_requests import send_request
from models.model_card import Stack

NC_API_BASE = "/apps/deck/api/v1.0"


async def get_stack() -> Stack | None:
    webhook_url = f"{settings.NC_URL}{NC_API_BASE}/boards/{settings.DECK_BOARD_ID}/stacks/{settings.DECK_STACK_ID}"
    stack_data = await send_request(url=webhook_url, method="get")
    if stack_data is not None:
        logger.success("Данные по стеку получены")
        stack = Stack(**stack_data)
        return stack
    else:
        logger.error("Данные по стеку не получены")
    return None
