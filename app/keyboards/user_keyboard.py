'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2024
Ending //

'''
import os
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def start_keyboard(user_id):
    # Check if the user is an admin by comparing user_id with the ADMIN_ID environment variable
    keyboard = ReplyKeyboardBuilder()
    if user_id == int(os.getenv('ADMIN_ID')):
        # For admins, provide buttons for admin panel and catalog
        keyboard.add(types.KeyboardButton(text="🛠️Админ-панель"),
                     types.KeyboardButton(text="🛍Каталог"),)
        keyboard.row(
            types.KeyboardButton(text="🌐 Наш сайт")
        )
        # For regular users, provide buttons for catalog and site, with contacts
    else:
        keyboard.add(types.KeyboardButton(text="🛍Каталог"))
        keyboard.row(
            types.KeyboardButton(text="🌐 Наш сайт"),
            types.KeyboardButton(text="☎️ Контакты"),
            types.KeyboardButton(text="🎧 Задать вопрос")
        )
    return keyboard.as_markup(resize_keyboard=True)


# Apartment category selection keyboard
async def catalog_categories_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        types.InlineKeyboardButton(text="Однокомнатная", callback_data="one-room_apartment"),
        types.InlineKeyboardButton(text="Двухкомнатная", callback_data="two-room_apartment")
    )
    keyboard.row(
        types.InlineKeyboardButton(text="Трехкомнатная", callback_data="three-room_apartment"),
        types.InlineKeyboardButton(text="Студия", callback_data="studio")
    )
    return keyboard.as_markup()


# Create an InlineKeyboardMarkup for catalog navigation
def catalog_navigation_keyboard(index, total_records):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(types.InlineKeyboardButton(text="Забронировать ✅", callback_data="add"))
    keyboard.row(types.InlineKeyboardButton(text="Оставить отзыв ⭐", callback_data="add_review"))
    # Add a button to go to the previous item if not on the first item
    if index > 0:
        keyboard.row(types.InlineKeyboardButton(text="◀ Пред.", callback_data="prev_view"))
        # Add a button to go to the next item if not on the last item
    if index < total_records - 1:
        keyboard.row(types.InlineKeyboardButton(text="След. ▶", callback_data="next_view"))

    return keyboard.as_markup()


# Create an InlineKeyboardMarkup for booking options
def booking_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(text="-1", callback_data="subtract_days"),
        types.InlineKeyboardButton(text="+1", callback_data="add_days")
    )
    # Add buttons to modify the number of days and a payment button
    keyboard.row(types.InlineKeyboardButton(text="💳Оплатить", callback_data="pay"))
    return keyboard.as_markup()
