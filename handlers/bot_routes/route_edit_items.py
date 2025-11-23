"""Логика редактирования элементов карточки"""

from aiogram import F, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.bot_routes.route_list_cards import list_handler
from handlers.bot_routes.route_view_card import (
    _show_card_view,
    get_cached_card,
)
from handlers.bot_routes.states import CardCallback
from handlers.handler_logging import logger
from handlers.handler_nc_deck import update_card_description

edit_router = Router()


@edit_router.callback_query(CardCallback.filter(F.action == "toggle"))
async def toggle_item_handler(
    callback: types.CallbackQuery, callback_data: CardCallback
) -> None:
    """
    Переключить статус элемента списка

    :param callback: Callback запрос
    :type callback: types.CallbackQuery
    :param callback_data: Данные callback
    :type callback_data: CardCallback
    """
    # Пытаемся получить карточку из кэша
    target_card = await get_cached_card(callback_data.card_id)

    if not target_card or not target_card.description:
        await callback.answer("❌ Карточка не найдена")
        return

    lines = target_card.description.split("\n")
    if 0 <= callback_data.item_index < len(lines):
        line = lines[callback_data.item_index]

        if "[ ]" in line:
            lines[callback_data.item_index] = line.replace("[ ]", "[x]")
        elif "[x]" in line:
            lines[callback_data.item_index] = line.replace("[x]", "[ ]")

        new_description = "\n".join(lines)
        success = await update_card_description(target_card.id, new_description)

        if success:
            logger.success(f"Статус карочки {target_card.id} обновлен")
            await callback.answer("✅ Статус обновлен")
            target_card.description = new_description
            await _show_card_view(callback.message, target_card)
        else:
            logger.error(f"Статус карточки {target_card.id} не был обновлен")
            await callback.answer("❌ Ошибка обновления")
    else:
        logger.error(f"Элемент карточки {target_card.id} не был найден")
        await callback.answer("❌ Элемент не найден")


@edit_router.callback_query(CardCallback.filter(F.action == "remove"))
async def remove_items_handler(
    callback: types.CallbackQuery, callback_data: CardCallback
) -> None:
    """
    Начать удаление элементов

    :param callback: Callback запрос
    :type callback: types.CallbackQuery
    :param callback_data: Данные callback
    :type callback_data: CardCallback
    """
    # Пытаемся получить карточку из кэша
    target_card = await get_cached_card(callback_data.card_id)

    if not target_card:
        await callback.answer("❌ Карточка не найдена")
        return

    items = target_card.get_list_items()
    if not items:
        await callback.answer("📝 Список пуст")
        await list_handler(callback.message)
        return

    keyboard_builder = InlineKeyboardBuilder()
    for index, item in enumerate(items):
        keyboard_builder.button(
            text=f"🗑️ {item}",
            callback_data=CardCallback(
                action="delete", card_id=target_card.id, item_index=index
            ),
        )

    keyboard_builder.button(
        text="⬅️ Назад",
        callback_data=CardCallback(action="view", card_id=target_card.id),
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
    """
    Удалить элемент из списка

    :param callback: Callback запрос
    :type callback: types.CallbackQuery
    :param callback_data: Данные callback
    :type callback_data: CardCallback
    """
    # Пытаемся получить карточку из кэша
    target_card = await get_cached_card(callback_data.card_id)

    if not target_card or not target_card.description:
        await callback.answer("❌ Карточка не найдена")
        return

    lines = target_card.description.split("\n")
    if 0 <= callback_data.item_index < len(lines):
        lines.pop(callback_data.item_index)

        new_description = "\n".join(lines) if lines else ""
        success = await update_card_description(target_card.id, new_description)

        if success:
            await callback.answer("✅ Элемент удален")

            # Обновляем кэш
            target_card.description = new_description
            items = target_card.get_list_items()

            if items:
                await remove_items_handler(callback, callback_data)
            else:
                await callback.answer("📝 Список пуст")
                callback_data.action = "view"
                await _show_card_view(callback.message, target_card)
        else:
            await callback.answer("❌ Ошибка удаления")
    else:
        await callback.answer("❌ Элемент не найден")
