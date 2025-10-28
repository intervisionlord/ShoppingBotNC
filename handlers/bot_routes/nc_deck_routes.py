"""Обработчик отображения доступных досок"""

from aiogram import Router, types
from aiogram.filters import Command

from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_decks

nc_deck_router = Router()


@nc_deck_router.message(Command("decks"))
async def command_get_decks(message: types.Message) -> None:
    """
    Отправляет в ответ список доступных досок

    :param message: Ответное сообщение
    :type message: types.Message
    """
    logger.info(
        f"Запрошен список досок пользователем {message.from_user.id} "
        f"({message.from_user.username})"
    )
    decks = await get_decks()
    if decks is not None:
        await message.answer(
            "<b>🗃️ Доступные доски:</b>\n\n"
            f"{'\n'.join([f'    🗂️ {deck.title}' for deck in decks])}",
            parse_mode="HTML",
        )
    else:
        await message.answer("❌ Доски отсутствуют или не получены")
