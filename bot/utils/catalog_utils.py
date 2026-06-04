from aiogram import types
from aiogram.types import FSInputFile
from bot.keyboards.user_keyboard import catalog_navigation_keyboard
from bot.utils.paginator import Paginator


# Render apartment data for catalog
async def show_room_data(message: types.Message, rooms, index=0):
    if not rooms:
        await message.answer("Каталог пуст!")
        return

    paginator = Paginator(rooms, page=index + 1)
    record = paginator.get_page()[0]

    photos_info = [
        types.InputMediaPhoto(
            media=FSInputFile(getattr(record, f'photo{i}').path)
        )
        for i in range(1, 4)
        if getattr(record, f'photo{i}')
    ]
    message_text = (
        f"🏨 <strong>Описание:</strong>\n{record.description}\n\n"
        f"💰 <strong>Цена за ночь:</strong> {record.price} ₽\n\n"
        f"<strong>Номер {paginator.page} из {paginator.pages}</strong>"
    )

    keyboard = catalog_navigation_keyboard(index, len(rooms))

    if photos_info:
        await message.bot.send_media_group(
            message.chat.id,
            media=photos_info
        )

    await message.answer(
        message_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
