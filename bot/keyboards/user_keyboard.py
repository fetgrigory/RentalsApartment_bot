from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def start_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text="🛍Каталог"))
    keyboard.row(types.KeyboardButton(text="🎧 Задать вопрос"))
    return keyboard.as_markup(resize_keyboard=True)


# Apartment category selection keyboard
def catalog_categories_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        types.InlineKeyboardButton(text="Стандарт", callback_data="standard"),
        types.InlineKeyboardButton(text="Комфорт", callback_data="comfort")
    )
    keyboard.row(
        types.InlineKeyboardButton(text="Улучшенный", callback_data="superior"),
        types.InlineKeyboardButton(text="Империал", callback_data="imperial")
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
        types.InlineKeyboardButton(text="+1", callback_data="add_days"),
        types.InlineKeyboardButton(text="🛒 Положить в корзину", callback_data="add_to_draft"),
        types.InlineKeyboardButton(text="🗑 Очистить корзину", callback_data="clear_draft"),
        types.InlineKeyboardButton(text="🔙 Продолжить выбор", callback_data="back_to_catalog"),
        types.InlineKeyboardButton(text="💳 Оплатить", callback_data="pay")
    )

    keyboard.adjust(2, 1, 2, 1)

    return keyboard.as_markup()
