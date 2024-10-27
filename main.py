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
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ContentType
import datetime
from app.keyboards import start_keyboard, admin_keyboard, catalog_navigation_keyboard, booking_keyboard
# from app.database import create_database, get_catalog_data, insert_apartment_data
from app.PostgreSQL import create_database, get_catalog_data, insert_apartment_data
from app.payment import send_invoice, handle_successful_payment

# Initialize bot and dispatcher in combination with state storage
load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# States group
class AddApartmentState(StatesGroup):
    PHOTO1 = State()
    PHOTO2 = State()
    PHOTO3 = State()
    DESCRIPTION = State()
    PRICE = State()


# Dictionary to store user data temporarily
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


@dp.message(Command("start"))
async def start(message: types.Message):
    USER_DATA.clear()

    keyboard = start_keyboard(message.from_user.id)
    me = await bot.get_me()
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!\n"
                         f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
                         parse_mode='html', reply_markup=keyboard)


@dp.message(F.text == "🛠️Админ-панель")
async def admin_panel_handler(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        keyboard = admin_keyboard()
        await message.answer("Добро пожаловать в админ-панель!", reply_markup=keyboard)


# Start data entry process for a new apartment
@dp.message(F.text == "➕Добавить данные")
async def add_data_handler(message: types.Message, state: FSMContext):
    await state.set_state(AddApartmentState.PHOTO1)
    await message.answer("Загрузите первое фото квартиры:")


@dp.message(AddApartmentState.PHOTO1, F.content_type == ContentType.PHOTO)
async def handle_first_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo1=message.photo[-1].file_id)
    await state.set_state(AddApartmentState.PHOTO2)
    await message.answer("Загрузите второе фото квартиры:")


@dp.message(AddApartmentState.PHOTO2, F.content_type == ContentType.PHOTO)
async def handle_second_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo2=message.photo[-1].file_id)
    await state.set_state(AddApartmentState.PHOTO3)
    await message.answer("Загрузите третье фото квартиры:")


@dp.message(AddApartmentState.PHOTO3, F.content_type == ContentType.PHOTO)
async def handle_third_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo3=message.photo[-1].file_id)
    await state.set_state(AddApartmentState.DESCRIPTION)
    await message.answer("Введите описание квартиры:")


@dp.message(AddApartmentState.DESCRIPTION)
async def handle_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddApartmentState.PRICE)
    await message.answer("Введите цену:")


@dp.message(AddApartmentState.PRICE)
async def handle_price(message: types.Message, state: FSMContext):
    try:
        # Attempt to convert the text message into a float representing the price
        price = float(message.text)

        # Check if the price is valid (greater than 0)
        if price <= 0:
            # Send a message to the user if the price is invalid
            await message.answer("Цена не может быть равна 0 или быть отрицательной. Пожалуйста, введите корректную цену.")
            return
        # Update the FSM context with the valid price data
        await state.update_data(price=message.text)

        # Retrieve all data collected so far in the FSM context
        data = await state.get_data()

        # Get the current date and time, formatted as a string
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create a list containing the data to be inserted into the database
        apartment_data = [
            current_date,
            data['photo1'],
            data['photo2'],
            data['photo3'],
            data['description'],
            data['price']
        ]

        # Call a function to insert the data into the database
        insert_apartment_data(apartment_data)

        # Clear the FSM context, indicating the end of the data collection process
        await state.clear()

        # Inform the user that the apartment data has been successfully saved
        await message.answer("Данные о квартире успешно сохранены!")

    except ValueError:
        # Handle the case where the provided price is not a valid float
        await message.answer("Пожалуйста, введите корректное числовое значение для цены.")


# The button to exit the administrator mode
@dp.message(F.text == "⤴️Назад")
async def back_to_main_menu(message: types.Message):
    keyboard = start_keyboard(message.from_user.id)
    await message.answer("Вы вернулись в основное меню.", reply_markup=keyboard)


# Fetch and display apartment listings
@dp.message(F.text == "🛍Каталог")
async def get_apartment_data_handler(message: types.Message):
    await get_next_apartment_data(message)


#  Inform user about website availability
@dp.message(F.text == '🌐 Наш сайт')
async def website(message: types.Message):
    await message.answer('Сожалею, но у нас пока нет сайта')


# Provide contact information
@dp.message(F.text == '☎️ Контакты')
async def contact(message: types.Message):
    await message.answer('Наш телефон: 8-901-133-00-00')


# If the directory is empty issue a message
async def get_next_apartment_data(message: types.Message):
    data = get_catalog_data()
    if not data:
        await message.answer("Каталог пуст!")
        return

    index = USER_DATA.get('apartment_index', 0)
    if index < len(data):
        record = data[index]

        photos_info = [
            types.InputMediaPhoto(media=record[i], caption=f"Фото квартиры")
            for i in range(2, 5)
        ]

        description = record[5]
        price = record[6]

        message_text = f"Описание квартиры: {description}\nЦена(в сутки): {price}"
        keyboard = catalog_navigation_keyboard(index, len(data))

        await bot.send_media_group(message.chat.id, media=photos_info)
        await message.answer(message_text, reply_markup=keyboard)
        USER_DATA['apartment_index'] = index


# Navigate to the next or previous apartment details
@dp.callback_query(F.data == "add")
async def add_button(callback_query: types.CallbackQuery):
    USER_DATA['added_button'] = True
    keyboard = booking_keyboard()
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)


# Show the previous apartment
@dp.callback_query(F.data == "prev")
async def prev_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        USER_DATA['apartment_index'] = max(index - 1, 0)
        await get_next_apartment_data(callback_query.message)


# Show the next apartment
@dp.callback_query(F.data == "next")
async def next_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        USER_DATA['apartment_index'] = min(index + 1, len(get_catalog_data()) - 1)
        await get_next_apartment_data(callback_query.message)


# Increase the rental period and calculate the total price
@dp.callback_query(F.data == "add_days")
async def add_days(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        price = get_catalog_data()[index][6]
        USER_DATA['rent_days'] = USER_DATA.get('rent_days', 1) + 1
        new_price = int(price) * USER_DATA['rent_days']

        text = f"Количество дней аренды: {USER_DATA['rent_days']}\nОбщая сумма к оплате: {new_price} RUB"
        keyboard = booking_keyboard()
        await callback_query.message.edit_text(text=text, reply_markup=keyboard)


@dp.callback_query(F.data == "subtract_days")
async def subtract_days(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        price = get_catalog_data()[index][6]
        USER_DATA['rent_days'] = max(USER_DATA.get('rent_days', 1) - 1, 1)
        new_price = int(price) * USER_DATA['rent_days']

        text = f"Количество дней аренды: {USER_DATA['rent_days']}\nОбщая сумма к оплате: {new_price} RUB"
        keyboard = booking_keyboard()
        await callback_query.message.edit_text(text=text, reply_markup=keyboard)


# Handle the payment process for renting the apartment
@dp.callback_query(F.data == "pay")
async def pay_for_apartment(callback_query: types.CallbackQuery):
    await send_invoice(bot, callback_query, USER_DATA)


# Confirm pre-checkout queries
@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# Handle successful payment confirmation
@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await handle_successful_payment(bot, message)

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
