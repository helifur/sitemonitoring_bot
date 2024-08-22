import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter

from assets.config.config import TOKEN
from assets.modules.states.states import ManageSite

from assets.modules.handlers.help import help_handler
from assets.modules.handlers.start import start_handler
from assets.modules.handlers.tracking import tracking_handler
from assets.modules.handlers.add import add_handler
from assets.modules.handlers.remove import remove_handler

from assets.modules.handlers.new_site import new_site_handler
from assets.modules.handlers.add_classname import add_classname_handler
from assets.modules.handlers.delete_site import delete_site_handler
from assets.modules.handlers.remove_classname import remove_classname_handler

from assets.modules.parser.functions.get_page import manage_page


dp = Dispatcher()


@dp.message(Command("test"))
async def test(message: Message):
    await message.answer(
        manage_page("https://www.linux.org.ru/forum/general/10040134", "msg_body")
    )


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    # default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=TOKEN)

    dp.message.register(start_handler, CommandStart(), StateFilter(None))
    dp.message.register(help_handler, Command("help"), StateFilter(None))
    dp.message.register(add_handler, Command("add"), StateFilter(None))
    dp.message.register(tracking_handler, Command("tracking"), StateFilter(None))
    dp.message.register(remove_handler, Command("remove"), StateFilter(None))

    dp.message.register(new_site_handler, ManageSite.adding_site)
    dp.message.register(add_classname_handler, ManageSite.adding_class_name)
    dp.message.register(delete_site_handler, ManageSite.removing_site)
    dp.message.register(remove_classname_handler, ManageSite.removing_class_name)

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    elems = {}

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
