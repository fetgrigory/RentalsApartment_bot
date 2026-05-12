from aiogram import types
from datetime import datetime
from src.db.crud import add_apartment_to_draft


async def process_add_apartment_to_draft(call: types.CallbackQuery):
    user_id = call.from_user.id
    apartment_id = 1
    add_apartment_to_draft(
        user_telegram_id=user_id,
        apartment_id=apartment_id,
        start_date=datetime.now(),
        end_date=datetime.now()
    )
    await call.answer("Квартира добавлена в корзину!", show_alert=False)
