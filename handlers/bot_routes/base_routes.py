from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from handlers.handler_logging import logger

# Создаем роутер для базовых команд бота
base_router = Router()


@base_router.message(CommandStart())
async def start_handler(message: types.Message):
    """Обработчик команды /start"""
    await message.answer("🚀 Бот запущен! Используйте /help для списка команд")
    logger.info(f"Пользователь {message.from_user.id} запустил бота")


@base_router.message(Command("help"))
async def help_handler(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
📋 Доступные команды:

/start - Запуск бота
/help - Помощь
/test - Тестовая команда
/about - О боте

Просто напишите "test" для проверки текстового хендлера
    """
    await message.answer(help_text)


@base_router.message(Command("test"))
async def test_command_handler(message: types.Message):
    """Обработчик команды /test"""
    await message.answer("✅ Тест пройден! Бот работает корректно!")
    logger.info(f"Пользователь {message.from_user.id} выполнил тест-команду")


@base_router.message(Command("about"))
async def about_handler(message: types.Message):
    """Обработчик команды /about"""
    await message.answer(
        "🤖 Это тестовый бот с модульной архитектурой\n\n"
        "⚡ Быстрое масштабирование\n"
        "📁 Чистая структура проекта\n"
        "🔧 Легкое обслуживание"
    )


@base_router.message(lambda message: message.text and message.text.lower() == "test")
async def test_text_handler(message: types.Message):
    """Обработчик текстового сообщения 'test'"""
    await message.answer("🔤 Вы написали 'test'! Текстовые хендлеры работают!")
    logger.info(f"Пользователь {message.from_user.id} отправил текстовый тест")
