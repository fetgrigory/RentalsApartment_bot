'''
This bot make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 28/05/2024
Ending //

'''
# Installing the necessary libraries
import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ContentType
import datetime
from app.keyboards import start_keyboard, admin_keyboard, catalog_navigation_keyboard, booking_keyboard
from app.database import create_database, get_catalog_data, insert_apartment_data
from app.payment import send_invoice, handle_successful_payment


load_dotenv()  # Load environment variables from a .env file.
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)
# Dictionary to store user data temporarily.
USER_DATA = {}
questions = [
    "Загрузите первое фото квартиры:",
    "Загрузите второе фото квартиры:",
    "Загрузите третье фото квартиры:",
    "Введите описание квартиры:",
    "Введите цену:"
]
# Initialize or open database connection.
create_database()
# Making sure that the bot is running
print('Бот успешно запущен!')

# Handle the /start command to greet the user
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    USER_DATA.clear()

    keyboard = start_keyboard(message.from_user.id)
    me = await bot.get_me()
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!\n"
                         f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
                         parse_mode='html', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "🛠️Админ-панель")
async def admin_panel_handler(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        keyboard = admin_keyboard()
        await message.answer("Добро пожаловать в админ-панель!", reply_markup=keyboard)
# Start data entry process for a new apartment
@dp.message_handler(lambda message: message.text == "Добавить данные")
async def add_data_handler(message: types.Message):
    USER_DATA.clear()
    await ask_next_question(message)
# The button to exit the administrator mode
@dp.message_handler(lambda message: message.text == "Назад")
async def back_to_main_menu(message: types.Message):
    keyboard = start_keyboard(message.from_user.id)
    await message.answer("Вы вернулись в основное меню.", reply_markup=keyboard)
# Fetch and display apartment listings
@dp.message_handler(lambda message: message.text == "🛍Каталог")
async def get_apartment_data_handler(message: types.Message):
    await get_next_apartment_data(message)
# Inform user about website availability
@dp.message_handler(text='🌐 Наш сайт')
async def website(message: types.Message):
    await message.answer('Сожалею, но у нас пока нет сайта')
# Provide contact information
@dp.message_handler(text='☎️ Контакты')
async def call(message: types.Message):
    await message.answer('Наш телефон: 8-901-133-00-00')
# Prompt the next question for apartment details
async def ask_next_question(message: types.Message):
    if len(USER_DATA) < len(questions):
        question = questions[len(USER_DATA)]
        await message.answer(question)
        USER_DATA['current_question'] = question
    else:
        await save_apartment_data(message)
# Handle photo uploads during apartment data entry
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    if 'current_question' in USER_DATA:
        file_id = message.photo[-1].file_id
        USER_DATA[USER_DATA['current_question']] = file_id
        del USER_DATA['current_question']
        await ask_next_question(message)

@dp.message_handler()
async def add_apartment(message: types.Message):
    answer = message.text
    if 'current_question' in USER_DATA:
        USER_DATA[USER_DATA['current_question']] = answer
        del USER_DATA['current_question']
        await ask_next_question(message)
# Save all collected apartment data to the database
async def save_apartment_data(message: types.Message):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [
        current_date,
        USER_DATA.get(questions[0], ""),
        USER_DATA.get(questions[1], ""),
        USER_DATA.get(questions[2], ""),
        USER_DATA.get(questions[3], ""),
        USER_DATA.get(questions[4], "")
    ]
    insert_apartment_data(data)
    await message.answer("Данные о квартире успешно сохранены!")
# Retrieve and display the next apartment in the catalog
async def get_next_apartment_data(message: types.Message):
    data = get_catalog_data()
    index = USER_DATA.get('apartment_index', 0)

    if index < len(data):
        record = data[index]

        photos_info = []
        for i in range(2, 5):
            photo_id = record[i]
            photos_info.append(types.InputMediaPhoto(media=photo_id, caption=f"Фото квартиры"))

        description = record[5]
        price = record[6]

        message_text = f"Описание квартиры: {description}\nЦена(в сутки): {price}"
        keyboard = catalog_navigation_keyboard(index, len(data))

        await bot.send_media_group(message.chat.id, media=photos_info)
        await message.answer(message_text, reply_markup=keyboard)
        USER_DATA['apartment_index'] = index
# Navigate to the next or previous apartment details
@dp.callback_query_handler(text="add")
async def add_button(callback_query: types.CallbackQuery):
    USER_DATA['added_button'] = True
    keyboard = booking_keyboard()
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=keyboard)
# Show the previous apartment
@dp.callback_query_handler(text="prev")
async def prev_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        USER_DATA['apartment_index'] = max(index - 1, 0)
        await get_next_apartment_data(callback_query.message)
# Show the next apartment
@dp.callback_query_handler(text="next")
async def next_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        USER_DATA['apartment_index'] = min(index + 1, len(get_catalog_data()) - 1)
        await get_next_apartment_data(callback_query.message)
# Increase the rental period and calculate the total price
@dp.callback_query_handler(text="add_days")
async def add_days(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        price = get_catalog_data()[index][6]
        USER_DATA['rent_days'] = USER_DATA.get('rent_days', 1) + 1
        new_price = int(price) * USER_DATA['rent_days']

        text = f"Количество дней аренды: {USER_DATA['rent_days']}\nОбщая сумма к оплате: {new_price} RUB"
        keyboard = booking_keyboard()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text, reply_markup=keyboard)
# Decrease the rental period but ensure it's at least 1 day
@dp.callback_query_handler(text="subtract_days")
async def subtract_days(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        price = get_catalog_data()[index][6]
        USER_DATA['rent_days'] = max(USER_DATA.get('rent_days', 1) - 1, 1)
        new_price = int(price) * USER_DATA['rent_days']

        text = f"Количество дней аренды: {USER_DATA['rent_days']}\nОбщая сумма к оплате: {new_price} RUB"
        keyboard = booking_keyboard()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text, reply_markup=keyboard)
# Handle the payment process for renting the apartment
@dp.callback_query_handler(text="pay")
async def pay_for_apartment(callback_query: types.CallbackQuery):
    await send_invoice(bot, callback_query, USER_DATA)
# Confirm pre-checkout queries
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
# Handle successful payment confirmation
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await handle_successful_payment(bot, message)
# Starting the polling loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())
