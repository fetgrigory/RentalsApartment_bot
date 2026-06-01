from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from bot.db.crud import add_apartment_to_draft, is_apartment_available


# Add apartment to draft
async def process_add_apartment_to_draft(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    apartment = data.get('current_apartment')
    rent_days = data.get('rent_days', 1)

    if not apartment:
        return await callback.answer("Ошибка: данные о квартире не найдены.", show_alert=True)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=rent_days)

    # Check if the apartment is available for the selected dates
    if not is_apartment_available(apartment.id, start_date, end_date):
        return await callback.answer(
            "❌ Квартира уже забронирована на выбранные даты!\n"
            "Пожалуйста, выберите другие даты или другую квартиру.",
            show_alert=True
        )

    add_apartment_to_draft(
        user_telegram_id=callback.from_user.id,
        apartment_id=apartment.id,
        start_date=start_date,
        end_date=end_date
    )

    await callback.answer(
        f"✅ Квартира добавлена в черновик!\n"
        f"📅 {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}\n"
        f"⏱️ {rent_days} дн.\n\n"
        f"Просмотреть черновик можно по кнопке '🛒 Корзина' в главном меню.",
        show_alert=False
    )