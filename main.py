# import time

# def task(name, second):
#     print(f"Упала задача {name} начал работу")
#     time.sleep(second)
#     print(f"Задача {name} готово!")

# task("Задача1", 4)
# task("Задача2", 2)
# task("Задача3", 3)

# import asyncio

# async def task(name, seconds):
#     print(f"Упала задача {name} начал работу")
#     await asyncio.sleep(seconds)
#     print(f"Задача {name} готово!")


# async def main():
#     await asyncio.gather(
#         task("Задача1", 5),
#         task("Задача2", 2),
#         task("Задача3", 3)
#     )

# asyncio.run(main())

import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

BOT_TOKEN = "8699853215:AAGvrStTbE0qbOLThQYgCJzSnAX1jqbyU_o"

bot = Bot(BOT_TOKEN)
dp = Dispatcher() # обработчик входящих сообщений

@dp.message(CommandStart())
async def CommandStart(message: Message):
    await message.answer(
        f"Привет {message.from_user.full_name} (@{message.from_user.username}), я Бот!"
    )
    print(f"Пользователь {message.from_user.username} написал команду start")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        f"/start - команда для запуска\n"
        f"/help - список команд"
    )


@dp.message(F.text.lower() == "группа")
async def cmd_group_f(message: Message):
    await message.answer(
        f"Твоя группа: 71-1"
    )

@dp.message()
async def cmd_echo(message:Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    await dp.start_polling(bot) # отправляет запросы на тг-сервер

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

