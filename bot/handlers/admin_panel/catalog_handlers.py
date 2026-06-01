from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from bot.keyboards.admin_keyboard import admin_category_keyboard
from bot.db.crud import get_catalog_data, get_catalog_by_category
from bot.utils.catalog_utils import show_apartment_data
from bot.utils.paginator import Paginator

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

    await message.answer(
        "Выберите тип квартиры:",
        reply_markup=admin_category_keyboard()
    )


# Showing apartments by selected category
@router.callback_query(F.data.in_(["one-room_apartment", "two-room_apartment", "three-room_apartment", "studio"]))
async def show_apartments_by_category(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data
    apartments = get_catalog_by_category(category)

    if not apartments:
        await callback.answer("Квартиры не найдены в этой категории.", show_alert=True)
        return

    await state.update_data(apartments=apartments, page=1)
    data = await state.get_data()
    await show_apartment_data(
        callback.message,
        apartments=apartments,
        index=0,
        edit_mode=data.get('edit_mode', False)
    )
    await callback.answer()


# Navigation: next apartment
@router.callback_query(F.data.startswith("next_"))
async def next_apartment(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    apartments = data.get('apartments', [])
    page = data.get('page', 1)

    if not apartments:
        return await callback.answer()

    is_edit = callback.data == "next_edit"
    paginator = Paginator(apartments, page=page)
    if paginator.has_next():
        page += 1
        await state.update_data(page=page, edit_mode=is_edit)

    await show_apartment_data(
        callback.message,
        apartments=apartments,
        index=page - 1,
        edit_mode=is_edit
    )
    await callback.answer()


# Navigation: previous apartment
@router.callback_query(F.data.startswith("prev_"))
async def prev_apartment(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    apartments = data.get('apartments', [])
    page = data.get('page', 1)

    if not apartments:
        return await callback.answer()

    is_edit = callback.data == "prev_edit"
    paginator = Paginator(apartments, page=page)
    if paginator.has_previous():
        page -= 1
        await state.update_data(page=page, edit_mode=is_edit)

    await show_apartment_data(
        callback.message,
        apartments=apartments,
        index=page - 1,
        edit_mode=is_edit
    )
    await callback.answer()


# Catalog editing mode
@router.message(F.text == "✏️Редактировать каталог")
async def get_apartment_data_edit_handler(message: types.Message, state: FSMContext):
    # Enable edit mode for subsequent navigation
    await state.update_data(edit_mode=True)
    keyboard = admin_category_keyboard()
    await message.answer("Выберите категорию квартиры для редактирования:", reply_markup=keyboard)
