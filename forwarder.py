import json
import asyncio
from telethon import TelegramClient

class ForwardManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.data_file = "data/forward.json"
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        except:
            self.data = {}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    async def add_account(self, message):
        await message.reply("Kirimkan file session (.session) ke sini.")
        # Ini harus manual upload file lalu dipindahkan ke `sessions/`
        # Alternatif bisa dibuat inline upload nanti.

    async def set_targets(self, message):
        username = message.from_user.username
        if not self.user_manager.is_premium(username):
            return await message.reply("Kamu bukan user premium!")
        targets = message.get_args().split()
        if len(targets) > 10:
            return await message.reply("Maksimal 10 grup!")
        self.data.setdefault(username, {})["targets"] = targets
        self.save_data()
        await message.reply("✅ Target grup disimpan!")

    async def set_message(self, message):
        username = message.from_user.username
        if not self.user_manager.is_premium(username):
            return await message.reply("Kamu bukan user premium!")
        self.data.setdefault(username, {})["message"] = message.get_args()
        self.save_data()
        await message.reply("✅ Pesan forward disimpan!")

    async def set_delay(self, message):
        username = message.from_user.username
        if not self.user_manager.is_premium(username):
            return await message.reply("Kamu bukan user premium!")
        try:
            delay = int(message.get_args())
            self.data.setdefault(username, {})["delay"] = delay
            self.save_data()
            await message.reply(f"✅ Delay disimpan: {delay} detik")
        except:
            await message.reply("Gunakan angka! contoh: /setdelay 5")

    async def start_forward(self, message):
        username = message.from_user.username
        if not self.user_manager.is_premium(username):
            return await message.reply("Kamu bukan user premium!")
        await message.reply("Memulai forward...")

        session_path = f"sessions/{username}.session"
        client = TelegramClient(session_path, api_id=message.bot.get("api_id"), api_hash=message.bot.get("api_hash"))
        await client.start()

        text = self.data[username].get("message", "")
        targets = self.data[username].get("targets", [])
        delay = self.data[username].get("delay", 5)

        if not text or not targets:
            return await message.reply("Pastikan sudah set pesan dan target!")

        for target in targets:
            try:
                await client.send_message(target, text + "\n\n// ᴊᴀsᴇʙ ʙʏ @waydevs //")
                await asyncio.sleep(delay)
            except Exception as e:
                await message.reply(f"Error kirim ke {target}: {str(e)}")

        await client.disconnect()
        await message.reply("✅ Selesai forward semua grup!")

    async def stop_forward(self, message):
        await message.reply("Untuk saat ini tidak ada proses live, semua forward instan.")

    async def join_group(self, message):
        username = message.from_user.username
        session_path = f"sessions/{username}.session"
        client = TelegramClient(session_path, api_id=message.bot.get("api_id"), api_hash=message.bot.get("api_hash"))
        await client.start()

        link = message.get_args()
        try:
            await client(JoinChannelRequest(link))
            await message.reply(f"✅ Bergabung ke {link}")
        except Exception as e:
            await message.reply(f"Gagal join: {str(e)}")
        await client.disconnect()

    async def leave_group(self, message):
        username = message.from_user.username
        session_path = f"sessions/{username}.session"
        client = TelegramClient(session_path, api_id=message.bot.get("api_id"), api_hash=message.bot.get("api_hash"))
        await client.start()

        link = message.get_args()
        try:
            await client(LeaveChannelRequest(link))
            await message.reply(f"✅ Keluar dari {link}")
        except Exception as e:
            await message.reply(f"Gagal left: {str(e)}")
        await client.disconnect()
