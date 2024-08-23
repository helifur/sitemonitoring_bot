from aiogram import Bot, Dispatcher


TOKEN = "6064533705:AAFy_PObiHjdS1hpWy93BYAM8UtmdO8uCzg"
dp = Dispatcher()
# Initialize Bot instance with default bot properties which will be passed to all API calls
# default=DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=TOKEN)
task = None
timer = 10
