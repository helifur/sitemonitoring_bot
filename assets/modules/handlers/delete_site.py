from assets.modules.states.states import ManageSite
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


import json


async def delete_site_handler(message: Message, state: FSMContext) -> None:
    with open("./assets/data/data.json") as f:
        data = json.load(f)

    if message.text not in data.keys():
        await message.answer("Вы еще не добавляли этот сайт или ссылка некорректна!")

    else:
        await message.answer("Введите имя удаляемого класса.")

        await state.set_state(ManageSite.removing_class_name)
        await state.update_data({"link": message.text})
