from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from assets.modules.states.states import ManageSite


async def remove_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with '/remove' command
    """
    await message.answer("Введите ссылку на отслеживаемый сайт.")

    await state.set_state(ManageSite.removing_site)
