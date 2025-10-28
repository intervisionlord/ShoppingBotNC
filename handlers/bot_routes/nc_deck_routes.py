"""Обработчик отображения доступных досок"""

from aiogram import Router, types
from aiogram.filters import Command

from handlers.handler_logging import logger
from handlers.handler_nc_deck import get_boards, get_stacks

nc_deck_router = Router()


@nc_deck_router.message(Command("decks"))
async def command_get_decks(message: types.Message) -> None:
    """
    Отправляет в ответ список доступных досок

    :param message: Ответное сообщение
    :type message: types.Message
    """
    logger.info(
        f"Запрошен список досок пользователем {message.from_user.id} "
        f"({message.from_user.username})"
    )
    decks = await get_boards()
    if decks is not None:
        await message.answer(
            "<b>🗃️ Доступные доски:</b>\n\n"
            f"{'\n'.join([f'    🗂️ {deck.title}' for deck in decks])}",
            parse_mode="HTML",
        )
    else:
        await message.answer("❌ Доски отсутствуют или не получены")


@nc_deck_router.message(Command("stacks"))
async def command_get_stacks(message: types.Message) -> None:
    """
    Отправляет в ответ список стеков для указанной доски

    :param message: Ответное сообщение
    :type message: types.Message
    """
    # Получаем текст команды и аргументы
    command_args = message.text.split()

    if len(command_args) < 2:
        await message.answer(
            "❌ Не указан ID доски\n\n"
            "📝 Использование: <code>/stacks &lt;board_id&gt;</code>\n\n"
            "🔍 Чтобы получить список досок с их ID, используйте <code>/decks</code>",
            parse_mode="HTML",
        )
        return

    try:
        board_id = int(command_args[1])
    except ValueError:
        await message.answer(
            "❌ Неверный формат ID доски\n\n"
            "📝 ID доски должен быть числом\n"
            "🔍 Используйте <code>/decks</code> для просмотра доступных досок",
            parse_mode="HTML",
        )
        return

    logger.info(
        f"Запрошены стеки доски {board_id} пользователем {message.from_user.id} "
        f"({message.from_user.username})"
    )

    stacks = await get_stacks(board_id)
    if stacks is not None and stacks:
        stacks_list = "\n".join([f"    📑 {stack.title}" for stack in stacks])
        await message.answer(
            f"<b>📚 Стеки доски {board_id}:</b>\n\n{stacks_list}",  # noqa: E231
            parse_mode="HTML",
        )
    else:
        await message.answer(f"❌ Стеки для доски {board_id} отсутствуют или не найдены")
