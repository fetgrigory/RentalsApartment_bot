'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/01/2026
Ending //

'''
# Installing the necessary libraries
from aiogram import F, Router, types
from src.db.crud import get_bookings

router = Router()


# List of bookings
@router.message(F.text == "📜Список бронирований")
async def show_bookings(message: types.Message):
    bookings = await get_bookings()
    if not bookings:
        await message.answer("Бронирования не найдены.")
        return

    bookings_text = "Список бронирований:\n\n"
    for booking in bookings:
        bookings_text += (
            f"ID брони: {booking.id}\n"
            f"Имя: {booking.user.first_name} {booking.user.last_name}\n"
            f"Телефон: {booking.user.phone}\n"
            f"Адрес квартиры: {booking.apartment.address}\n"
            f"Дата начала: {booking.start_date}\n"
            f"Дата окончания: {booking.end_date}\n"
            f"Дней аренды: {booking.rent_days}\n"
            f"Общая стоимость: {booking.total_price} RUB\n\n"
        )

    await message.answer(bookings_text)
