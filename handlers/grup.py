# handlers/grup.py
import os
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from telethon.sync import TelegramClient

from utils.config_loader import load_config
from utils.data_manager import load_temp_data, save_temp_data

config = load_config()
API_ID = config["api_id"]
API_HASH = config["api_hash"]

user_data = load_temp_data()

async def lihat_grup(message: types.Message):
    uid = str(message.from_user.id)
    session_path = os.path.join("sessions", f"{uid}")
    if not os.path.exists(session_path + ".session"):
        return await message.reply("Kamu belum login akun JASEB.")

    try:
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.start()
        dialogs = await client.get_dialogs()
        group_list = [d for d in dialogs if d.is_group]

        user_data.setdefault(uid, {})["grup_list"] = []
        for d in group_list:
            title = getattr(d, 'title', None) or getattr(d, 'name', 'Tanpa Nama')
            gid = getattr(d.entity, 'id', None)
            if title and gid:
                user_data[uid]["grup_list"].append((title, gid))

        kb = InlineKeyboardMarkup(row_width=1)
        for title, gid in user_data[uid]["grup_list"]:
            kb.add(InlineKeyboardButton(text=title, callback_data=f"pilihgrup:{gid}"))

        save_temp_data(user_data)
        await message.reply("Silakan pilih grup yang ingin kamu tambahkan ke target:", reply_markup=kb)
        await client.disconnect()
    except Exception as e:
        await message.reply(f"Gagal mengambil daftar grup: {e}")

async def pilih_grup_callback(callback_query: types.CallbackQuery):
    uid = str(callback_query.from_user.id)
    gid = int(callback_query.data.split(":")[1])
    grup_list = user_data.get(uid, {}).get("grup_list", [])
    target = next((g for g in grup_list if g[1] == gid), None)
    if not target:
        return await callback_query.answer("Grup tidak ditemukan.")

    user_data.setdefault(uid, {}).setdefault("grup_target", [])
    if target not in user_data[uid]["grup_target"]:
        user_data[uid]["grup_target"].append(target)
        save_temp_data(user_data)
        await callback_query.answer("Grup ditambahkan ke target.")
    else:
        await callback_query.answer("Grup sudah ada di target.")

async def daftar_grup_terpilih(message: types.Message):
    uid = str(message.from_user.id)
    grups = user_data.get(uid, {}).get("grup_target", [])
    if not grups:
        return await message.reply("Belum ada grup yang dipilih.")

    teks = "Berikut grup yang sudah kamu pilih sebagai target forward:\n\n"
    for i, (title, gid) in enumerate(grups, 1):
        teks += f"{i}. {title} (ID: {gid})\n"

    await message.reply(teks)

async def hapus_target(message: types.Message):
    uid = str(message.from_user.id)
    if "grup_target" in user_data.get(uid, {}) and user_data[uid]["grup_target"]:
        user_data[uid]["grup_target"] = []
        save_temp_data(user_data)
        await message.reply("Daftar grup target telah dihapus.")
    else:
        await message.reply("Belum ada grup yang dipilih.")

def register(dp: Dispatcher):
    dp.register_message_handler(lihat_grup, lambda m: m.text == "📄 Lihat Daftar Grup")
    dp.register_callback_query_handler(pilih_grup_callback, lambda c: c.data.startswith("pilihgrup:"))
    dp.register_message_handler(daftar_grup_terpilih, lambda m: m.text == "📋 Grup Terpilih")
    dp.register_message_handler(hapus_target, lambda m: m.text == "❌ Hapus Target Grup")