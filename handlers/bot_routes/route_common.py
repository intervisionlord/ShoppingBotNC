"""Общие функции для роутов бота"""

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_shopping_cards
from handlers.bot_routes.route_states import CardCallback


async def get_card_by_id(card_id: int):
    """Получить карточку по ID (с загрузкой карточек)"""
    cards = await get_shopping_cards()
    if not cards:
        return None
    return next((c for c in cards if c.id == card_id), None)


def create_card_keyboard(card, items: list) -> InlineKeyboardBuilder:
    """Создает клавиатуру для карточки"""
    keyboard_builder = InlineKeyboardBuilder()

    # Элементы списка как инлайн кнопки
    for index, item in enumerate(items):
        description = card.description or ""
        lines = description.split("\n")
        emoji = "✅" if index < len(lines) and "[x]" in lines[index] else "⭕"

        keyboard_builder.button(
            text=f"{emoji} {item}",
            callback_data=CardCallback(
                action="toggle", card_id=card.id, item_index=index
            ),
        )

    keyboard_builder.button(
        text="🗑️ Удалить", callback_data=CardCallback(action="remove", card_id=card.id)
    )
    keyboard_builder.button(text="⬅️ Назад", callback_data=CardCallback(action="back"))

    keyboard_builder.adjust(1)
    return keyboard_builder


async def show_card_view(message: types.Message, card_id: int) -> None:
    """Показать представление карточки"""
    card = await get_card_by_id(card_id)
    if not card:
        await message.answer("❌ Карточка не найдена")
        return

    items = card.get_list_items()
    keyboard_builder = create_card_keyboard(card, items)

    card_text = f"<b>{card.title}</b>\n\n"
    if items:
        card_text += f"Элементов: {len(items)}\n\n"
    else:
        card_text += "Список пуст\n\n"

    card_text += "💡 <i>Просто введите новые элементы сообщением:</i>\n"
    card_text += "<i>• Один элемент</i>\n"
    card_text += "<i>• Или несколько через запятую</i>"

    await message.answer(
        card_text, reply_markup=keyboard_builder.as_markup(), parse_mode="HTML"
    )
