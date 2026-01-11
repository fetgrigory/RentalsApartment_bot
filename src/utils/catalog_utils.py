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
from src.db.crud import get_catalog_data


# Global dictionary for storing user data
USER_DATA = {}


# Apartment data display function
async def show_apartment_data(message: types.Message, apartments=None, index=0, edit_mode=False):
    if apartments is None:
        apartments = get_catalog_data()
    if not apartments:
        await message.answer("Каталог пуст!")
        return

    record = apartments[0]

    photos_info = [
        types.InputMediaPhoto(media=getattr(record, f'photo{i}'), caption=f"Фото квартиры")
        for i in range(1, 4)
    ]
    # Creating an apartment card for display in the catalog
    message_text = (
        f"🏠 Описание:\n{record.description}\n\n"
        f"📍 Адрес:\n{record.address}\n\n"
        f"📐 Площадь:\n"
        f"  • Общая: {record.total_area} м²\n"
        f"  • Жилая: {record.living_area} м²\n"
        f"  • Кухня: {record.kitchen_area} м²\n\n"
        f"💰 Цена (в сутки): {record.price} ₽"
    )

    # Choose the keyboard depending on the mode
    keyboard = catalog_navigation_edit_keyboard(index, len(apartments)) if edit_mode else catalog_navigation_keyboard(index, len(apartments))

    await message.bot.send_media_group(message.chat.id, media=photos_info)
    await message.answer(message_text, reply_markup=keyboard)
    # Save data to global variable
    USER_DATA['apartments'] = apartments
    USER_DATA['apartment_index'] = index
