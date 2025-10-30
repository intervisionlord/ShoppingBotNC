"""Логика просмотра и управления карточкой"""

from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.handler_nc_deck import get_shopping_cards, update_card_description
from handlers.bot_routes.states import CardCallback
from handlers.bot_routes.route_list_cards import list_handler
from handlers.handler_logging import logger

view_router = Router()

MAX_ITEM_PREVIEW_LENGTH = 50
ELLIPSIS_LENGTH = 3

# Простой кэш карточек на время сессии
_card_cache = {}


@view_router.callback_query(CardCallback.filter(F.action == "view"))
async def view_card_handler(
    callback: types.CallbackQuery, callback_data: CardCallback
) -> None:
    """
    Показать детали карточки с элементами списка

    :param callback: Callback запрос
    :type callback: types.CallbackQuery
    :param callback_data: Данные callback
    :type callback_data: CardCallback
    """
    cards = await get_shopping_cards()
    if not cards:
        await callback.message.edit_text("❌ Карточка не найдена")
        return

    target_card = next(
        (card for card in cards if card.id == callback_data.card_id), None
    )
    if not target_card:
        await callback.message.edit_text("❌ Карточка не найдена")
        return

    # Кэшируем карточку
    _card_cache[callback_data.card_id] = target_card

    await _show_card_view(callback.message, target_card)
    await callback.answer()


async def _show_card_view(message: types.Message, card) -> None:
    """
    Показать представление карточки

    :param message: Сообщение для редактирования/отправки
    :type message: types.Message
    :param card: Карточка для отображения
    """
    items = card.get_list_items()
    keyboard_builder = InlineKeyboardBuilder()

    for index, item in enumerate(items):
        description = card.description or ""
        lines = description.split("\n")
        EMOJI_CHECKED = "✅"
        EMOJI_UNCHECKED = "🔳"

        emoji = (
            EMOJI_CHECKED
            if index < len(lines) and "[x]" in lines[index]
            else EMOJI_UNCHECKED
        )

        display_item = item
        if len(item) > MAX_ITEM_PREVIEW_LENGTH:
            display_item = item[: MAX_ITEM_PREVIEW_LENGTH - ELLIPSIS_LENGTH] + "..."

        keyboard_builder.button(
            text=f"{emoji} {display_item}",
            callback_data=CardCallback(
                action="toggle", card_id=card.id, item_index=index
            ),
        )

    if items:
        keyboard_builder.button(
            text="🗑️ Удалить",
            callback_data=CardCallback(action="remove", card_id=card.id),
        )

    keyboard_builder.button(text="⬅️ Назад", callback_data=CardCallback(action="back"))
    keyboard_builder.adjust(1)

    card_text = await _generate_card_text(card.title, items)

    if hasattr(message, "edit_text"):
        await message.edit_text(
            card_text, reply_markup=keyboard_builder.as_markup(), parse_mode="HTML"
        )
    else:
        await message.answer(
            card_text, reply_markup=keyboard_builder.as_markup(), parse_mode="HTML"
        )


async def _generate_card_text(title: str, items: list) -> str:
    """
    Сгенерировать текст для отображения карточки

    :param title: Заголовок карточки
    :type title: str
    :param items: Список элементов
    :type items: list
    :return: Сформированный текст
    :rtype: str
    """
    if items:
        items_text = f"Элементов: {len(items)}\n\n"
    else:
        items_text = "📝 Список пуст\n\n"

    return f"""<b>{title}</b>

{items_text}
💡 <i>Просто введите новые элементы сообщением:</i>
<i>• Один элемент</i>
<i>• Или несколько через запятую</i>"""


@view_router.message()
async def handle_message_input(message: types.Message) -> None:
    """
    Обработчик текстовых сообщений для автоматического добавления элементов

    :param message: Входящее сообщение
    :type message: types.Message
    """
    if message.text.startswith("/"):
        return

    logger.info(f"Получено сообщение для добавления: {message.text}")

    # Используем первую карточку из кэша или загружаем заново
    if _card_cache:
        # Берем первую карточку из кэша (самый частый случай - одна карточка)
        target_card = next(iter(_card_cache.values()))
        await _add_items_to_card(message, target_card)
    else:
        # Fallback - загружаем карточки если кэш пуст
        cards = await get_shopping_cards()
        if not cards:
            await message.answer("❌ Нет доступных карточек")
            return
        target_card = cards[0]
        await _add_items_to_card(message, target_card)


async def _parse_new_items(text: str) -> list:
    """
    Парсит новые элементы из текста

    :param text: Текст с элементами для парсинга
    :type text: str
    :return: Список очищенных элементов
    :rtype: list
    """
    ITEM_SEPARATOR = ","

    new_items_text = text.strip()
    if not new_items_text:
        return []

    if ITEM_SEPARATOR in new_items_text:
        return [
            item.strip()
            for item in new_items_text.split(ITEM_SEPARATOR)
            if item.strip()
        ]
    return [new_items_text]


async def _add_items_to_card(message: types.Message, card) -> None:
    """
    Добавить элементы в карточку

    :param message: Сообщение с элементами
    :type message: types.Message
    :param card: Карточка для обновления
    """
    new_items = await _parse_new_items(message.text)
    if not new_items:
        await message.answer("❌ Не указаны элементы для добавления")
        return

    logger.info(f"Парсинг элементов: {new_items}")

    current_items = card.get_list_items()
    updated_items = current_items + new_items
    new_description = card.update_list_items(updated_items)

    logger.info(f"Обновление карточки {card.id}: {len(updated_items)} элементов")

    success = await update_card_description(card.id, new_description)

    if success:
        await message.answer(f"✅ Добавлено {len(new_items)} элементов в '{card.title}'")
        # Обновляем кэш
        card.description = new_description
        _card_cache[card.id] = card
        await list_handler(message)
    else:
        await message.answer("❌ Ошибка при добавлении элементов")


async def get_cached_card(card_id: int):
    """
    Получить карточку из кэша

    :param card_id: ID карточки
    :type card_id: int
    :return: Карточка из кэша или None
    """
    return _card_cache.get(card_id)
