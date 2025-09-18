'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 15/09/2025
Ending //
'''
# Installing the necessary libraries
import datetime
import os
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from app.keyboards.admin_keyboard import admin_keyboard, catalog_navigation_edit_keyboard, admin_category_keyboard, edit_apartment_keyboard
from app.database.PostgreSQL_db import get_catalog_by_category, get_catalog_data, insert_apartment_data, delete_apartment_data, update_apartment_data, get_bookings
from app.states import AddApartmentState, EditApartmentState
router = Router()

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


@router.message(F.text == "🛠️Админ-панель")
async def admin_panel_handler(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        keyboard = admin_keyboard()
        await message.answer("Добро пожаловать в админ-панель!", reply_markup=keyboard)


# Start data entry process for a new apartment
@router.message(F.text == "➕Добавить данные")
async def add_data_handler(message: types.Message, state: FSMContext):
    await state.set_state(AddApartmentState.CATEGORY)
    keyboard = admin_category_keyboard()
    await message.answer("Выберите категорию квартиры:", reply_markup=keyboard)


@router.callback_query(AddApartmentState.CATEGORY)
async def handle_category_selection(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback_query.data)
    await state.set_state(AddApartmentState.PHOTO1)
    await callback_query.message.answer("Загрузите первое фото квартиры:")


@router.message(AddApartmentState.PHOTO1)
async def handle_first_photo(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(photo1=message.photo[-1].file_id)
        await state.set_state(AddApartmentState.PHOTO2)
        await message.answer("Загрузите второе фото квартиры:")
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@router.message(AddApartmentState.PHOTO2)
async def handle_second_photo(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(photo2=message.photo[-1].file_id)
        await state.set_state(AddApartmentState.PHOTO3)
        await message.answer("Загрузите третье фото квартиры:")
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@router.message(AddApartmentState.PHOTO3)
async def handle_third_photo(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(photo3=message.photo[-1].file_id)
        await state.set_state(AddApartmentState.DESCRIPTION)
        await message.answer("Введите описание квартиры:")
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@router.message(AddApartmentState.DESCRIPTION)
async def handle_description(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(description=message.text)
        await state.set_state(AddApartmentState.ADDRESS)
        await message.answer("Введите адрес квартиры:")
    else:
        await message.answer("Пожалуйста, введите текстовое описание квартиры!")


@router.message(AddApartmentState.ADDRESS)
async def handle_address(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(address=message.text)
        await state.set_state(AddApartmentState.PRICE)
        await message.answer("Введите цену:")
    else:
        await message.answer("Пожалуйста, введите текстовое значение для адреса!")


@router.message(AddApartmentState.PRICE)
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


@router.callback_query(F.data.startswith("update_photo1_"))
async def update_photo1(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PHOTO1)
    await callback_query.message.edit_text(text="Загрузите новое первое фото квартиры:")


@router.message(EditApartmentState.PHOTO1)
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
        # Updating the cache
        USER_DATA['apartments'] = get_catalog_data()
        USER_DATA['apartment_index'] = index
        # Clear the state after updating the photo
        await state.clear()
        await message.answer("Первое фото успешно обновлено!")
        # Update the displayed apartment data
        await show_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@router.callback_query(F.data.startswith("update_photo2_"))
async def update_photo2(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PHOTO2)
    await callback_query.message.edit_text(text="Загрузите новое второе фото квартиры:")


@router.message(EditApartmentState.PHOTO2)
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
        # Updating the cache
        USER_DATA['apartments'] = get_catalog_data()
        USER_DATA['apartment_index'] = index
        # Clear the state after updating the photo
        await state.clear()
        await message.answer("Второе фото успешно обновлено!")
        # Update the displayed apartment data
        await show_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@router.callback_query(F.data.startswith("update_photo3_"))
async def update_photo3(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PHOTO3)
    await callback_query.message.edit_text(text="Загрузите новое третье фото квартиры:")


@router.message(EditApartmentState.PHOTO3)
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
        # Updating the cache
        USER_DATA['apartments'] = get_catalog_data()
        USER_DATA['apartment_index'] = index
        # Clear the state after updating the photo
        await state.clear()
        await message.answer("Третье фото успешно обновлено!")
        # Update the displayed apartment data
        await show_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")


@router.callback_query(F.data.startswith("update_description_"))
async def update_description(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.DESCRIPTION)
    await callback_query.message.edit_text(text="Введите новое описание квартиры:")


@router.message(EditApartmentState.DESCRIPTION)
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
        # Updating the cache
        USER_DATA['apartments'] = get_catalog_data()
        USER_DATA['apartment_index'] = index
        # Clear the state after updating the description
        await state.clear()
        await message.answer("Описание успешно обновлено!")
        # Update the displayed apartment data
        await show_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Введите текст")


@router.callback_query(F.data.startswith("update_address_"))
async def update_address(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.ADDRESS)
    await callback_query.message.edit_text(text="Введите новый адрес квартиры:")


@router.message(EditApartmentState.ADDRESS)
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
        # Updating the cache
        USER_DATA['apartments'] = get_catalog_data()
        USER_DATA['apartment_index'] = index
        # Clear the state after updating the address
        await state.clear()
        await message.answer("Адрес успешно обновлен!")
        await show_apartment_data(message, edit_mode=True)
    else:
        await message.answer("Введите текст для адреса.")


@router.callback_query(F.data.startswith("update_price_"))
async def update_price(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PRICE)
    await callback_query.message.edit_text(text="Введите новую цену квартиры:")


@router.message(EditApartmentState.PRICE)
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
            # Updating the cache
            USER_DATA['apartments'] = get_catalog_data()
            USER_DATA['apartment_index'] = index
            # Clear the state after updating the price
            await state.clear()
            await message.answer("Цена успешно обновлена!")
            await show_apartment_data(message, edit_mode=True)

        except ValueError:
            await message.answer("Пожалуйста, введите корректное целое числовое значение для цены.")
    else:
        await message.answer("Пожалуйста, введите корректное целое числовое значение для цены.")


# Fetch and display apartment listings
@router.message(F.text == "🛍Каталог")
async def show_catalog_categories(message: types.Message):
    USER_DATA.clear()
    # Set edit mode flag to False for viewing
    USER_DATA['edit_mode'] = False
    USER_DATA['apartments'] = get_catalog_data()
    keyboard = admin_category_keyboard()
    await message.answer("Выберите тип квартиры:", reply_markup=keyboard)


@router.callback_query(F.data.in_(["one-room_apartment", "two-room_apartment", "three-room_apartment", "studio"]))
async def show_apartments_by_category(callback_query: types.CallbackQuery):
    category = callback_query.data
    apartments = get_catalog_by_category(category)
    if not apartments:
        await callback_query.answer("Квартиры не найдены в этой категории.")
        return

    USER_DATA['apartments'] = apartments
    USER_DATA['apartment_index'] = 0
    is_edit_mode = USER_DATA.get('edit_mode', False)
    await show_apartment_data(callback_query.message, edit_mode=is_edit_mode, apartments=apartments)


# Apartment data display function
async def show_apartment_data(message: types.Message, edit_mode=False, apartments=None):
    if apartments is None:
        apartments = USER_DATA.get('apartments', get_catalog_data())
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

        # Keyboard selection depending on the mode
        if edit_mode:
            keyboard = catalog_navigation_edit_keyboard(index, len(apartments))
        else:
            keyboard = admin_catalog_navigation_keyboard(index, len(apartments))

        await message.bot.send_media_group(message.chat.id, media=photos_info)
        await message.answer(message_text, reply_markup=keyboard)
        USER_DATA['apartment_index'] = index
        USER_DATA['apartments'] = apartments


# Handler for editing the catalog
@router.message(F.text == "✏️Редактировать каталог")
async def get_apartment_data_edit_handler(message: types.Message, state: FSMContext):
    keyboard = admin_category_keyboard()
    # Set edit mode flag
    USER_DATA['edit_mode'] = True
    # Reset the FSM state
    await state.clear()
    await message.answer("Выберите категорию квартиры для редактирования:", reply_markup=keyboard)


# Handler for the previous record
@router.callback_query(F.data.in_(["prev_view", "prev_edit"]))
async def prev_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA.get('apartments', get_catalog_data())
        if index > 0:
            USER_DATA['apartment_index'] = index - 1
            is_edit_mode = callback_query.data == "prev_edit"
            await show_apartment_data(callback_query.message, edit_mode=is_edit_mode, apartments=apartments)


# Handler for the next record
@router.callback_query(F.data.in_(["next_view", "next_edit"]))
async def next_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA.get('apartments', get_catalog_data())
        if index < len(apartments) - 1:
            USER_DATA['apartment_index'] = index + 1
            is_edit_mode = callback_query.data == "next_edit"
            await show_apartment_data(callback_query.message, edit_mode=is_edit_mode, apartments=apartments)


# Add a new handler for deleting an apartment
@router.callback_query(F.data.startswith("delete_"))
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


@router.callback_query(F.data.startswith("edit_"))
async def edit_apartment(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1])
    # Display the keyboard for editing specific fields
    keyboard = edit_apartment_keyboard(index)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)


# Fetch and display list of bookings
@router.message(F.text == "📜Список бронирований")
async def show_bookings(message: types.Message):
    bookings = get_bookings()
    if not bookings:
        await message.answer("Бронирования не найдены.")
        return

    bookings_text = "Список бронирований:\n\n"
    for booking in bookings:
        bookings_text += (f"ID брони: {booking[0]}\n"
        f"Имя: {booking[1]} {booking[2]}\n"
        f"Телефон: {booking[8]}\n"
        f"Адрес квартиры: {booking[3]}\n"
        f"Дата начала: {booking[4]}\n"
        f"Дата окончания: {booking[5]}\n"
        f"Дней аренды: {booking[6]}\n"
        f"Общая стоимость: {booking[7]} RUB\n\n")

    await message.answer(bookings_text)