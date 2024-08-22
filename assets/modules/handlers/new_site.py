from assets.modules.states.states import ManageSite
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import re


async def new_site_handler(message: Message, state: FSMContext) -> None:
    pattern = r"^(https?):\/\/[^\s\/$.?#].[^\s]*$"

    if re.match(pattern, message.text) is not None:
        await message.answer("Введите имя класса отслеживаемого элемента страницы.")

        await state.set_state(ManageSite.adding_class_name)
        await state.update_data({"link": message.text})

    else:
        await message.answer("Некорректная ссылка!")
