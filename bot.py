import json
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from user_manager import UserManager
from forwarder import ForwardManager

with open("config.json", "r") as f:
    config = json.load(f)

bot = Bot(token=config["BOT_TOKEN"])
dp = Dispatcher(bot)
user_manager = UserManager()
forward_manager = ForwardManager(user_manager)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Selamat datang di WayXD auto forward bot✨")

@dp.message_handler(commands=["addakun"])
async def addakun(message: types.Message):
    await forward_manager.add_account(message)

@dp.message_handler(commands=["target"])
async def target(message: types.Message):
    await forward_manager.set_targets(message)

@dp.message_handler(commands=["setpesan"])
async def setpesan(message: types.Message):
    await forward_manager.set_message(message)

@dp.message_handler(commands=["setdelay"])
async def setdelay(message: types.Message):
    await forward_manager.set_delay(message)

@dp.message_handler(commands=["startforward"])
async def startforward(message: types.Message):
    await forward_manager.start_forward(message)

@dp.message_handler(commands=["stop"])
async def stopforward(message: types.Message):
    await forward_manager.stop_forward(message)

@dp.message_handler(commands=["join"])
async def join(message: types.Message):
    await forward_manager.join_group(message)

@dp.message_handler(commands=["left"])
async def left(message: types.Message):
    await forward_manager.leave_group(message)

# Admin Commands
@dp.message_handler(commands=["addprem"])
async def addprem(message: types.Message):
    await user_manager.add_premium(message)

@dp.message_handler(commands=["delprem"])
async def delprem(message: types.Message):
    await user_manager.remove_premium(message)

@dp.message_handler(commands=["broadcast"])
async def broadcast(message: types.Message):
    await user_manager.broadcast(message)

async def check_expired_users():
    while True:
        for username, data in list(user_manager.users.items()):
            if data["expired"] < int(time.time()):
                del user_manager.users[username]
        user_manager.save_users()
        await asyncio.sleep(3600)  # cek setiap 1 jam

if __name__ == "__main__":
    dp.loop.create_task(check_expired_users())
    executor.start_polling(dp, skip_updates=True)
