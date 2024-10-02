'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2024
Ending //

'''
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import os


def start_keyboard(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # Check if the user is an admin by comparing user_id with the ADMIN_ID environment variable
    if user_id == int(os.getenv('ADMIN_ID')):
        # For admins, provide buttons for admin panel and catalog
        keyboard.row("🛠️Админ-панель", "🛍Каталог")
        keyboard.row("🌐 Наш сайт")
        # For regular users, provide buttons for catalog and site, with contacts
    else:
        keyboard.add("🛍Каталог")
        keyboard.row("🌐 Наш сайт", "☎️ Контакты")
    return keyboard


def admin_keyboard():
    """AI is creating summary for admin_keyboard

    Returns:
        [type]: [description]
    """
    # Create an admin-specific keyboard with a button to add data
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("Добавить данные")
    return keyboard


def catalog_navigation_keyboard(index, total_records):
    """AI is creating summary for catalog_navigation_keyboard

    Args:
        index ([type]): [description]
        total_records ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Create an InlineKeyboardMarkup for catalog navigation
    keyboard = InlineKeyboardMarkup()
    # Add a button to book an item
    keyboard.add(InlineKeyboardButton("Забронировать✅", callback_data="add"))
    # Add a button to go to the previous item if not on the first item
    if index > 0:
        keyboard.add(InlineKeyboardButton("◀ Пред.", callback_data="prev"))
    # Add a button to go to the next item if not on the last item
    if index < total_records - 1:
        keyboard.add(InlineKeyboardButton("След. ▶", callback_data="next"))
    return keyboard


def booking_keyboard():
    """AI is creating summary for booking_keyboard

    Returns:
        [type]: [description]
    """
    # Create an InlineKeyboardMarkup for booking options
    keyboard = InlineKeyboardMarkup()
    # Add buttons to modify the number of days and a payment button
    keyboard.add(InlineKeyboardButton("+1", callback_data="add_days"))
    keyboard.add(InlineKeyboardButton("-1", callback_data="subtract_days"))
    keyboard.add(InlineKeyboardButton("💳Оплатить", callback_data="pay"))
    return keyboard
