'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/01/2026
Ending //

'''
# Installing the necessary libraries
import datetime
import os
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from src.keyboards.admin_keyboard import admin_keyboard, admin_category_keyboard
from src.database.PostgreSQL_db import insert_apartment_data
from src.states import AddApartmentState

router = Router()


# Admin Panel
@router.message(F.text == "🛠️Админ-панель")
async def admin_panel_handler(message: types.Message):
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


# Apartment data
@router.message(AddApartmentState.TOTAL_AREA)
async def handler_total_area(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(total_area=message.text)
        await state.set_state(AddApartmentState.LIVING_AREA)
        await message.answer("Введите жилую площадь квартиры (м²):")
    else:
        await message.answer("Пожалуйста, введите числовое значение для общей площади!")


@router.message(AddApartmentState.LIVING_AREA)
async def handler_living_area(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(living_area=message.text)
        await state.set_state(AddApartmentState.KITCHEN_AREA)
        await message.answer("Введите площадь кухни (м²):")
    else:
        await message.answer("Пожалуйста, введите числовое значение для жилой площади!")


@router.message(AddApartmentState.KITCHEN_AREA)
async def handler_kitchen_area(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(kitchen_area=message.text)
        await state.set_state(AddApartmentState.DESCRIPTION)
        await message.answer("Введите описание квартиры:")
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
