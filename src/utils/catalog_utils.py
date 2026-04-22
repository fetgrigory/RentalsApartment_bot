from aiogram import types
from src.keyboards.admin_keyboard import catalog_navigation_edit_keyboard
from src.keyboards.user_keyboard import catalog_navigation_keyboard
from src.utils.paginator import Paginator


# Render apartment data for catalog
async def show_apartment_data(message: types.Message, apartments, index=0, edit_mode=False):
    if not apartments:
        await message.answer("Каталог пуст!")
        return

    paginator = Paginator(apartments, page=index + 1)
    record = paginator.get_page()[0]

    photos_info = [
        types.InputMediaPhoto(
            media=getattr(record, f'photo{i}'),
            caption=f"Фото квартиры"
        )
        for i in range(1, 4)
    ]
    message_text = (
        f"🏠 Описание:\n{record.description}\n\n"
        f"📍 Адрес:\n{record.address}\n\n"
        f"📐 Площадь:\n"
        f"  • Общая: {record.total_area} м²\n"
        f"  • Жилая: {record.living_area} м²\n"
        f"  • Кухня: {record.kitchen_area} м²\n\n"
        f"💰 Цена (в сутки): {record.price} ₽ \n\n"
        f"{paginator.page} из {paginator.pages}"
    )

    keyboard = (
        catalog_navigation_edit_keyboard(index, len(apartments))
        if edit_mode
        else catalog_navigation_keyboard(index, len(apartments))
    )

    await message.bot.send_media_group(message.chat.id, media=photos_info)
    await message.answer(message_text, reply_markup=keyboard)
