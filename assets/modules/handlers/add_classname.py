from assets.modules.parser.functions.get_page import manage_page
from assets.modules.states.states import ManageSite
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import json


async def add_classname_handler(message: Message, state: FSMContext) -> None:
    """
    This handler
    """
    with open("./assets/data/data.json") as f:
        data = json.load(f)

    link = await state.get_data()
    link = link["link"]

    if link not in data.keys():
        data[link] = [message.text]

        with open("./assets/data/data.json", "w") as f:
            json.dump(data, f)

        await state.clear()

        await message.answer(
            f"Сайт {link} успешно добавлен!\n\n"
            "Используйте /tracking для просмотра добавленных сайтов и элементов.",
            disable_web_page_preview=True,
        )

    else:
        data[link].append(message.text)

        with open("./assets/data/data.json", "w") as f:
            json.dump(data, f)

        await state.clear()

        await message.answer(
            f"Имя класса {message.text} успешно добавлено к сайту {link}!\n\n"
            "Используйте /tracking для просмотра добавленных сайтов и элементов.",
            disable_web_page_preview=True,
        )
