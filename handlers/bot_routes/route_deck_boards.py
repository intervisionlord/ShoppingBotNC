"""Обработчик для работы с досками"""

from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_boards

KBD_COLUMNS = 1


class NavigationCallback(CallbackData, prefix="nav"):
    """Универсальный callback для навигации по доскам и стекам"""

    screen: str  # 'boards_list', 'stacks_list', 'cards_list'
    target_id: int = 0  # ID доски или стека


async def show_boards_command(message: types.Message) -> None:
    """
    Показывает список досок в виде инлайн-кнопок

    :param message: Сообщение от пользователя
    :type message: types.Message

    Пользователь -> /decks ->
    Бот показывает кнопки с досками
    """
    logger.info(f"Пользователь {message.from_user.id} запросил список досок")
    decks = await get_boards()

    if not decks:
        await message.answer("❌ Доски не найдены")
        return

    keyboard_builder = InlineKeyboardBuilder()

    for deck in decks:
        keyboard_builder.button(
            text=f"🗂️ {deck.title}",
            callback_data=NavigationCallback(screen="stacks_list", target_id=deck.id),
        )

    keyboard_builder.adjust(KBD_COLUMNS)

    await message.answer(
        "🗃️ <b>Выберите доску:</b>",
        reply_markup=keyboard_builder.as_markup(),
        parse_mode="HTML",
    )
