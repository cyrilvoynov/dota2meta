import logging
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import python_opendota
import asyncio

API_TOKEN = 'YOUR_API_TOKEN'

# Создание экземпляров
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Установим уровень логирования
logging.basicConfig(level=logging.INFO)

# Определим кнопки
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Carry"), KeyboardButton(text="Mid")],
        [KeyboardButton(text="Offlane"), KeyboardButton(text="Soft Support"), KeyboardButton(text="Hard Support")]
    ],
    resize_keyboard=True
)

# Функция для получения всех героев
async def get_all_heroes():
    url = "https://api.opendota.com/api/heroes"  # Измените на https
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Проверяем на ошибки HTTP
            heroes = response.json()  # Получаем JSON-ответ
            return heroes  # Возвращаем список всех героев
    except Exception as e:
        logging.error("Ошибка при получении героев: %s" % e)
        return []

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привет!", reply_markup=keyboard)

@dp.message()
async def send_top_heroes(message: types.Message):
    role = message.text
    heroes = await get_all_heroes()

    if heroes:
        # Пример: просто отправим первых 6 героев
        top_heroes = [hero['localized_name'] for hero in heroes[:6]]  # Здесь можно добавить логику для роли
        await message.answer("\n".join(top_heroes))
    else:
        await message.answer("Ошибка получения героев.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())