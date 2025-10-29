"""Логика редактирования элементов карточки"""

from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_shopping_cards, update_card_description
from handlers.bot_routes.route_states import CardCallback
from handlers.bot_routes.route_view_card import view_card_handler

edit_router = Router()


@edit_router.callback_query(CardCallback.filter(F.action == "toggle"))
async def toggle_item_handler(
    callback: types.CallbackQuery, callback_data: CardCallback
) -> None:
    """Переключить статус элемента списка"""
    cards = await get_shopping_cards()
    if not cards:
        await callback.answer("❌ Карточка не найдена")
        return

    card = next((c for c in cards if c.id == callback_data.card_id), None)
    if not card or not card.description:
        await callback.answer("❌ Карточка не найдена")
        return

    lines = card.description.split("\n")
    if 0 <= callback_data.item_index < len(lines):
        line = lines[callback_data.item_index]

        if "[ ]" in line:
            lines[callback_data.item_index] = line.replace("[ ]", "[x]")
        elif "[x]" in line:
            lines[callback_data.item_index] = line.replace("[x]", "[ ]")

        success = await update_card_description(card.id, "\n".join(lines))
        if success:
            await callback.answer("✅ Статус обновлен")
            await view_card_handler(callback, callback_data)
        else:
            await callback.answer("❌ Ошибка обновления")
    else:
        await callback.answer("❌ Элемент не найден")


@edit_router.callback_query(CardCallback.filter(F.action == "remove"))
async def remove_items_handler(
    callback: types.CallbackQuery, callback_data: CardCallback
) -> None:
    """Начать удаление элементов"""
    cards = await get_shopping_cards()
    if not cards:
        await callback.answer("❌ Карточка не найдена")
        return

    card = next((c for c in cards if c.id == callback_data.card_id), None)
    if not card:
        await callback.answer("❌ Карточка не найдена")
        return

    items = card.get_list_items()
    if not items:
        await callback.answer("❌ Список пуст")
        return

    keyboard_builder = InlineKeyboardBuilder()
    for index, item in enumerate(items):
        keyboard_builder.button(
            text=f"🗑️ {item}",
            callback_data=CardCallback(
                action="delete", card_id=card.id, item_index=index
            ),
        )

    keyboard_builder.button(
        text="⬅️ Назад", callback_data=CardCallback(action="view", card_id=card.id)
    )
    keyboard_builder.adjust(1)

    await callback.message.edit_text(
        "🗑️ <b>Выберите элементы для удаления:</b>",
        reply_markup=keyboard_builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@edit_router.callback_query(CardCallback.filter(F.action == "delete"))
async def delete_item_handler(
    callback: types.CallbackQuery, callback_data: CardCallback
) -> None:
    """Удалить элемент из списка"""
    cards = await get_shopping_cards()
    if not cards:
        await callback.answer("❌ Карточка не найдена")
        return

    card = next((c for c in cards if c.id == callback_data.card_id), None)
    if not card or not card.description:
        await callback.answer("❌ Карточка не найдена")
        return

    lines = card.description.split("\n")
    if 0 <= callback_data.item_index < len(lines):
        lines.pop(callback_data.item_index)
        success = await update_card_description(card.id, "\n".join(lines))

        if success:
            await callback.answer("✅ Элемент удален")
            # Перезагружаем карточки для актуальных данных
            updated_cards = await get_shopping_cards()
            updated_card = next((c for c in updated_cards if c.id == card.id), None)
            if updated_card:
                await remove_items_handler(callback, callback_data)
            else:
                await callback.answer("❌ Ошибка обновления данных")
        else:
            await callback.answer("❌ Ошибка удаления")
    else:
        await callback.answer("❌ Элемент не найден")
