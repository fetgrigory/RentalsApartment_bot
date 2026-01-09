'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/01/2026
Ending //

'''
# Installing the necessary libraries
from aiogram import F, Router, types
from src.keyboards.admin_keyboard import admin_category_keyboard
from src.database.PostgreSQL_db import get_catalog_data, get_catalog_by_category
from src.utils.catalog_utils import USER_DATA, show_apartment_data

router = Router()


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
    await show_apartment_data(callback_query.message, edit_mode=USER_DATA.get('edit_mode', False), apartments=apartments)


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


@router.message(F.text == "✏️Редактировать каталог")
async def get_apartment_data_edit_handlerr(message: types.Message):
    USER_DATA['edit_mode'] = True
    keyboard = admin_category_keyboard()
    await message.answer("Выберите категорию квартиры для редактирования:", reply_markup=keyboard)
