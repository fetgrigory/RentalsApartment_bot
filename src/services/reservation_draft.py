from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from src.db.crud import add_apartment_to_draft


# Add apartment to draft
async def process_add_apartment_to_draft(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    apartment = data.get('current_apartment')
    rent_days = data.get('rent_days', 1)

    if not apartment:
        return await callback.answer("Ошибка: данные о квартире не найдены.",show_alert=True)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=rent_days)

    add_apartment_to_draft(
        user_telegram_id=callback.from_user.id,
        apartment_id=apartment.id,
        start_date=start_date,
        end_date=end_date
    )
    await callback.answer(f"Квартира добавлена на {rent_days} дн.!", show_alert=False)