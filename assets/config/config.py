from aiogram import Bot, Dispatcher


TOKEN = ""
dp = Dispatcher()
# Initialize Bot instance with default bot properties which will be passed to all API calls
# default=DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=TOKEN)
task = None
