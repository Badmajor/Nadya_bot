import datetime

from aiogram import Dispatcher, Bot

from data.config import BOT_TOKEN

dp = Dispatcher()
bot = Bot(BOT_TOKEN)


dt_utc = datetime.datetime.now(datetime.timezone.utc)
dt = dt_utc.replace(month=dt_utc.month, hour=dt_utc.hour+3)
