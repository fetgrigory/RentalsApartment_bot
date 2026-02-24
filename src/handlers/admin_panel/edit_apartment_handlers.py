"""
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/01/2026
Ending //
"""
# Installing the necessary libraries
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sentence_transformers import SentenceTransformer
from src.db.crud import delete_apartment_data, get_catalog_data, update_apartment_data
from src.keyboards.admin_keyboard import edit_apartment_keyboard
from src.states import EditApartmentState
from src.utils.catalog_utils import USER_DATA, show_apartment_data

router = Router()

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


# Updates apartment fields
def save_apartment(apartment, **fields):
    for key, value in fields.items():
        setattr(apartment, key, value)
# Recalculating embedding
    embedding_text = f"{apartment.total_area}.{apartment.living_area}.{apartment.kitchen_area}.{apartment.description}.{apartment.price}"
    embedding_vector = embedding_model.encode(embedding_text, convert_to_numpy=True).tolist()
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
        embedding_vector,
        apartment.category
    )
    USER_DATA['apartments'] = get_catalog_data()


# Universal functions
async def update_apartment_photo(apartment, message: types.Message, state: FSMContext, photo_field: str):
    file_id = message.photo[-1].file_id
    save_apartment(apartment, **{photo_field: file_id})
    await state.clear()
    await message.answer(f"{photo_field} успешно обновлено!")
    await show_apartment_data(message, edit_mode=True)


async def update_text_field(apartment, message: types.Message, state: FSMContext, field_name: str, field_label: str):
    if message.content_type != types.ContentType.TEXT:
        await message.answer(f"Введите текст для {field_label}.")
        return
    save_apartment(apartment, **{field_name: message.text})
    await state.clear()
    await message.answer(f"{field_label} успешно обновлено!")
    await show_apartment_data(message, edit_mode=True)


# Delete apartment
@router.callback_query(F.data.startswith("delete_"))
async def delete_apartment(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    if apartment:
        # deleting by object ID
        delete_apartment_data(apartment.id)
        # Update the cache to keep the list up to date
        USER_DATA['apartments'] = get_catalog_data()
        USER_DATA['current_apartment'] = None
    await callback_query.answer("Квартира удалена!")
    await callback_query.answer()


# Edit apartment menu
@router.callback_query(F.data.startswith("edit_"))
async def edit_apartment(callback_query: types.CallbackQuery):
    apartment_id = int(callback_query.data.split("_")[-1])
    keyboard = edit_apartment_keyboard(apartment_id)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()


# Update photo1
@router.callback_query(F.data.startswith("update_photo1_"))
async def update_photo1_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.PHOTO1)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Отправьте новое первое фото квартиры:")
    await callback_query.answer()


@router.message(F.photo, EditApartmentState.PHOTO1)
async def handler_update_photo1(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        await update_apartment_photo(apartment, message, state, "photo1")


# Update photo2
@router.callback_query(F.data.startswith("update_photo2_"))
async def update_photo2_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.PHOTO2)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Отправьте новое второе фото квартиры:")
    await callback_query.answer()


@router.message(F.photo, EditApartmentState.PHOTO2)
async def handler_update_photo2(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        await update_apartment_photo(apartment, message, state, "photo2")

# Update photo3
@router.callback_query(F.data.startswith("update_photo3_"))
async def update_photo3_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.PHOTO3)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Отправьте новое третье фото квартиры:")
    await callback_query.answer()


@router.message(F.photo, EditApartmentState.PHOTO3)
async def handler_update_photo3(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        await update_apartment_photo(apartment, message, state, "photo3")


# Update description
@router.callback_query(F.data.startswith("update_description_"))
async def update_description_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.DESCRIPTION)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Введите новое описание квартиры:")
    await callback_query.answer()


@router.message(EditApartmentState.DESCRIPTION)
async def handler_update_description(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        await update_text_field(apartment, message, state, "description", "описание")

# Update address
@router.callback_query(F.data.startswith("update_address_"))
async def update_address_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.ADDRESS)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Введите новый адрес квартиры:")
    await callback_query.answer()


