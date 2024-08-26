from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

import json

from assets.modules.parser.functions.fill_urls import fill_urls
import assets.config.config


async def tracking_handler(message: Message) -> None:
    """
    This handler receives messages with `/tracking` command
    """

    with open("./assets/data/data.json") as f:
        data = json.load(f)

    try:
        data = data[str(message.chat.id)]

    except KeyError:
        data = None

    await fill_urls(message.chat.id)

    if data:
        output = [f"{i} == {', '.join(data[i])}" for i in data.keys()]
    else:
        output = ["Пусто!"]

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Запустить", callback_data="launch"))
    builder.add(InlineKeyboardButton(text="Остановить", callback_data="stop"))

    await message.answer(
        f"Список добавленных сайтов:\n\n{'\n\n'.join(output)}".strip()
        + "\n\nСтатус мониторинга: "
        + f"{'<b>Остановлен</b>' if not assets.config.config.task else '<b>Запущен</b>'}",
        disable_web_page_preview=True,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
