from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import json


async def remove_classname_handler(message: Message, state: FSMContext) -> None:
    """
    This handler
    """
    with open("./assets/data/data.json") as f:
        data = json.load(f)
        data = data[str(message.chat.id)]

    link = await state.get_data()
    link = link["link"]

    if message.text not in data[link]:
        await message.answer("Вы не добавляли элемент с таким именем класса!")

    else:
        data[link].remove(message.text)

        if not data[link]:
            del data[link]

        with open("./assets/data/data.json", "w") as f:
            json.dump(data, f)

        await state.clear()

        await message.answer(
            f"Имя класса {message.text}, привязанное к сайту {link}, успешно удалено!\n\n"
            "Используйте /tracking для просмотра добавленных сайтов и элементов.",
            disable_web_page_preview=True,
        )
