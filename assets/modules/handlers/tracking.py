from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

import json

from assets.modules.parser.functions.fill_urls import fill_urls


async def tracking_handler(message: Message) -> None:
    """
    This handler receives messages with `/tracking` command
    """

    with open("./assets/data/data.json") as f:
        data = json.load(f)

    await fill_urls()

    output = [f"{i} == {", ".join(data[i])}" for i in data.keys()]

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Запустить", callback_data="launch"))
    builder.add(InlineKeyboardButton(text="Остановить", callback_data="stop"))

    await message.answer(
        f"Список добавленных сайтов:\n\n{'\n\n'.join(output)}".strip(),
        disable_web_page_preview=True,
        reply_markup=builder.as_markup(),
    )
