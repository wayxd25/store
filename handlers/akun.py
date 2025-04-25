# handlers/akun.py
import os
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import Dispatcher
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

from utils.config_loader import load_config
from utils.data_manager import load_temp_data, save_temp_data

config = load_config()
API_ID = config["api_id"]
API_HASH = config["api_hash"]

user_data = load_temp_data()
user_sessions = {}

async def tambah_akun(message: types.Message):
    await message.reply("Silakan kirim nomor HP akun JASEB kamu (format: +62...)")

async def handle_nomor(message: types.Message):
    uid = str(message.from_user.id)
    phone = message.text.strip()
    session_path = os.path.join("sessions", f"{uid}")
    os.makedirs("sessions", exist_ok=True)

    try:
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.connect()
        result = await client.send_code_request(phone)

        user_data[uid] = {
            "phone": phone,
            "code_hash": result.phone_code_hash
        }
        user_sessions[uid] = client
        save_temp_data(user_data)
        await message.reply("Kode OTP telah dikirim. Silakan masukkan kode yang kamu terima.")
    except Exception as e:
        await message.reply(f"Gagal mengirim kode OTP: {e}")

async def handle_otp(message: types.Message):
    uid = str(message.from_user.id)
    data = user_data.get(uid, {})
    phone = data.get("phone")
    code_hash = data.get("code_hash")
    client = user_sessions.get(uid)

    if not phone or not code_hash or not client:
        return await message.reply("Data login tidak lengkap atau sesi kadaluarsa.")

    try:
        await client.sign_in(phone=phone, code=message.text, phone_code_hash=code_hash)
        await client.disconnect()
        del user_sessions[uid]
        user_data.pop(uid, None)
        save_temp_data(user_data)
        await message.reply("Akun JASEB berhasil ditambahkan!")
    except SessionPasswordNeededError:
        user_data[uid]["pending_2fa"] = {
            "phone": phone,
            "code_hash": code_hash,
            "otp": message.text
        }
        save_temp_data(user_data)
        await message.reply("Akun ini menggunakan verifikasi dua langkah.\nSilakan kirim password akun Telegram kamu.")
    except Exception as e:
        await message.reply(f"Gagal login: {e}")

async def handle_password(message: types.Message):
    uid = str(message.from_user.id)
    data = user_data[uid].get("pending_2fa", {})
    password = message.text
    session_path = os.path.join("sessions", f"{uid}")

    try:
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.start()
        await client.check_password(password)
        await client.disconnect()
        user_data.pop(uid, None)
        save_temp_data(user_data)
        await message.reply("Login dengan verifikasi dua langkah berhasil!")
    except Exception as e:
        await message.reply(f"Gagal login dengan 2FA: {e}")

async def hapus_akun(message: types.Message):
    uid = str(message.from_user.id)
    session_path = os.path.join("sessions", f"{uid}.session")
    if os.path.exists(session_path):
        os.remove(session_path)
        await message.reply("Akun JASEB berhasil dihapus.")
    else:
        await message.reply("Tidak ada akun yang bisa dihapus.")

def register(dp: Dispatcher):
    dp.register_message_handler(tambah_akun, lambda m: m.text == "➕ Tambah Akun Jaseb")
    dp.register_message_handler(handle_nomor, lambda m: m.text.startswith("+62"))
    dp.register_message_handler(handle_otp, lambda m: m.text.isdigit() and len(m.text) in [5, 6])
    dp.register_message_handler(handle_password, lambda m: user_data.get(str(m.from_user.id), {}).get("pending_2fa"))
    dp.register_message_handler(hapus_akun, lambda m: m.text == "🗑 Hapus Akun Jaseb")