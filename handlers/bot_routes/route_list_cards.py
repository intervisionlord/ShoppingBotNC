"""Логика отображения списка карточек"""

from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_shopping_cards
from handlers.bot_routes.route_states import CardCallback

list_router = Router()


@list_router.message(CommandStart())
@list_router.message(Command("help"))
async def start_help_handler(message: types.Message) -> None:
    """Обработчик команд /start и /help"""
    help_text = """
🛒 Бот для списка покупок

Команды:
/list - Показать список покупок
/help - Эта справка

💡 Просто введите элементы покупок сообщением, чтобы добавить их в список!
"""
    await message.answer(help_text)


@list_router.message(Command("list"))
async def list_handler(message: types.Message) -> None:
    """Показать список покупок в виде инлайн кнопок"""
    logger.info(f"Пользователь {message.from_user.id} запросил список покупок")

    # Всегда загружаем свежие данные
    cards = await get_shopping_cards()

    if cards is None:
        await message.answer("❌ Ошибка загрузки списка покупок")
        return

    if not cards:
        await message.answer("📝 Список покупок пуст")
        return

    keyboard_builder = InlineKeyboardBuilder()
    for card in cards:
        keyboard_builder.button(
            text=f"📋 {card.short_title}",
            callback_data=CardCallback(action="view", card_id=card.id),
        )

    keyboard_builder.adjust(1)
    await message.answer(
        f"🛒 Список покупок ({len(cards)}):",  # noqa: E231
        reply_markup=keyboard_builder.as_markup(),
    )


@list_router.callback_query(CardCallback.filter(F.action == "back"))
async def back_to_list_handler(
    callback: types.CallbackQuery, callback_data: CardCallback
) -> None:
    """Вернуться к списку карточек"""
    del callback_data
    await callback.answer()
    await list_handler(callback.message)
