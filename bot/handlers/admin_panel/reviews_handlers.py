'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/01/2026
Ending //

'''
# Installing the necessary libraries
from aiogram import F, Router, types
from bot.db.crud import get_reviews

router = Router()


# Viewing reviews
@router.message(F.text == "📝Просмотр отзывов")
async def show_reviews(message: types.Message):
    reviews = get_reviews()
    if not reviews:
        await message.answer("Отзывы не найдены.")
        return
    reviews_text = "Список отзывов:\n\n"
    for review in reviews:
        reviews_text += (
            f"ID отзыва: {review.id}\n"
            f"ID квартиры: {review.apartment_id}\n"
            f"Текст отзыва: {review.review_text}\n"
            f"Оценка: {review.sentiment_label} ({review.sentiment_score})\n"
            f"Дата: {review.date}\n\n"
        )

    await message.answer(reviews_text)
