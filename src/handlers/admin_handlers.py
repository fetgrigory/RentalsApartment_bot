'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 18/09/2025
Ending //
'''
# Installing the necessary libraries
import datetime
import os
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from src.keyboards.admin_keyboard import admin_keyboard, admin_category_keyboard, edit_apartment_keyboard
from src.database.PostgreSQL_db import get_catalog_by_category, get_catalog_data, insert_apartment_data, delete_apartment_data, update_apartment_data, get_bookings, get_reviews
from src.states import AddApartmentState, EditApartmentState
from src.utils.catalog_utils import show_apartment_data, USER_DATA
router = Router()


# Admin Panel
@router.message(F.text == "🛠️Админ-панель")
async def admin_panel_handlerr(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        keyboard = admin_keyboard()
        await message.answer("Добро пожаловать в админ-панель!", reply_markup=keyboard)


# Adding an apartment
@router.message(F.text == "➕Добавить данные")
async def add_data_handler(message: types.Message, state: FSMContext):
    await state.set_state(AddApartmentState.CATEGORY)
    keyboard = admin_category_keyboard()
    await message.answer("Выберите категорию квартиры:", reply_markup=keyboard)


@router.callback_query(AddApartmentState.CATEGORY)
async def handler_category_selection(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback_query.data)
    await state.set_state(AddApartmentState.PHOTO1)
    await callback_query.message.answer("Загрузите первое фото квартиры:")


# A universal function for processing photos when adding an apartment
async def handler_add_photo(message: types.Message, state: FSMContext, next_state, prompt: str):
    if message.content_type != ContentType.PHOTO:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")
        return
    current_state_name = (await state.get_state()).split(':')[-1]
    await state.update_data(**{current_state_name.lower(): message.photo[-1].file_id})
    await state.set_state(next_state)
    await message.answer(prompt)


@router.message(AddApartmentState.PHOTO1)
async def handler_first_photo(message: types.Message, state: FSMContext):
    await handler_add_photo(message, state, AddApartmentState.PHOTO2, "Загрузите второе фото квартиры:")


@router.message(AddApartmentState.PHOTO2)
async def handler_second_photo(message: types.Message, state: FSMContext):
    await handler_add_photo(message, state, AddApartmentState.PHOTO3, "Загрузите третье фото квартиры:")


@router.message(AddApartmentState.PHOTO3)
async def handler_third_photo(message: types.Message, state: FSMContext):
    await handler_add_photo(message, state, AddApartmentState.TOTAL_AREA, "Введите общую площадь квартиры (м²):")


@router.message(AddApartmentState.TOTAL_AREA)
async def handler_total_area(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(total_area=message.text)
        await state.set_state(AddApartmentState.LIVING_AREA)
        await message.answer("Введите общую площадь квартиры (м²):")
    else:
        await message.answer("Пожалуйста, введите числовое значение для общей площади!")


@router.message(AddApartmentState.LIVING_AREA)
async def handler_Living_area(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(living_area=message.text)
        await state.set_state(AddApartmentState.KITCHEN_AREA)
        await message.answer("Введите жилую площадь квартиры (м²):")
    else:
        await message.answer("Пожалуйста, введите числовое значение для жилой площади!")


@router.message(AddApartmentState.KITCHEN_AREA)
async def handler_kitchen_area(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(kitchen_area=message.text)
        await state.set_state(AddApartmentState.DESCRIPTION)
        await message.answer("Введите площадь кухни (м²):")
    else:
        await message.answer("Пожалуйста, введите числовое значение для площади кухни!")


@router.message(AddApartmentState.DESCRIPTION)
async def handler_description(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(description=message.text)
        await state.set_state(AddApartmentState.ADDRESS)
        await message.answer("Введите адрес квартиры:")
    else:
        await message.answer("Пожалуйста, введите текстовое описание квартиры!")


@router.message(AddApartmentState.ADDRESS)
async def handler_address(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(address=message.text)
        await state.set_state(AddApartmentState.PRICE)
        await message.answer("Введите цену:")
    else:
        await message.answer("Пожалуйста, введите текстовое значение для адреса!")


@router.message(AddApartmentState.PRICE)
async def handler_price(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("Пожалуйста, введите текстовое значение для цены!")
        return
    try:
        price = float(message.text)
        if price <= 0:
            await message.answer("Цена не может быть равна 0 или быть отрицательной. Пожалуйста, введите корректную цену.")
            return
        await state.update_data(price=message.text)
        data = await state.get_data()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        apartment_data = [
            current_date,
            data['photo1'],
            data['photo2'],
            data['photo3'],
            data['total_area'],
            data['living_area'],
            data['kitchen_area'],
            data['description'],
            data["address"],
            data['price'],
            data['category']
        ]
        insert_apartment_data(apartment_data)
        await state.clear()
        await message.answer("Данные о квартире успешно сохранены!")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное числовое значение для цены.")


# Редактирование фото
async def handler_update_photo(message: types.Message, state: FSMContext, photo_number: int, success_text: str):
    if message.content_type != ContentType.PHOTO:
        await message.answer("Пожалуйста, загрузите именно фото квартиры!")
        return
    index = USER_DATA['apartment_index']
    current_data = get_catalog_data()[index]
    photos = [current_data[2], current_data[3], current_data[4]]
    photos[photo_number - 1] = message.photo[-1].file_id
    update_apartment_data(
        current_data[0],
        photos[0],
        photos[1],
        photos[2],
        current_data[5],
        current_data[6],
        current_data[7],
        current_data[8]
    )
    USER_DATA['apartments'] = get_catalog_data()
    USER_DATA['apartment_index'] = index
    await state.clear()
    await message.answer(success_text)
    await show_apartment_data(message, edit_mode=True)


@router.message(EditApartmentState.PHOTO1)
async def handler_update_first_photo(message: types.Message, state: FSMContext):
    await handler_update_photo(message, state, 1, "Первое фото успешно обновлено!")


@router.message(EditApartmentState.PHOTO2)
async def handler_update_second_photo(message: types.Message, state: FSMContext):
    await handler_update_photo(message, state, 2, "Второе фото успешно обновлено!")


@router.message(EditApartmentState.PHOTO3)
async def handler_update_third_photo(message: types.Message, state: FSMContext):
    await handler_update_photo(message, state, 3, "Третье фото успешно обновлено!")


@router.callback_query(F.data.startswith("update_description_"))
async def update_description(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.DESCRIPTION)
    await callback_query.message.edit_text(text="Введите новое описание квартиры:")


@router.message(EditApartmentState.DESCRIPTION)
async def handler_update_description(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("Введите текст")
        return
    index = USER_DATA['apartment_index']
    current_data = get_catalog_data()
    apartment_id = current_data[index][0]
    update_apartment_data(
        apartment_id,
        current_data[index][2],
        current_data[index][3],
        current_data[index][4],
        message.text,
        current_data[index][6],
        current_data[index][7],
        current_data[index][8]
    )
    USER_DATA['apartments'] = get_catalog_data()
    await state.clear()
    await message.answer("Описание успешно обновлено!")
    await show_apartment_data(message, edit_mode=True)


@router.callback_query(F.data.startswith("update_address_"))
async def update_address(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.ADDRESS)
    await callback_query.message.edit_text(text="Введите новый адрес квартиры:")


@router.message(EditApartmentState.ADDRESS)
async def handler_update_address(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("Введите текст для адреса.")
        return
    index = USER_DATA['apartment_index']
    current_data = get_catalog_data()
    apartment_id = current_data[index][0]
    update_apartment_data(
        apartment_id,
        current_data[index][2],
        current_data[index][3],
        current_data[index][4],
        current_data[index][5],
        message.text,
        current_data[index][7],
        current_data[index][8]
    )
    USER_DATA['apartments'] = get_catalog_data()
    await state.clear()
    await message.answer("Адрес успешно обновлен!")
    await show_apartment_data(message, edit_mode=True)


@router.callback_query(F.data.startswith("update_price_"))
async def update_price(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[2])
    USER_DATA['apartment_index'] = index
    await state.set_state(EditApartmentState.PRICE)
    await callback_query.message.edit_text(text="Введите новую цену квартиры:")


@router.message(EditApartmentState.PRICE)
async def handler_update_price(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("Пожалуйста, введите корректное целое числовое значение для цены.")
        return
    index = USER_DATA['apartment_index']
    current_data = get_catalog_data()
    apartment_id = current_data[index][0]
    try:
        price = int(message.text)
        if price <= 0:
            await message.answer("Цена не может быть равна 0 или быть отрицательной. Пожалуйста, введите корректную цену.")
            return
        update_apartment_data(
            apartment_id,
            current_data[index][2],
            current_data[index][3],
            current_data[index][4],
            current_data[index][5],
            current_data[index][6],
            price,
            current_data[index][8]
        )
        USER_DATA['apartments'] = get_catalog_data()
        await state.clear()
        await message.answer("Цена успешно обновлена!")
        await show_apartment_data(message, edit_mode=True)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное целое числовое значение для цены.")


# Catalog
@router.message(F.text == "🛍Каталог")
async def show_catalog_categories(message: types.Message):
    USER_DATA.clear()
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


@router.message(F.text == "✏️Редактировать каталог")
async def get_apartment_data_edit_handlerr(message: types.Message, state: FSMContext):
    keyboard = admin_category_keyboard()
    USER_DATA['edit_mode'] = True
    await state.clear()
    await message.answer("Выберите категорию квартиры для редактирования:", reply_markup=keyboard)


@router.callback_query(F.data.in_(["prev_view", "prev_edit"]))
async def prev_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA.get('apartments', get_catalog_data())
        if index > 0:
            USER_DATA['apartment_index'] = index - 1
            is_edit_mode = callback_query.data == "prev_edit"
            await show_apartment_data(callback_query.message, edit_mode=is_edit_mode, apartments=apartments)

@router.callback_query(F.data.in_(["next_view", "next_edit"]))
async def next_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        apartments = USER_DATA.get('apartments', get_catalog_data())
        if index < len(apartments) - 1:
            USER_DATA['apartment_index'] = index + 1
            is_edit_mode = callback_query.data == "next_edit"
            await show_apartment_data(callback_query.message, edit_mode=is_edit_mode, apartments=apartments)


# Delete and edit
@router.callback_query(F.data.startswith("delete_"))
async def delete_apartment(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1])
    data = get_catalog_data()
    if index < len(data):
        apartment_id = data[index][0]
        delete_apartment_data(apartment_id)
        await callback_query.answer("Квартира удалена!")


@router.callback_query(F.data.startswith("edit_"))
async def edit_apartment(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1])
    keyboard = edit_apartment_keyboard(index)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)


# Reviews and bookings
@router.message(F.text == "📝Просмотр отзывов")
async def show_reviews(message: types.Message):
    reviews = get_reviews()
    if not reviews:
        await message.answer("Отзывы не найдены.")
        return
    reviews_text = "Список отзывов:\n\n"
    for review in reviews:
        reviews_text += (
            f"ID отзыва: {review[0]}\n"
            f"ID квартиры: {review[2]}\n"
            f"Текст отзыва: {review[3]}\n"
            f"Оценка: {review[4]} ({review[5]})\n"
            f"Дата: {review[6]}\n\n"
        )
    await message.answer(reviews_text)


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
