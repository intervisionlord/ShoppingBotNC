"""Обработчик для работы со стеками"""

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.bot_routes.route_deck_boards import (
    NavigationCallback,
    show_boards_command,
)
from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_stacks

KBD_COLUMNS = 1


async def show_stacks_for_board(
    callback: types.CallbackQuery, callback_data: NavigationCallback
) -> None:
    """
    Показывает стеки выбранной доски

    :param callback: Callback от нажатой кнопки в предыдущем меню
    :type callback: types.CallbackQuery
    :param callback_data: Данные callback'а
    :type callback_data: NavigationCallback

    Пользователь нажимает на кнопку доски ->
    Бот показывает кнопки со стеками этой доски
    """
    board_id = callback_data.target_id
    logger.info(f"Пользователь {callback.from_user.id} выбрал доску {board_id}")
    stacks = await get_stacks(board_id)

    if not stacks:
        await callback.message.edit_text("❌ Стеки не найдены для этой доски")
        await callback.answer()
        return

    keyboard_builder = InlineKeyboardBuilder()

    for stack in stacks:
        keyboard_builder.button(
            text=f"📑 {stack.title}",
            callback_data=NavigationCallback(screen="cards_list", target_id=stack.id),
        )

    keyboard_builder.button(
        text="⬅️ Назад к доскам", callback_data=NavigationCallback(screen="boards_list")
    )

    keyboard_builder.adjust(KBD_COLUMNS)

    await callback.message.edit_text(
        "📚 <b>Стеки выбранной доски:</b>",
        reply_markup=keyboard_builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


async def back_to_boards_list(callback: types.CallbackQuery) -> None:
    """
    Возвращает к списку досок

    :param callback: Callback от нажатия кнопки "Назад"
    :type callback: types.CallbackQuery

    Пользователь нажимает "Назад" ->
    Бот снова показывает список досок
    """

    await show_boards_command(callback.message)
    await callback.answer()
