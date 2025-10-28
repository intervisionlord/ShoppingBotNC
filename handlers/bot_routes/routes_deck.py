"""Главный роутер для всех команд бота (базовые + deck)"""

from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart

from handlers.bot_routes.route_deck_boards import (
    NavigationCallback,
    show_boards_command,
)
from handlers.bot_routes.route_deck_cards import show_cards_in_stack
from handlers.bot_routes.route_deck_stacks import (
    back_to_boards_list,
    show_stacks_for_board,
)
from handlers.handler_logging import logger

nc_deck_router = Router()


# ========== БАЗОВЫЕ КОМАНДЫ ==========
@nc_deck_router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    """
    Обработчик команды /start

    :param message: Сообщение пользователя
    :type message: types.Message
    """
    await message.answer("🚀 Бот запущен! Используйте /help для списка команд")
    logger.info(f"Пользователь {message.from_user.id} запустил бота")


@nc_deck_router.message(Command("help"))
async def help_handler(message: types.Message) -> None:
    """
    Обработчик команды /help

    :param message: Сообщение от пользователя
    :type message: types.Message
    """
    help_text = """
📋 Доступные команды:

/start - Запуск бота
/help - Помощь
/test - Тестовая команда
/about - О боте
/decks - Показать доски

Просто напишите "test" для проверки текстового хендлера
    """
    await message.answer(help_text)


@nc_deck_router.message(Command("test"))
async def test_command_handler(message: types.Message) -> None:
    """
    Обработчик команды /test

    :param message: Сообщение от пользователя
    :type message: types.Message

    """
    await message.answer("✅ Тест пройден! Бот работает корректно!")
    logger.info(f"Пользователь {message.from_user.id} выполнил тест-команду")


@nc_deck_router.message(Command("about"))
async def about_handler(message: types.Message) -> None:
    """
    Обработчик команды /about

    :param message: Сообщение от пользователя
    :type message: types.Message

    """
    await message.answer(
        "🤖 Это тестовый бот с модульной архитектурой\n\n"
        "⚡ Быстрое масштабирование\n"
        "📁 Чистая структура проекта\n"
        "🔧 Легкое обслуживание"
    )


@nc_deck_router.message(lambda message: message.text and message.text.lower() == "test")
async def test_text_handler(message: types.Message) -> None:
    """
    Обработчик текстового сообщения 'test'

    :param message: Сообщение от пользователя
    :type message: types.Message
    """
    await message.answer("🔤 Вы написали 'test'! Текстовые хендлеры работают!")
    logger.info(f"Пользователь {message.from_user.id} отправил текстовый тест")


# ========== DECK КОМАНДЫ ==========
@nc_deck_router.message(Command("decks"))
async def decks_handler(message: types.Message) -> None:
    """
    Обработчик команды /decks

    :param message: Сообщение от пользователя
    :type message: types.Message
    """
    await show_boards_command(message)


@nc_deck_router.callback_query(NavigationCallback.filter(F.screen == "stacks_list"))
async def stacks_handler(
    callback: types.CallbackQuery, callback_data: NavigationCallback
):
    """
    Обработчик выбора доски

    :param callback: Callback от нажатой кнопки меню
    :type callback: types.CallbackQuery
    :param callback_data: Callback данные
    :type callback_data: NavigationCallback
    """
    await show_stacks_for_board(callback, callback_data)


@nc_deck_router.callback_query(NavigationCallback.filter(F.screen == "boards_list"))
async def boards_handler(
    callback: types.CallbackQuery, callback_data: NavigationCallback
):
    """
    Обработчик возврата к доскам

    :param callback: Callback от нажатой кнопки
    :type callback: types.CallbackQuery
    :param callback_data: Callback данные
    :type callback_data: NavigationCallback
    """
    await back_to_boards_list(callback)


@nc_deck_router.callback_query(NavigationCallback.filter(F.screen == "cards_list"))
async def cards_handler(
    callback: types.CallbackQuery, callback_data: NavigationCallback
):
    """
    Обработчик выбора стека

    :param callback: Callback от нажатой кнопки
    :type callback: types.CallbackQuery
    :param callback_data: Callback данные
    :type callback_data: NavigationCallback
    """
    await show_cards_in_stack(callback, callback_data)
