# handlers/start.py
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import Dispatcher

from utils.data_manager import load_premium_users
from utils.config_loader import load_config

config = load_config()
premium_users = load_premium_users()

def main_menu(is_premium):
    buttons = [
        [KeyboardButton("➕ Tambah Akun Jaseb"), KeyboardButton("📄 Lihat Daftar Grup")],
        [KeyboardButton("✏️ Setting Pesan"), KeyboardButton("🎯 Pilih Target Grup")],
        [KeyboardButton("🆔 Lihat Akun Jaseb")],
        [KeyboardButton("👁 Preview Pesan"), KeyboardButton("▶️ Mulai Jaseb")],
        [KeyboardButton("🗑 Hapus Akun Jaseb")],
        [KeyboardButton("📋 Grup Terpilih"), KeyboardButton("❌ Hapus Target Grup")],
        [KeyboardButton("⏳ Cek Sisa Durasi Premium"), KeyboardButton("👤 Owner Bot Jaseb")],
        [KeyboardButton("⏱ Atur Delay Jaseb"), KeyboardButton("⛔ Stop Jaseb")]
    ]
    if not is_premium:
        buttons.append([KeyboardButton("🛒 Beli Akses Bot Jaseb")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

async def cmd_start(message: types.Message):
    uid = str(message.from_user.id)
    nama = message.from_user.first_name

    exp_str = premium_users.get(uid)
    is_premium = exp_str and (datetime.fromisoformat(exp_str) > datetime.now())

    teks = (
        f"Halo {nama}, selamat datang di BOT JASEB BY @waydevs✨\n\n"
        "Untuk menggunakan bot ini kamu harus memiliki akses premium terlebih dahulu😉🙏\n\n"
        "Untuk mendapatkan akses premium silahkan gunakan tombol "
        "(🛒 Beli Akses Bot JASEB) atau bisa langsung chat owner: @waydevs."
    )

    foto_url = "https://telegra.ph//file/283e59f1315575dab812d.jpg"
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=foto_url,
        caption=teks,
        reply_markup=main_menu(is_premium)
    )

async def owner_info(message: types.Message):
    await message.reply("Owner bot ini: @waydevs")

async def beli_akses(message: types.Message):
    uid = str(message.from_user.id)
    if uid in premium_users:
        await message.reply("Kamu sudah menjadi user premium.")
        return

    text = f"""
Untuk membeli akses premium Bot JASEB:

1. Kirim DANA ke: {config["nomor_dana"]}
2. Atau Scan QRIS: {config["qris"]}
3. Kirim bukti pembayaran ke @waydevs
Setelah diverifikasi, akunmu akan diupgrade ke Premium.
"""
    await message.reply(text)

async def cek_premium(message: types.Message):
    uid = str(message.from_user.id)
    exp_str = premium_users.get(uid)
    if not exp_str:
        return await message.reply("Kamu belum memiliki akses premium.")

    exp = datetime.fromisoformat(exp_str)
    sisa = exp - datetime.now()
    await message.reply(f"Sisa durasi premium kamu: {sisa}")

def register(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(owner_info, lambda m: m.text == "👤 Owner Bot Jaseb")
    dp.register_message_handler(beli_akses, lambda m: m.text == "🛒 Beli Akses Bot Jaseb")
    dp.register_message_handler(cek_premium, lambda m: m.text == "⏳ Cek Sisa Durasi Premium")