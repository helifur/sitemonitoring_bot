import asyncio
import logging
import sys

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


from assets.config.config import dp, bot
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

from assets.modules.parser.parser import parser

import assets.config.config


@dp.callback_query(F.data == "launch")
async def launch_monitoring(callback: CallbackQuery):
    await callback.answer("Мониторинг запущен!", show_alert=True)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Запустить", callback_data="launch"))
    builder.add(InlineKeyboardButton(text="Остановить", callback_data="stop"))

    await callback.message.edit_text(
        callback.message.text[:-10] + "<b>Запущен</b>",
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=builder.as_markup(),
    )
    assets.config.config.task[callback.message.chat.id] = asyncio.create_task(
        parser(str(callback.message.chat.id))
    )
    print("Tasks:", end=" ")
    print(assets.config.config.task)


@dp.callback_query(F.data == "stop")
async def stop_monitoring(callback: CallbackQuery):
    assets.config.config.task[callback.message.chat.id].cancel()

    try:
        await assets.config.config.task[callback.message.chat.id]

    except asyncio.CancelledError:
        assets.config.config.driver.quit()
        assets.config.config.task.pop(callback.message.chat.id, None)
        print("Tasks:", end=" ")
        print(assets.config.config.task)

        await callback.answer("Мониторинг остановлен!", show_alert=True)

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Запустить", callback_data="launch"))
        builder.add(InlineKeyboardButton(text="Остановить", callback_data="stop"))

        await callback.message.edit_text(
            callback.message.text[:-7] + "<b>Остановлен</b>",
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=builder.as_markup(),
        )


async def main() -> None:
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
