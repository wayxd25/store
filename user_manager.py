import json
import time
from aiogram import types

class UserManager:
    def __init__(self):
        self.data_file = "data/users.json"
        self.load_users()

    def load_users(self):
        try:
            with open(self.data_file, "r") as f:
                self.users = json.load(f)
        except:
            self.users = {}

    def save_users(self):
        with open(self.data_file, "w") as f:
            json.dump(self.users, f, indent=4)

    async def add_premium(self, message: types.Message):
        if message.from_user.id not in message.bot.get("admin_ids", []):
            return await message.reply("Kamu bukan admin!")
        try:
            args = message.get_args().split()
            username = args[0].lstrip("@")
            days = int(args[1])
            expired_at = int(time.time()) + days * 86400
            self.users[username] = {"expired": expired_at}
            self.save_users()
            await message.reply(f"✅ {username} berhasil jadi premium {days} hari!")
        except:
            await message.reply("Format salah!\nGunakan: /addprem @username 30")

    async def remove_premium(self, message: types.Message):
        if message.from_user.id not in message.bot.get("admin_ids", []):
            return await message.reply("Kamu bukan admin!")
        try:
            args = message.get_args().split()
            username = args[0].lstrip("@")
            if username in self.users:
                del self.users[username]
                self.save_users()
                await message.reply(f"✅ {username} sudah dihapus dari premium.")
            else:
                await message.reply("User tidak ditemukan.")
        except:
            await message.reply("Format salah!\nGunakan: /delprem @username")

    async def broadcast(self, message: types.Message):
        if message.from_user.id not in message.bot.get("admin_ids", []):
            return await message.reply("Kamu bukan admin!")
        text = message.get_args()
        if not text:
            return await message.reply("Isi pesan broadcast setelah perintah.")
        for username in self.users.keys():
            try:
                await message.bot.send_message(username, text)
            except:
                continue
        await message.reply("Broadcast selesai!")

    def is_premium(self, username):
        data = self.users.get(username)
        if not data:
            return False
        if data["expired"] < int(time.time()):
            return False
        return True
