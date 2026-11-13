import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from db.database import init_db
from src.handlers import router as handlers_router

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage()) # обработчик входящих сообщений


async def main():
    init_db()
    dp.include_router(handlers_router)
    await dp.start_polling(bot) # отправляет запросы на тг-сервер

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())