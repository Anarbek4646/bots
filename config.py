from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()
TOKEN = config('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
admin = config('ADMIN')
# OPEN_AI_BOT_TOKEN = config('AITOKEN')

# openai.api_key = OPEN_AI_BOT_TOKEN
new_admins = config('ADMINS')

