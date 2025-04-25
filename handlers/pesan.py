# handlers/pesan.py
from aiogram import types
from aiogram.dispatcher import Dispatcher

from utils.data_manager import load_temp_data, save_temp_data

user_data = load_temp_data()

async def setting_pesan(message: types.Message):
    await message.reply("Kirim pesan yang ingin diforward oleh bot.")

    @message.bot.message_handler(lambda m: True)
    async def simpan_pesan(msg: types.Message):
        uid = str(msg.from_user.id)
        user_data.setdefault(uid, {})["pesan"] = msg.text
        save_temp_data(user_data)
        await msg.reply("Pesan berhasil disimpan!")
        message.bot.message_handlers.unregister(simpan_pesan)

async def preview_pesan(message: types.Message):
    uid = str(message.from_user.id)
    data = user_data.get(uid, {})
    pesan = data.get("pesan")
    if not pesan:
        await message.reply("Belum ada pesan yang disimpan. Silakan setting pesan terlebih dahulu.")
    else:
        await message.reply(f"Berikut isi pesan yang akan diforward:\n\n{pesan}")

def register(dp: Dispatcher):
    dp.register_message_handler(setting_pesan, lambda m: m.text == "✏️ Setting Pesan")
    dp.register_message_handler(preview_pesan, lambda m: m.text == "👁 Preview Pesan")