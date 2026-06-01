'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/01/2026
Ending //

'''
# Installing the necessary libraries
from aiogram import F, Router, types
from bot.db.crud import get_bookings

router = Router()


# List of bookings
@router.message(F.text == "📜Список бронирований")
async def show_bookings(message: types.Message):
    bookings = get_bookings()
    if not bookings:
        await message.answer("Бронирования не найдены.")
        return

    bookings_text = "Список бронирований:\n\n"
    for booking in bookings:
        bookings_text += (
            f"📋 Бронирование #{booking.id}\n\n"
            f"👤 Гость: {booking.user.first_name} {booking.user.last_name}\n"
            f"📞 Телефон: {booking.user.phone}\n\n"
            f"🏠 Апартаменты: {booking.apartment.address}\n"
            f"💰 Стоимость апартаментов: {booking.apartment.price} руб./сутки\n\n"
            f"📅 Заезд: {booking.start_date}\n"
            f"📅 Выезд: {booking.end_date}\n"
            f"⏳ Дней: {booking.rent_days}\n"
            f"💳 Итого: {booking.total_price} руб.\n"
        )

    await message.answer(bookings_text)
