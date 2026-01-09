'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/01/2026
Ending //

'''
# Installing the necessary libraries
from aiogram import F, Router, types
from src.database.PostgreSQL_db import get_bookings

router = Router()


@router.message(F.text == "📜Список бронирований")
async def show_bookings(message: types.Message):
    bookings = get_bookings()
    if not bookings:
        await message.answer("Бронирования не найдены.")
        return
    bookings_text = "Список бронирований:\n\n"
    for booking in bookings:
        bookings_text += (
            f"ID брони: {booking[0]}\n"
            f"Имя: {booking[1]} {booking[2]}\n"
            f"Телефон: {booking[8]}\n"
            f"Адрес квартиры: {booking[3]}\n"
            f"Дата начала: {booking[4]}\n"
            f"Дата окончания: {booking[5]}\n"
            f"Дней аренды: {booking[6]}\n"
            f"Общая стоимость: {booking[7]} RUB\n\n"
        )
    await message.answer(bookings_text)
