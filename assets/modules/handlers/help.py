from aiogram.types import Message


async def help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    await message.answer(
        "Все доступные команды:\n"
        "/start - начать работу бота\n"
        "/help - помощь\n"
        "/add - добавить сайт/отслеживаемый элемент\n"
        "/remove - удалить сайт/отслеживаемый элемент\n"
        "/tracking - управление мониторингом и сайтами"
    )
