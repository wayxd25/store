# handlers/forward.py
import os
import asyncio
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from telethon.sync import TelegramClient

from utils.config_loader import load_config
from utils.data_manager import load_temp_data, save_temp_data, load_premium_users

config = load_config()
API_ID = config["api_id"]
API_HASH = config["api_hash"]
premium_users = load_premium_users()
user_data = load_temp_data()
active_forwarding = {}

async def start_forwarding(uid, session_path, pesan, delay, targets, bot):
    client = TelegramClient(session_path, API_ID, API_HASH)
    await client.start()

    active_forwarding[uid] = True

    while active_forwarding.get(uid, False):
        for title, gid in targets:
            try:
                await client.send_message(gid, pesan + "\n\nʙᴏᴛ ᴊᴀsᴇʙ ʙʏ @waydevs")
            except Exception as e:
                await bot.send_message(uid, f"Gagal forward ke *{title}*: {str(e)}", parse_mode="Markdown")
        await asyncio.sleep(delay)

    await client.disconnect()

async def mulai_jaseb(message: types.Message):
    uid = str(message.from_user.id)
    if uid not in premium_users or datetime.fromisoformat(premium_users[uid]) < datetime.now():
        return await message.reply("Fitur ini hanya untuk pengguna premium.")

    session_path = os.path.join("sessions", f"{uid}.session")
    if not os.path.exists(session_path):
        return await message.reply("Kamu belum login akun.")

    data = user_data.get(uid, {})
    pesan = data.get("pesan")
    delay = data.get("delay", 30)
    targets = data.get("grup_target", [])

    if not pesan:
        return await message.reply("Silakan setting pesan terlebih dahulu.")
    if not targets:
        return await message.reply("Silakan pilih grup target terlebih dahulu.")

    await message.reply("Forward dimulai...")
    asyncio.create_task(start_forwarding(uid, session_path, pesan, delay, targets, message.bot))

async def stop_jaseb(message: types.Message):
    uid = str(message.from_user.id)
    active_forwarding[uid] = False
    await message.reply("Forward otomatis dihentikan.")

async def set_delay(message: types.Message):
    await message.reply("Kirim angka dalam detik sebagai delay antar siklus forward:")

async def simpan_delay(message: types.Message):
    uid = str(message.from_user.id)
    user_data.setdefault(uid, {})["delay"] = int(message.text)
    save_temp_data(user_data)
    await message.reply(f"Delay telah diatur ke {message.text} detik.")

def register(dp: Dispatcher):
    dp.register_message_handler(mulai_jaseb, lambda m: m.text == "▶️ Mulai Jaseb")
    dp.register_message_handler(stop_jaseb, lambda m: m.text == "⛔ Stop Jaseb")
    dp.register_message_handler(set_delay, lambda m: m.text == "⏱ Atur Delay Jaseb")
    dp.register_message_handler(simpan_delay, lambda m: m.text.isdigit() and int(m.text) > 0)