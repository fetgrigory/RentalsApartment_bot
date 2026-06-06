from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from apps.rooms.selectors import (
    get_catalog_data,
    get_catalog_by_category)
from bot.keyboards.user_keyboard import catalog_categories_keyboard
from bot.utils.catalog_utils import show_room_data
from bot.utils.paginator import Paginator

router = Router()


# Showing apartment categories
@router.message(F.text == "🛍Каталог")
async def show_catalog_categories(message: types.Message, state: FSMContext):
    await state.clear()
    rooms = await get_catalog_data()
    await state.update_data(
        rooms=rooms,
        page=1
    )

    await message.answer(
        "Выберите тип квартиры:",
        reply_markup=catalog_categories_keyboard()
    )


# Showing rooms by selected category
@router.callback_query(F.data.in_(["standard", "comfort", "superior", "imperial"]))
async def show_rooms_by_category(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data
    rooms = await get_catalog_by_category(category)

    if not rooms:
        await callback.answer("Квартиры не найдены в этой категории.", show_alert=True)
        return

    await state.update_data(rooms=rooms, page=1)
    data = await state.get_data()
    await show_room_data(
        callback.message,
        rooms=rooms,
        index=0
    )
    await callback.answer()


# Navigation: next apartment
@router.callback_query(F.data.startswith("next_"))
async def next_apartment(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    rooms = data.get('rooms', [])
    page = data.get('page', 1)

    if not rooms:
        return await callback.answer()

    paginator = Paginator(rooms, page=page)
    if paginator.has_next():
        page += 1
        await state.update_data(page=page)

    await show_room_data(
        callback.message,
        rooms=rooms,
        index=page - 1
    )
    await callback.answer()


# Navigation: previous apartment
@router.callback_query(F.data.startswith("prev_"))
async def prev_apartment(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    rooms = data.get('rooms', [])
    page = data.get('page', 1)

    if not rooms:
        return await callback.answer()

    paginator = Paginator(rooms, page=page)
    if paginator.has_previous():
        page -= 1
        await state.update_data(page=page)

    await show_room_data(
        callback.message,
        rooms=rooms,
        index=page - 1
    )
    await callback.answer()
