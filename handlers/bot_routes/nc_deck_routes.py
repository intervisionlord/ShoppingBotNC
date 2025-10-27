from aiogram import Router, types
from aiogram.filters import Command

from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_decks_in_workspace
from models.model_board import ModelBoard

nc_deck_router = Router()


@nc_deck_router.message(Command("decks"))
async def get_decks(message: types.Message):
    logger.info(f"Запрошен список карточек пользователем {message.from_user.id}")
    decks_json = await get_decks_in_workspace()
    decks = [ModelBoard.model_validate(deck) for deck in decks_json]
    await message.answer(
        f"Доступные списки: {', '.join([deck.title for deck in decks])}"  # TODO: Дебаг
    )
