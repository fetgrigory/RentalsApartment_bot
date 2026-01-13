"""
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/01/2026
Ending //
"""
# Installing the necessary libraries
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from src.keyboards.admin_keyboard import edit_apartment_keyboard
from src.db.crud import get_catalog_data, update_apartment_data, delete_apartment_data
from src.states import EditApartmentState
from src.utils.catalog_utils import USER_DATA, show_apartment_data

router = Router()


# Delete apartment
@router.callback_query(F.data.startswith("delete_"))
async def delete_apartment(callback_query: types.CallbackQuery):
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        delete_apartment_data(apartment.id)
    await callback_query.answer("Квартира удалена!")


# Edit apartment menu
@router.callback_query(F.data.startswith("edit_"))
async def edit_apartment(callback_query: types.CallbackQuery):
    apartment_id = int(callback_query.data.split("_")[1])
    keyboard = edit_apartment_keyboard(apartment_id)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()


# Update description
@router.callback_query(F.data.startswith("update_description_"))
async def update_description(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.DESCRIPTION)
    await callback_query.message.edit_text("Введите новое описание квартиры:")


@router.message(EditApartmentState.DESCRIPTION)
async def handler_update_description(message: types.Message, state: FSMContext):
    if message.content_type != types.ContentType.TEXT:
        await message.answer("Введите текст")
        return
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        apartment.description = message.text
        update_apartment_data(
            apartment.id,
            apartment.photo1,
            apartment.photo2,
            apartment.photo3,
            apartment.total_area,
            apartment.living_area,
            apartment.kitchen_area,
            apartment.description,
            apartment.address,
            apartment.price,
            apartment.category
        )
        USER_DATA['apartments'] = get_catalog_data()
        await state.clear()
        await message.answer("Описание успешно обновлено!")
        await show_apartment_data(message, edit_mode=True)


# Update address
@router.callback_query(F.data.startswith("update_address_"))
async def update_address(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.ADDRESS)
    await callback_query.message.edit_text("Введите новый адрес квартиры:")


@router.message(EditApartmentState.ADDRESS)
async def handler_update_address(message: types.Message, state: FSMContext):
    if message.content_type != types.ContentType.TEXT:
        await message.answer("Введите текст для адреса.")
        return
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        apartment.address = message.text
        update_apartment_data(
            apartment.id,
            apartment.photo1,
            apartment.photo2,
            apartment.photo3,
            apartment.total_area,
            apartment.living_area,
            apartment.kitchen_area,
            apartment.description,
            apartment.address,
            apartment.price,
            apartment.category
        )
        USER_DATA['apartments'] = get_catalog_data()
        await state.clear()
        await message.answer("Адрес успешно обновлен!")
        await show_apartment_data(message, edit_mode=True)


# Update price
@router.callback_query(F.data.startswith("update_price_"))
async def update_price(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.PRICE)
    await callback_query.message.edit_text("Введите новую цену квартиры:")


@router.message(EditApartmentState.PRICE)
async def handler_update_price(message: types.Message, state: FSMContext):
    if message.content_type != types.ContentType.TEXT:
        await message.answer("Введите числовое значение для цены.")
        return
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        try:
            price = int(message.text)
            if price <= 0:
                await message.answer("Цена не может быть равна 0 или быть отрицательной.")
                return
            apartment.price = price
            update_apartment_data(
                apartment.id,
                apartment.photo1,
                apartment.photo2,
                apartment.photo3,
                apartment.total_area,
                apartment.living_area,
                apartment.kitchen_area,
                apartment.description,
                apartment.address,
                apartment.price,
                apartment.category
            )
            USER_DATA['apartments'] = get_catalog_data()
            await state.clear()
            await message.answer("Цена успешно обновлена!")
            await show_apartment_data(message, edit_mode=True)
        except ValueError:
            await message.answer("Введите корректное целое числовое значение для цены.")
