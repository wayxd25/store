# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.utils.executor import start_polling

from utils.config_loader import load_config
from utils.data_manager import load_premium_users

from handlers import (
    start, akun, grup, pesan,
    premium, forward, admin
)

config = load_config()
BOT_TOKEN = config["bot_token"]
OWNER_ID = config["owner_id"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Register semua handler
start.register(dp)
akun.register(dp)
grup.register(dp)
pesan.register(dp)
premium.register(dp)
forward.register(dp)
admin.register(dp)

async def on_startup(dp):
    await bot.send_message(OWNER_ID, "✅ BOT JASEB berhasil diaktifkan kembali setelah restart.")

if __name__ == "__main__":
    asyncio.run(on_startup(dp))
    start_polling(dp, skip_updates=True)