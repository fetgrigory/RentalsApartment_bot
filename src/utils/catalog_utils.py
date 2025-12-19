'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 19/09/2025
Ending //
'''
# Installing the necessary libraries
from aiogram import types
from src.keyboards.admin_keyboard import catalog_navigation_edit_keyboard
from src.keyboards.user_keyboard import catalog_navigation_keyboard
from src.database.PostgreSQL_db import get_catalog_data


# Global dictionary for storing user data
USER_DATA = {}


# Apartment data display function
async def show_apartment_data(message: types.Message, apartments=None, index=0, edit_mode=False):
    if apartments is None:
        apartments = get_catalog_data()
    if not apartments:
        await message.answer("Каталог пуст!")
        return

    record = apartments[index]

    photos_info = [
        types.InputMediaPhoto(media=record[i], caption=f"Фото квартиры")
        for i in range(2, 5)  # Photos from index 2 to 4
    ]

    description = record[5]
    address = record[6]
    price = record[7]

    message_text = f"Описание квартиры: {description}\nАдрес: {address}\nЦена (в сутки): {price}"

    # Choose the keyboard depending on the mode
    keyboard = catalog_navigation_edit_keyboard(index, len(apartments)) if edit_mode else catalog_navigation_keyboard(index, len(apartments))

    await message.bot.send_media_group(message.chat.id, media=photos_info)
    await message.answer(message_text, reply_markup=keyboard)
    # Save data to global variable
    USER_DATA['apartments'] = apartments
    USER_DATA['apartment_index'] = index
