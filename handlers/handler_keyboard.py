from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

l
from models.model_card import Card


class CardCallback(CallbackData, prefix="card"):
    id: int
    title: str


async def make_keyboard(cards: list | List[Card] | None) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    if cards is None:
        keyboard_builder.button(
            text="Назад", callback_data=CardCallback(id=-1, title="back_callback")
        )
    else:
        for index, item in enumerate(cards):
            if isinstance(item, Card):
                keyboard_builder.button(
                    text=item.title,
                    callback_data=CardCallback(id=item.id, title=item.title).pack(),
                )
            if isinstance(item, str):
                keyboard_builder.button(
                    text=item, callback_data=CardCallback(id=index, title=item).pack()
                )
                keyboard_builder.button(
                    text="Назад",
                    callback_data=CardCallback(id=-1, title="back_callback"),
                )
    return keyboard_builder.as_markup()
