from tkinter import Button
from typing import List

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.settings import settings
from handlers.handler_card import get_card

from handlers.handler_logging import logger
from handlers.handler_stack import get_stack
from models.model_card import Card

router = Router()


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


@router.message(Command("list"))
async def get_cards_list(message: Message) -> None:
    stack = await get_stack()
    if stack is not None:
        await message.reply(stack.title, reply_markup=await make_keyboard(stack.cards))
    else:
        logger.critical(f"Ошибка получения стэка {settings.DECK_STACK_ID}")
        await message.reply("Ошибка получения стэка")


l @ router.callback_query(CardCallback.filter(F.id))


async def get_card_details(
    callback_query: CallbackQuery, callback_data: CardCallback
) -> None:
    card = await get_card(callback_data.id)
    if card is None:
        empty_keyboard = await make_keyboard()
        await callback_query.message.edit_reply_markup(
            text="Ошибка получения карточки", reply_markup=empty_keyboard
        )
    items = card.description.split("\n")
    for index, item in enumerate(items):
        if item.startswith("- [ ]"):
            items[index] = item.replace("- [ ]", "🔳")
        if item.startswith("- [x]"):
            items[index] = item.replace("- [x]", "✅")
    items_keyboard = await make_keyboard(items)
    await callback_query.message.edit_reply_markup(reply_markup=items_keyboard)
