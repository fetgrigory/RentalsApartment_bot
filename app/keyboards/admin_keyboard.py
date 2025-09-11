'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 11/09/2025
Ending //

'''
# Installing the necessary libraries
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Create a keyboard for a specific administrator with a button to add data and exit administrator mode
def admin_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(types.KeyboardButton(text="➕Добавить данные"))
    keyboard.row(types.KeyboardButton(text="✏️Редактировать каталог"))
    keyboard.row(types.KeyboardButton(text="📜Список бронирований"))
    keyboard.row(types.KeyboardButton(text="📝Просмотр отзывов"))
    keyboard.row(types.KeyboardButton(text="⤴️Назад"))
    return keyboard.as_markup(resize_keyboard=True)


# Keyboard for navigation and editing of the catalog
def catalog_navigation_edit_keyboard(index, total_records):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_{index}"),
        types.InlineKeyboardButton(text="Изменить", callback_data=f"edit_{index}")
    )
    if index > 0:
        keyboard.row(types.InlineKeyboardButton(text="◀ Пред.", callback_data="prev_edit"))
    if index < total_records - 1:
        keyboard.row(types.InlineKeyboardButton(text="След. ▶", callback_data="next_edit"))

    return keyboard.as_markup()


# Keyboard for editing apartment parameters
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
    keyboard.row(
        types.InlineKeyboardButton(text='Обновить адрес', callback_data=f'update_address_{index}')
    )
    return keyboard.as_markup()
