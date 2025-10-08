import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот запущен!")

async def send_car_notification(car_data: dict):
    text = (
        f"Добавлена новая машина!\n\n"
        f"Owner: {car_data.get('user')}\n"
        f"Brand: {car_data.get('brand')}\n"
        f"Model: {car_data.get('model')}\n"
        f"Number: {car_data.get('number')}\n"
        f"Date: {car_data.get('date')}\n"
        f"KPP: {car_data.get('carabka_transfer')}\n"
        f"type: {car_data.get('type_car')}\n"
        f"Probeg: {car_data.get('probeg')}\n"
    )
    await bot.send_message(ADMIN_ID, text)


async def start_polling():
    logging.info("Bot is starting...")
    await dp.start_polling(bot)
