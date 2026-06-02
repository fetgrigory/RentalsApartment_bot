from aiogram import types
from bot.keyboards.admin_keyboard import catalog_navigation_edit_keyboard
from bot.keyboards.user_keyboard import catalog_navigation_keyboard
from bot.utils.paginator import Paginator


# Render apartment data for catalog
async def show_room_data(message: types.Message, rooms, index=0, edit_mode=False):
    if not rooms:
        await message.answer("Каталог пуст!")
        return

    paginator = Paginator(rooms, page=index + 1)
    record = paginator.get_page()[0]

    photos_info = [
        types.InputMediaPhoto(
            media=getattr(record, f'photo{i}'),
        )
        for i in range(1, 4)
    ]
    message_text = (
        f"🏨 <strong>Описание:</strong>\n{record.description}\n\n"
        f"💰 <strong>Цена за ночь:</strong> {record.price} ₽\n\n"
        f"<strong>Номер {paginator.page} из {paginator.pages}</strong>"
    )

    keyboard = (
        catalog_navigation_edit_keyboard(index, len(rooms))
        if edit_mode
        else catalog_navigation_keyboard(index, len(rooms))
    )

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