@router.message(EditApartmentState.ADDRESS)
async def handler_update_address(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if apartment:
        await update_text_field(apartment, message, state, "address", "адрес")


# Update total area
@router.callback_query(F.data.startswith("update_total_area_"))
async def update_total_area_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.TOTAL_AREA)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Введите новую общую площадь квартиры (в м²):")
    await callback_query.answer()


@router.message(EditApartmentState.TOTAL_AREA)
async def handler_update_total_area(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if not apartment:
        return
    if message.content_type != types.ContentType.TEXT:
        await message.answer("Введите числовое значение для общей площади.")
        return
    try:
        value = float(message.text)
        if value <= 0:
            await message.answer("Общая площадь должна быть больше 0.")
            return
        save_apartment(apartment, total_area=value)
        await state.clear()
        await message.answer("Общая площадь успешно обновлена!")
        await show_apartment_data(message, edit_mode=True)
    except ValueError:
        await message.answer("Введите корректное числовое значение для общей площади.")


# Update living area
@router.callback_query(F.data.startswith("update_living_area_"))
async def update_living_area_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.LIVING_AREA)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Введите новую жилую площадь квартиры (в м²):")
    await callback_query.answer()


@router.message(EditApartmentState.LIVING_AREA)
async def handler_update_living_area(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if not apartment:
        return
    if message.content_type != types.ContentType.TEXT:
        await message.answer("Введите числовое значение для жилой площади.")
        return
    try:
        value = float(message.text)
        if value <= 0:
            await message.answer("Жилая площадь должна быть больше 0.")
            return
        save_apartment(apartment, living_area=value)
        await state.clear()
        await message.answer("Жилая площадь успешно обновлена!")
        await show_apartment_data(message, edit_mode=True)
    except ValueError:
        await message.answer("Введите корректное числовое значение для жилой площади.")

# Update kitchen area
@router.callback_query(F.data.startswith("update_kitchen_area_"))
async def update_kitchen_area_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.KITCHEN_AREA)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Введите новую площадь кухни (в м²):")
    await callback_query.answer()


@router.message(EditApartmentState.KITCHEN_AREA)
async def handler_update_kitchen_area(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if not apartment:
        return
    if message.content_type != types.ContentType.TEXT:
        await message.answer("Введите числовое значение для площади кухни.")
        return
    try:
        value = float(message.text)
        if value <= 0:
            await message.answer("Площадь кухни должна быть больше 0.")
            return
        save_apartment(apartment, kitchen_area=value)
        await state.clear()
        await message.answer("Площадь кухни успешно обновлена!")
        await show_apartment_data(message, edit_mode=True)
    except ValueError:
        await message.answer("Введите корректное числовое значение для площади кухни.")

# Update price
@router.callback_query(F.data.startswith("update_price_"))
async def update_price_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditApartmentState.PRICE)
    index = int(callback_query.data.split("_")[-1])
    apartment = USER_DATA["apartments"][index]
    USER_DATA["current_apartment"] = apartment
    await callback_query.message.edit_text("Введите новую цену квартиры:")
    await callback_query.answer()


@router.message(EditApartmentState.PRICE)
async def handler_update_price(message: types.Message, state: FSMContext):
    apartment = USER_DATA.get('current_apartment')
    if not apartment:
        return
    if message.content_type != types.ContentType.TEXT:
        await message.answer("Введите числовое значение для цены.")
        return
    try:
        value = int(message.text)
        if value <= 0:
            await message.answer("Цена не может быть равна 0 или быть отрицательной.")
            return
        save_apartment(apartment, price=value)
        await state.clear()
        await message.answer("Цена успешно обновлена!")
        await show_apartment_data(message, edit_mode=True)
    except ValueError:
        await message.answer("Введите корректное целое числовое значение для цены.")
