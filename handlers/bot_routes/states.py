"""Состояния и callback данные для бота списка покупок"""

from aiogram.filters.callback_data import CallbackData


class CardCallback(CallbackData, prefix="card"):
    """
    Callback для навигации по карточкам

    :param action: Действие (view, back, toggle, delete)
    :type action: str
    :param card_id: ID карточки
    :type card_id: int
    :param item_index: Индекс элемента
    :type item_index: int
    """

    action: str  # 'view', 'back', 'toggle', 'delete'
    card_id: int = 0
    item_index: int = -1
