from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from src.keyboards.admin_keyboard import admin_category_keyboard
from src.db.crud import get_catalog_data, get_catalog_by_category
from src.utils.catalog_utils import show_apartment_data
from src.utils.paginator import Paginator

router = Router()


# Showing apartment categories
@router.message(F.text == "🛍Каталог")
async def show_catalog_categories(message: types.Message, state: FSMContext):
    await state.clear()

    apartments = get_catalog_data()

    await state.update_data(
        edit_mode=False,
        apartments=apartments,
        page=1
    )

    keyboard = admin_category_keyboard()
    await message.answer("Выберите тип квартиры:", reply_markup=keyboard)


# Showing apartments by selected category
@router.callback_query(F.data.in_(["one-room_apartment", "two-room_apartment", "three-room_apartment", "studio"]))
async def show_apartments_by_category(callback_query: types.CallbackQuery, state: FSMContext):
    category = callback_query.data

    apartments = get_catalog_by_category(category)

    if not apartments:
        await callback_query.answer("Квартиры не найдены в этой категории.")
        return

    await state.update_data(
        apartments=apartments,
        page=1
    )

    paginator = Paginator(apartments, page=1)

    await show_apartment_data(
        callback_query.message,
        apartments=apartments,
        index=paginator.page - 1,
        edit_mode=False
    )


# Navigation: next apartment
@router.callback_query(F.data.in_(["next_view", "next_edit"]))
async def next_apartment(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    apartments = data.get('apartments', [])
    page = data.get('page', 1)

    if not apartments:
        await callback_query.answer()
        return

    paginator = Paginator(apartments, page=page)

    if paginator.has_next():
        page = paginator.page + 1
        await state.update_data(page=page)

    paginator = Paginator(apartments, page=page)

    await show_apartment_data(
        callback_query.message,
        apartments=apartments,
        index=paginator.page - 1,
        edit_mode=data.get('edit_mode', False)
    )


# Navigation: previous apartment
@router.callback_query(F.data.in_(["prev_view", "prev_edit"]))
async def prev_apartment(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    apartments = data.get('apartments', [])
    page = data.get('page', 1)

    if not apartments:
        await callback_query.answer()
        return

    paginator = Paginator(apartments, page=page)

    if paginator.has_previous():
        page = paginator.page - 1
        await state.update_data(page=page)

    paginator = Paginator(apartments, page=page)

    await show_apartment_data(
        callback_query.message,
        apartments=apartments,
        index=paginator.page - 1,
        edit_mode=data.get('edit_mode', False)
    )


# Catalog editing mode
@router.message(F.text == "✏️Редактировать каталог")
async def get_apartment_data_edit_handler(message: types.Message, state: FSMContext):
    await state.update_data(edit_mode=True)
    keyboard = admin_category_keyboard()
    await message.answer("Выберите категорию квартиры для редактирования:", reply_markup=keyboard)
