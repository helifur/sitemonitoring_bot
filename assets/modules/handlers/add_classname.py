from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import json


async def add_classname_handler(message: Message, state: FSMContext) -> None:
    """
    This handler
    """
    with open("./assets/data/data.json") as f:
        all_data = json.load(f)

    try:
        data = all_data[message.chat.id]

    except KeyError:
        all_data[message.chat.id] = {}
        data = {}

    link = await state.get_data()
    link = link["link"]

    if link not in data.keys():
        all_data[message.chat.id][link] = [message.text]

        with open("./assets/data/data.json", "w") as f:
            json.dump(all_data, f)

        await state.clear()

        await message.answer(
            f"Сайт {link} успешно добавлен!\n\n"
            "Используйте /tracking для просмотра добавленных сайтов и элементов.",
            disable_web_page_preview=True,
        )

    else:
        all_data[message.chat.id][link].append(message.text)

        with open("./assets/data/data.json", "w") as f:
            json.dump(all_data, f)

        await state.clear()

        await message.answer(
            f"Имя класса {message.text} успешно добавлено к сайту {link}!\n\n"
            "Используйте /tracking для просмотра добавленных сайтов и элементов.",
            disable_web_page_preview=True,
        )
