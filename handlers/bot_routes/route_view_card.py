"""Логика просмотра и управления карточкой"""

from aiogram import Router, types, F

# from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_shopping_cards, update_card_description
from handlers.bot_routes.route_utils import parse_new_items
from handlers.bot_routes.route_states import CardCallback
from handlers.bot_routes.route_list_cards import list_handler
from handlers.bot_routes.route_common import create_card_keyboard

view_router = Router()


@view_router.callback_query(CardCallback.filter(F.action == "view"))
async def view_card_handler(
    callback: types.CallbackQuery, callback_data: CardCallback
) -> None:
    """Показать детали карточки с элементами списка"""
    cards = await get_shopping_cards()
    if not cards:
        await callback.message.edit_text("❌ Карточка не найдена")
        return

    card = next((c for c in cards if c.id == callback_data.card_id), None)
    if not card:
        await callback.message.edit_text("❌ Карточка не найдена")
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

    await callback.message.edit_text(
        card_text, reply_markup=keyboard_builder.as_markup(), parse_mode="HTML"
    )
    await callback.answer()


@view_router.message()
async def handle_message_input(message: types.Message) -> None:
    """Обработчик текстовых сообщений для автоматического добавления элементов"""
    # Проверяем, не является ли сообщение командой
    if message.text.startswith("/"):
        return

    # Получаем все карточки один раз
    cards = await get_shopping_cards()
    if not cards:
        await message.answer("❌ Нет доступных карточек")
        return

    # Если есть только одна карточка, добавляем в нее
    if len(cards) == 1:
        card = cards[0]
        await _add_items_to_card(message, card)
        return

    # Если карточек несколько, используем первую как fallback
    card = cards[0]
    await _add_items_to_card(message, card)


async def _add_items_to_card(message: types.Message, card) -> None:
    """Добавить элементы в карточку"""
    # Парсим новые элементы
    new_items = parse_new_items(message.text)
    if not new_items:
        await message.answer("❌ Не указаны элементы для добавления")
        return

    # Добавляем новые элементы
    current_items = card.get_list_items()
    updated_items = current_items + new_items

    # Обновляем описание карточки
    new_description = card.update_list_items(updated_items)
    success = await update_card_description(card.id, new_description)

    if success:
        await message.answer(f"✅ Добавлено {len(new_items)} элементов в '{card.title}'")
        # Просто вызываем list_handler который покажет актуальный список
        await list_handler(message)
    else:
        await message.answer("❌ Ошибка при добавлении элементов")
