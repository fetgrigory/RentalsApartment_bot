'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2024
Ending //

'''
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import os


def start_keyboard(user_id):
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
            types.KeyboardButton(text="☎️ Контакты")
        )
    return keyboard.as_markup(resize_keyboard=True)


def admin_keyboard():
    # Create a keyboard for a specific administrator with a button to add data and exit administrator mode
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(types.KeyboardButton(text="➕Добавить данные"))
    keyboard.row(types.KeyboardButton(text="✏️Редактировать каталог"))
    keyboard.row(types.KeyboardButton(text="⤴️Назад"))
    return keyboard.as_markup(resize_keyboard=True)


def catalog_navigation_keyboard(index, total_records):
    # Create an InlineKeyboardMarkup for catalog navigation
    keyboard = InlineKeyboardBuilder()
    keyboard.row(types.InlineKeyboardButton(text="Забронировать✅", callback_data="add"))
    # Add a button to go to the previous item if not on the first item
    if index > 0:
        keyboard.row(types.InlineKeyboardButton(text="◀ Пред.", callback_data="prev"))
        # Add a button to go to the next item if not on the last item
    if index < total_records - 1:
        keyboard.row(types.InlineKeyboardButton(text="След. ▶", callback_data="next"))

    return keyboard.as_markup()


def catalog_navigation_edit_keyboard(index, total_records):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_{index}"),
        types.InlineKeyboardButton(text="Изменить", callback_data=f"edit_{index}")
    )
    if index > 0:
        keyboard.row(types.InlineKeyboardButton(text="◀ Пред.", callback_data="prev"))
    if index < total_records - 1:
        keyboard.row(types.InlineKeyboardButton(text="След. ▶", callback_data="next"))

    return keyboard.as_markup()

def edit_apartment_keyboard(index):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        types.InlineKeyboardButton(text='Обновить первое фото', callback_data=f'update_photo1_{index}'),
        types.InlineKeyboardButton(text='Обновить второе фото', callback_data=f'update_photo2_{index}')
    )
    keyboard.row(
        types.InlineKeyboardButton(text='Обновить третье фото', callback_data=f'update_photo3_{index}'),
        types.InlineKeyboardButton(text='Обновить описание', callback_data=f'update_description_{index}')
    )
    keyboard.row(
        types.InlineKeyboardButton(text='Обновить цену', callback_data=f'update_price_{index}')
    )
    return keyboard.as_markup()


def booking_keyboard():
    keyboard = InlineKeyboardBuilder()
    # Create an InlineKeyboardMarkup for booking options
    keyboard.add(
        types.InlineKeyboardButton(text="-1", callback_data="subtract_days"),
        types.InlineKeyboardButton(text="+1", callback_data="add_days")
    )
    # Add buttons to modify the number of days and a payment button
    keyboard.row(types.InlineKeyboardButton(text="💳Оплатить", callback_data="pay"))
    return keyboard.as_markup()
