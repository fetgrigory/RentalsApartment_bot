import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import logging
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Router, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from bot.handlers.user_handlers import router as user_router
from bot.handlers.catalog_handlers import router as catalog_router
from bot.nlp.rag.add_document_handlers import router as document_router
from bot.keyboards.user_keyboard import start_keyboard

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher in combination with state storage
load_dotenv()
router = Router()


TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logger.critical("TOKEN не задан в переменных окружения!")
    raise RuntimeError("TOKEN не задан!")

# Setting up the bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

# Connecting routers
dp.include_router(router)
dp.include_router(user_router)
dp.include_router(catalog_router)
dp.include_router(document_router)


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    logger.info("User pressed /start")
    await state.clear()
    keyboard = start_keyboard()
    me = await message.bot.get_me()
    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}!\n"
        f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
        parse_mode='html',
        reply_markup=keyboard
    )


async def main():
    logger.info("Start polling")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
