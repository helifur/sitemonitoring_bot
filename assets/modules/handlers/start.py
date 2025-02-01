from aiogram import html
from aiogram.types import Message


async def start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Здравствуйте, {html.bold(message.from_user.full_name)}!\n"
        "Для получения справки используйте /help.",
        parse_mode="HTML",
    )
