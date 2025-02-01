from aiogram.types import Message
import subprocess
import os


async def reboot_handler(message: Message) -> None:
    """
    This handler receives messages with `/tracking` command
    """
    await message.answer("Идет перезагрузка бота...")
    await message.answer(os.getcwd())
    subprocess.run(["./reboot.sh"])
