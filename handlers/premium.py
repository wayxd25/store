# handlers/premium.py
from aiogram import types
from aiogram.dispatcher import Dispatcher
from datetime import datetime, timedelta

from utils.config_loader import load_config
from utils.data_manager import load_premium_users, save_premium_users

config = load_config()
OWNER_ID = config["owner_id"]
premium_users = load_premium_users()

async def add_premium(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Kamu tidak memiliki izin untuk menjalankan perintah ini.")

    args = message.text.strip().split()
    if len(args) != 2 or not args[1].isdigit():
        return await message.reply("Gunakan format: /addpremium <user_id>")

    user_id = str(args[1])
    premium_users[user_id] = (datetime.now() + timedelta(days=30)).isoformat()
    save_premium_users(premium_users)
    await message.reply(f"User {user_id} sekarang menjadi premium selama 30 hari.")

def register(dp: Dispatcher):
    dp.register_message_handler(add_premium, commands=["addpremium"])