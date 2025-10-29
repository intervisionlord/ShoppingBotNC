"""Состояния и callback данные для бота списка покупок"""

from aiogram.filters.callback_data import CallbackData


class CardCallback(CallbackData, prefix="card"):
    """Callback для навигации по карточкам"""

    action: str  # 'view', 'back', 'toggle', 'delete'
    card_id: int = 0
    item_index: int = -1
