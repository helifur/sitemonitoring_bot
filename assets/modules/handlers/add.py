from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from assets.modules.states.states import ManageSite


async def add_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with '/add' command
    """
    await message.answer("Введите ссылку на отслеживаемый сайт.")

    await state.set_state(ManageSite.adding_site)
