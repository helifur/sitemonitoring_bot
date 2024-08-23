import asyncio
import aiofiles
import json

from assets.modules.parser.functions.get_changes import get_changes
from assets.config.config import bot, timer


async def parser(chat_id):
    while True:
        async with aiofiles.open("./assets/data/data.json") as file:
            sites = json.loads(await file.read())

        for url, classnames in sites.items():
            for classname in classnames:
                result = await get_changes(url, classname)

                # if not result:
                #    await bot.send_message(
                #        chat_id=chat_id,
                #        text=f"Сайт: {url}\nИмя класса: {classname}\nИзменения: нет.",
                #    )

                if result:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f"Сайт: {url}\nИмя класса: {classname}\n"
                        f"Изменения: 🔽🔽🔽\n=============\n{result}\n============\n",
                        disable_web_page_preview=True,
                    )

        await asyncio.sleep(timer)
