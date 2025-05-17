'''
This bot make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 28/05/2024
Ending //

'''
# Installing the necessary libraries
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ContentType
import datetime
from app.keyboards import start_keyboard, admin_keyboard, catalog_navigation_keyboard, catalog_categories_keyboard, booking_keyboard, catalog_navigation_edit_keyboard, edit_apartment_keyboard
from app.database.PostgreSQL_db import create_database, get_catalog_by_category, get_catalog_data, insert_apartment_data, delete_apartment_data, is_apartment_available, update_apartment_data, check_user_exists, insert_user_data, insert_booking_data, get_bookings, insert_review
from app.payment import send_invoice

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
    ADDRESS = State()
    PRICE = State()
    CATEGORY = State()


class EditApartmentState(StatesGroup):
    PHOTO1 = State()
    PHOTO2 = State()
    PHOTO3 = State()
    DESCRIPTION = State()
    ADDRESS = State()
    PRICE = State()
    CATEGORY = State()


class BookingState(StatesGroup):
    FIRST_NAME = State()
    LAST_NAME = State()
    PHONE = State()


class ReviewState(StatesGroup):
    TEXT = State()


# Dictionary to store user data temporarily
USER_DATA = {}
questions = [
    "Загрузите первое фото квартиры:",
    "Загрузите второе фото квартиры:",
    "Загрузите третье фото квартиры:",
    "Введите описание квартиры:",
    "Введите адрес квартиры",
    "Введите цену:",
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
    await state.set_state(AddApartmentState.CATEGORY)
    keyboard = catalog_categories_keyboard()
    await message.answer("Выберите категорию квартиры:", reply_markup=keyboard)


@dp.callback_query(AddApartmentState.CATEGORY)
async def handle_category_selection(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback_query.data)
    await state.set_state(AddApartmentState.PHOTO1)
    await callback_query.message.answer("Загрузите первое фото квартиры:")


@dp.message(AddApartmentState.PHOTO1)
async def handle_first_photo(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(photo1=message.photo[-1].file_id)
        await state.set_state(AddApartmentState.PHOTO2)
        await message.answer("Загрузите второе фото квартиры:")
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@dp.message(AddApartmentState.PHOTO2)
async def handle_second_photo(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(photo2=message.photo[-1].file_id)
        await state.set_state(AddApartmentState.PHOTO3)
        await message.answer("Загрузите третье фото квартиры:")
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@dp.message(AddApartmentState.PHOTO3)
async def handle_third_photo(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(photo3=message.photo[-1].file_id)
        await state.set_state(AddApartmentState.DESCRIPTION)
        await message.answer("Введите описание квартиры:")
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@dp.message(AddApartmentState.DESCRIPTION)
async def handle_description(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(description=message.text)
        await state.set_state(AddApartmentState.ADDRESS)
        await message.answer("Введите адрес квартиры:")
    else:
        await message.answer("Пожалуйста, введите текстовое описание квартиры!")


@dp.message(AddApartmentState.ADDRESS)
async def handle_address(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(address=message.text)
        await state.set_state(AddApartmentState.PRICE)
        await message.answer("Введите цену:")
    else:
        await message.answer("Пожалуйста, введите текстовое значение для адреса!")


@dp.message(AddApartmentState.PRICE)
async def handle_price(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
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
                data["address"],
                data['price'],
                data['category']
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
            # Checking text input
    else:
        await message.answer("Пожалуйста, введите текстовое значение для цены!")


@dp.callback_query(F.data.startswith("update_photo1_"))
async def update_photo1(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PHOTO1)
    await callback_query.message.edit_text(text="Загрузите новое первое фото квартиры:")


@dp.message(EditApartmentState.PHOTO1)
async def handle_update_first_photo(message: types.Message, state: FSMContext):
    # Checking if this is really a photo
    if message.content_type == ContentType.PHOTO:
        index = USER_DATA['apartment_index']
        current_data = get_catalog_data()[index]
        # Updating data using current_data
        photo1 = message.photo[-1].file_id
        photo2 = current_data[3]
        photo3 = current_data[4]
        description = current_data[5]
        address = current_data[6]
        price = current_data[7]
        category = current_data[8]

        update_apartment_data(current_data[0], photo1, photo2, photo3, description, address, price, category)
        # Clear the state after updating the photo
        await state.clear()
        await message.answer("Первое фото успешно обновлено!")
        # Update the displayed apartment data
        await show_editing_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@dp.callback_query(F.data.startswith("update_photo2_"))
async def update_photo2(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PHOTO2)
    await callback_query.message.edit_text(text="Загрузите новое второе фото квартиры:")


@dp.message(EditApartmentState.PHOTO2)
async def handle_update_second_photo(message: types.Message, state: FSMContext):
    # Checking if this is really a photo
    if message.content_type == ContentType.PHOTO:
        index = USER_DATA['apartment_index']
        current_data = get_catalog_data()[index]
        # Updating data using current_data
        photo1 = current_data[2]
        photo2 = message.photo[-1].file_id
        photo3 = current_data[4]
        description = current_data[5]
        address = current_data[6]
        price = current_data[7]
        category = current_data[8]
        update_apartment_data(current_data[0], photo1, photo2, photo3, description, address, price, category)

        # Clear the state after updating the photo
        await state.clear()
        await message.answer("Второе фото успешно обновлено!")
        # Update the displayed apartment data
        await show_editing_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@dp.callback_query(F.data.startswith("update_photo3_"))
async def update_photo3(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PHOTO3)
    await callback_query.message.edit_text(text="Загрузите новое третье фото квартиры:")


@dp.message(EditApartmentState.PHOTO3)
async def handle_update_third_photo(message: types.Message, state: FSMContext):
    # Checking if this is really a photo
    if message.content_type == ContentType.PHOTO:
        index = USER_DATA['apartment_index']
        current_data = get_catalog_data()[index]
        # Updating data using current_data
        photo1 = current_data[2]
        photo2 = current_data[3]
        photo3 = message.photo[-1].file_id
        description = current_data[5]
        address = current_data[6]
        price = current_data[7]
        category = current_data[8]

        update_apartment_data(current_data[0], photo1, photo2, photo3, description, address, price, category)
        # Clear the state after updating the photo
        await state.clear()
        await message.answer("Третье фото успешно обновлено!")
        # Update the displayed apartment data
        await show_editing_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@dp.callback_query(F.data.startswith("update_description_"))
async def update_description(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.DESCRIPTION)
    await callback_query.message.edit_text(text="Введите новое описание квартиры:")


@dp.message(EditApartmentState.DESCRIPTION)
async def handle_update_description(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        index = USER_DATA['apartment_index']
        # Get existing apartment data
        current_data = get_catalog_data()
        apartment_id = current_data[index][0]

        # Updating data using current_data
        photo1 = current_data[index][2]
        photo2 = current_data[index][3]
        photo3 = current_data[index][4]
        description = message.text
        address = current_data[index][6]
        price = current_data[index][7]
        category = current_data[index][8]
        update_apartment_data(apartment_id, photo1, photo2, photo3, description, address, price, category)
        # Clear the state after updating the description
        await state.clear()
        await message.answer("Описание успешно обновлено!")
        # Update the displayed apartment data
        await show_editing_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Введите текст")


@dp.callback_query(F.data.startswith("update_address_"))
async def update_address(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.ADDRESS)
    await callback_query.message.edit_text(text="Введите новый адрес квартиры:")


@dp.message(EditApartmentState.ADDRESS)
async def handle_update_address(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        index = USER_DATA['apartment_index']
        current_data = get_catalog_data()
        apartment_id = current_data[index][0]
        photo1 = current_data[index][2]
        photo2 = current_data[index][3]
        photo3 = current_data[index][4]
        description = current_data[index][5]
        price = current_data[index][7]
        new_address = message.text
        category = current_data[index][8]
        update_apartment_data(apartment_id, photo1, photo2, photo3, description, new_address, price, category)
        # Clear the state after updating the address
        await state.clear()
        await message.answer("Адрес успешно обновлен!")
        await show_editing_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Введите текст для адреса.")


@dp.callback_query(F.data.startswith("update_price_"))
async def update_price(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PRICE)
    await callback_query.message.edit_text(text="Введите новую цену квартиры:")


@dp.message(EditApartmentState.PRICE)
async def handle_update_price(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        index = USER_DATA['apartment_index']
        # Get existing apartment data
        current_data = get_catalog_data()
        # Get the apartment ID by index
        apartment_id = current_data[index][0]
        try:
            # Convert the price to an integer
            price = int(message.text)
            if price <= 0:
                await message.answer("Цена не может быть равна 0 или быть отрицательной. Пожалуйста, введите корректную цену.")
                return

            # Update apartment data using the existing data
            photo1 = current_data[index][2]
            photo2 = current_data[index][3]
            photo3 = current_data[index][4]
            description = current_data[index][5]
            address = current_data[index][6]
            category = current_data[index][8]

            # Updating the data in the database
            update_apartment_data(apartment_id, photo1, photo2, photo3, description, address, price, category)

            # Clear the state after updating the price
            await state.clear()
            await message.answer("Цена успешно обновлена!")

        except ValueError:
            await message.answer("Пожалуйста, введите корректное целое числовое значение для цены.")
            # Updating the displayed apartment data
            await show_editing_apartment_data(message, edit_mode=True)

    else:
        await message.answer("Пожалуйста, введите корректное целое числовое значение для цены.")


# The button to exit the administrator mode
@dp.message(F.text == "⤴️Назад")
async def back_to_main_menu(message: types.Message):
    keyboard = start_keyboard(message.from_user.id)
    await message.answer("Вы вернулись в основное меню.", reply_markup=keyboard)


# Fetch and display apartment listings
@dp.message(F.text == "🛍Каталог")
async def show_catalog_categories(message: types.Message):
    USER_DATA.clear()
    # Set edit mode flag to False for viewing
    USER_DATA['edit_mode'] = False
    keyboard = catalog_categories_keyboard()
    await message.answer("Выберите тип квартиры:", reply_markup=keyboard)


@dp.callback_query(F.data.in_(["one-room_apartment", "two-room_apartment", "three-room_apartment", "studio"]))
async def show_apartments_by_category(callback_query: types.CallbackQuery):
    category = callback_query.data
    apartments = get_catalog_by_category(category)
    if not apartments:
        await callback_query.answer("Квартиры не найдены в этой категории.")
        return

    USER_DATA['apartments'] = apartments
    USER_DATA['apartment_index'] = 0
    # Check if from the edit catalog menu
    is_edit_mode = USER_DATA.get('edit_mode', False)
    if is_edit_mode:
        await show_editing_apartment_data(callback_query.message, edit_mode=True)
    else:
        await get_next_apartment_data(callback_query.message, edit_mode=False, apartments=apartments)


#  Inform user about website availability
@dp.message(F.text == '🌐 Наш сайт')
async def website(message: types.Message):
    await message.answer('Сожалею, но у нас пока нет сайта')


# Provide contact information
@dp.message(F.text == '☎️ Контакты')
async def contact(message: types.Message):
    await message.answer('Наш телефон: 8-901-133-00-00')


# If the directory is empty issue a message
async def get_next_apartment_data(message: types.Message, edit_mode=False, apartments=None):
    if apartments is None:
        apartments = USER_DATA.get('apartments', [])
    if not apartments:
        await message.answer("Каталог пуст!")
        return

    index = USER_DATA.get('apartment_index', 0)
    if index < len(apartments):
        record = apartments[index]

        photos_info = [
            types.InputMediaPhoto(media=record[i], caption=f"Фото квартиры")
            for i in range(2, 5)  # Photos from index 2 to 4
        ]

        description = record[5]
        address = record[6]
        price = record[7]

        message_text = f"Описание квартиры: {description}\nАдрес: {address}\nЦена (в сутки): {price}"

        # Choose the correct keyboard based on edit_mode
        if edit_mode:
            keyboard = catalog_navigation_edit_keyboard(index, len(apartments))
        else:
            keyboard = catalog_navigation_keyboard(index, len(apartments))

        await bot.send_media_group(message.chat.id, media=photos_info)
        await message.answer(message_text, reply_markup=keyboard)
        USER_DATA['apartment_index'] = index


# Displays apartment data with an optional edit mode.
async def show_editing_apartment_data(message: types.Message, edit_mode=False):
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
        address = record[6]
        price = record[7]

        message_text = f"Описание квартиры: {description}\nАдрес: {address}\nЦена (в сутки): {price}"
        keyboard = catalog_navigation_edit_keyboard(index, len(data)) if edit_mode else catalog_navigation_keyboard(index, len(data))

        await bot.send_media_group(message.chat.id, media=photos_info)
        await message.answer(message_text, reply_markup=keyboard)
        USER_DATA['apartment_index'] = index


# Handler for editing the catalog
@dp.message(F.text == "✏️Редактировать каталог")
async def get_apartment_data_edit_handler(message: types.Message, state: FSMContext):
    keyboard = catalog_categories_keyboard()
    # Set edit mode flag
    USER_DATA['edit_mode'] = True
    # Reset the FSM state
    await state.clear()
    await message.answer("Выберите категорию квартиры для редактирования:", reply_markup=keyboard)


# Fetch and display list of bookings
@dp.message(F.text == "📜Список бронирований")
async def show_bookings(message: types.Message):
    bookings = get_bookings()
    if not bookings:
        await message.answer("Бронирования не найдены.")
        return

    bookings_text = "Список бронирований:\n\n"
    for booking in bookings:
        bookings_text += (f"ID брони: {booking[0]}\n"
        f"Имя: {booking[1]} {booking[2]}\n"
        f"Адрес квартиры: {booking[3]}\n"
        f"Дата начала: {booking[4]}\n"
        f"Дата окончания: {booking[5]}\n"
        f"Дней аренды: {booking[6]}\n"
        f"Общая стоимость: {booking[7]} RUB\n\n")

    await message.answer(bookings_text)


# Navigate to the next or previous apartment details
@dp.callback_query(F.data == "add")
async def add_button(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if 'apartment_index' in USER_DATA and 'apartments' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartment = USER_DATA['apartments'][index]
        apartment_id = apartment[0]
        start_date = datetime.datetime.now().date()
        rent_days = USER_DATA.get('rent_days', 1)
        end_date = start_date + datetime.timedelta(days=rent_days)
        # Check if the apartment is available
        if is_apartment_available(apartment_id, start_date, end_date):
            # Check if there is a user in the database
            if check_user_exists(user_id):
                # If the user is already registered, proceed to booking
                keyboard = booking_keyboard()
                await callback_query.message.edit_reply_markup(reply_markup=keyboard)
            else:
                # If the user is not registered, request data
                await state.set_state(BookingState.FIRST_NAME)
                await callback_query.message.answer("👤Для бронирования квартиры потребуется небольшая регистрация. Это займет всего пару минут!\n Эти данные мы не передаем третьим лицам и нигде не публикуем кроме внутренних ресурсов.")
                await callback_query.message.answer("Шаг 1 из 3. 🟩⬜️⬜️")
                await callback_query.message.answer("Введите ваше имя:")
        else:
            # Notify the user that the apartment is already booked
            await callback_query.answer("К сожалению, квартира уже забронирована. Пожалуйста, выберите другую квартиру.")
    else:
        await callback_query.answer("Ошибка: данные о квартире не найдены.")


@dp.message(BookingState.FIRST_NAME)
async def process_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(BookingState.LAST_NAME)
    await message.answer("Шаг 2 из 3. 🟩🟩⬜️")
    await message.answer("Введите вашу фамилию:")


@dp.message(BookingState.LAST_NAME)
async def process_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(BookingState.PHONE)
    await message.answer("Шаг 3 из 3. 🟩🟩🟩")
    await message.answer("Введите ваш номер телефона:")


@dp.message(BookingState.PHONE)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    user_data = await state.get_data()
    user_id = message.from_user.id
    first_name = user_data['first_name']
    last_name = user_data['last_name']
    phone = user_data['phone']

    # Adding the user to the database
    insert_user_data(user_id, first_name, last_name, phone)
    await state.clear()
    await message.answer("Данные сохранены! Теперь вы можете использовать их для будущих бронирований. Продолжайте бронирование.")
    # Getting information about the current apartment
    if 'apartment_index' in USER_DATA and 'apartments' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA['apartments']
        price = apartments[index][7]
        rent_days = USER_DATA.get('rent_days', 1)
        total_price = int(price) * rent_days
        text = f"Количество дней аренды: {rent_days}\nОбщая сумма к оплате: {total_price} RUB"
        keyboard = booking_keyboard()
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer("Ошибка: данные о квартире не найдены.")


@dp.callback_query(F.data == "prev_view")
async def prev_apartment_view(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA.get('apartments', [])
        if index > 0:
            USER_DATA['apartment_index'] = index - 1
            await get_next_apartment_data(callback_query.message, edit_mode=False, apartments=apartments)


@dp.callback_query(F.data == "next_view")
async def next_apartment_view(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA.get('apartments', [])
        if index < len(apartments) - 1:
            USER_DATA['apartment_index'] = index + 1
            await get_next_apartment_data(callback_query.message, edit_mode=False, apartments=apartments)


@dp.callback_query(F.data == "prev_edit")
async def prev_apartment_edit(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        USER_DATA['apartment_index'] = max(index - 1, 0)
        await show_editing_apartment_data(callback_query.message, edit_mode=True)


@dp.callback_query(F.data == "next_edit")
async def next_apartment_edit(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        USER_DATA['apartment_index'] = min(index + 1, len(get_catalog_data()) - 1)
        await show_editing_apartment_data(callback_query.message, edit_mode=True)


# Increase the rental period and calculate the total price
@dp.callback_query(F.data == "add_days")
async def add_days(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA and 'apartments' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA['apartments']
        price = apartments[index][7]
        USER_DATA['rent_days'] = USER_DATA.get('rent_days', 1) + 1
        new_price = int(price) * USER_DATA['rent_days']

        text = f"Количество дней аренды: {USER_DATA['rent_days']}\nОбщая сумма к оплате: {new_price} RUB"
        keyboard = booking_keyboard()
        await callback_query.message.edit_text(text=text, reply_markup=keyboard)


@dp.callback_query(F.data == "subtract_days")
async def subtract_days(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA and 'apartments' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA['apartments']
        price = apartments[index][7]
        USER_DATA['rent_days'] = max(USER_DATA.get('rent_days', 1) - 1, 1)
        new_price = int(price) * USER_DATA['rent_days']

        text = f"Количество дней аренды: {USER_DATA['rent_days']}\nОбщая сумма к оплате: {new_price} RUB"
        keyboard = booking_keyboard()
        await callback_query.message.edit_text(text=text, reply_markup=keyboard)


# Update the payment handler to use the filtered apartments list
@dp.callback_query(F.data == "pay")
async def pay_for_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA and 'apartments' in USER_DATA:
        USER_DATA['current_apartment'] = USER_DATA['apartments'][USER_DATA['apartment_index']]
        await send_invoice(bot, callback_query, USER_DATA)


# Confirm pre-checkout queries
@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# Handle successful payment confirmation
@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await handle_successful_payment(bot, message)


# Handle successful payment
async def handle_successful_payment(bot, message):
    user_id = message.from_user.id
    apartment_id = USER_DATA.get('current_apartment')[0]
    start_date = datetime.datetime.now().date()
    rent_days = USER_DATA.get('rent_days', 1)
    total_price = int(USER_DATA.get('current_apartment')[7]) * rent_days
    insert_booking_data(user_id, apartment_id, start_date, rent_days, total_price)

    await bot.send_message(user_id, "Оплата прошла успешно! Ваше бронирование подтверждено.")


# Add a new handler for deleting an apartment
@dp.callback_query(F.data.startswith("delete_"))
async def delete_apartment(callback_query: types.CallbackQuery):
    # Get the index of the apartment
    index = int(callback_query.data.split("_")[1])
    # Getting the catalog data
    data = get_catalog_data()
    if index < len(data):
        # Get the apartment ID by index
        apartment_id = data[index][0]
        # Deleting an apartment from the database using the ID
        delete_apartment_data(apartment_id)
        await callback_query.answer("Квартира удалена!")


@dp.callback_query(F.data.startswith("edit_"))
async def edit_apartment(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1])
    # Display the keyboard for editing specific fields
    keyboard = edit_apartment_keyboard(index)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)

# Add apartment review
@dp.callback_query(F.data == "add_review")
async def request_review(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(ReviewState.TEXT)
    await callback_query.message.answer("Пожалуйста, введите ваш отзыв:")


@dp.message(ReviewState.TEXT)
async def save_review(message: types.Message, state: FSMContext):
    review_text = message.text
    if 'apartment_index' in USER_DATA and 'apartments' in USER_DATA:
        apartment_id = USER_DATA['apartments'][USER_DATA['apartment_index']][0]
        user_id = message.from_user.id
        insert_review(user_id, apartment_id, review_text)
        await message.answer("Спасибо за ваш отзыв!")
    else:
        await message.answer("Ошибка: не удалось сохранить отзыв.")
    await state.clear()

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
