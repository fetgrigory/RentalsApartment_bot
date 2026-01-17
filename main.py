'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 28/05/2024
Ending //

'''
# Installing the necessary libraries
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Router, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from src.handlers.user_handlers import router as user_router
from src.handlers.admin_panel.add_apartment_handlers import router as add_router
from src.handlers.admin_panel.edit_apartment_handlers import router as edit_router
from src.handlers.admin_panel.catalog_handlers import router as catalog_router
from src.handlers.admin_panel.reviews_handlers import router as reviews_router
from src.handlers.admin_panel.bookings_handlers import router as bookings_router
from src.db.database import init_db
from src.keyboards.user_keyboard import start_keyboard

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)
# Initialize bot and dispatcher in combination with state storage
load_dotenv()
router = Router()


TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
if not TOKEN:
    logger.error("TOKEN не задан в переменных окружения!")
# Dictionary to store user data temporarily
USER_DATA = {}

# Setting up the bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

# Connecting routers
dp.include_router(router)
dp.include_router(user_router)
dp.include_router(add_router)
dp.include_router(edit_router)
dp.include_router(catalog_router)
dp.include_router(reviews_router)
dp.include_router(bookings_router)


@router.message(Command("start"))
async def start(message: types.Message):
    logger.info("User pressed /start")
    USER_DATA.clear()
    keyboard = start_keyboard(message.from_user.id)
    me = await message.bot.get_me()
    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}!\n"
        f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
        parse_mode='html',
        reply_markup=keyboard
    )

# Creating a database at startup
try:
    init_db()
    logger.info("Database successfully created/connected")
except Exception as e:
    logger.exception("Error creating database: %s", e)

if __name__ == "__main__":
    logger.info("Start polling")
    dp.run_polling(bot, skip_updates=True)
