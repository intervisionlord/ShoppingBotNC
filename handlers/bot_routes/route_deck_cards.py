"""Обработчик для работы с карточками"""

from aiogram import types

from handlers.bot_routes.route_deck_boards import NavigationCallback
from handlers.handler_logging import logger


async def show_cards_in_stack(
    callback: types.CallbackQuery, callback_data: NavigationCallback
) -> None:
    """
    Показывает карточки в стеке (заглушка)

    :param callback: Callback от нажатой кнопки в предыдущем меню
    :type callback: types.CallbackQuery
    :param callback_data: Данные callback'а
    :type callback_data: NavigationCallback

    Пользователь нажимает на кнопку стека ->
    Бот показывает карточки (пока заглушка)
    """
    stack_id = callback_data.target_id
    logger.info(f"Пользователь {callback.from_user.id} выбрал стек {stack_id}")

    # TODO: Здесь будет логика получения и отображения карточек
    await callback.message.edit_text(
        f"📋 <b>Карточки стека {stack_id}</b>\n\n"
        f"Функционал отображения карточек в разработке...",
        parse_mode="HTML",
    )
    await callback.answer()
