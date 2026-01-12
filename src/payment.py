'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2024
Ending //

'''
import os
from aiogram import Bot, types
from aiogram.types import LabeledPrice
from src.db.crud import get_catalog_data


async def send_invoice(bot: Bot, callback_query: types.CallbackQuery, user_data: dict):
    chat_id = callback_query.from_user.id
    # Set the title and description for the invoice
    title = "Аренда квартиры"
    description = "Аренда квартиры"
    invoice_payload = "month_sub"
    provider_token = os.getenv('PAYMENTS_TOKEN')
    current_apartment = user_data.get('current_apartment')
    if not current_apartment:
        await callback_query.answer("Ошибка: данные квартиры не найдены")
        return
    data = get_catalog_data()
    if not data:
        await callback_query.answer("Ошибка: данные каталога не найдены")
        return

    # Calculate the total price based on the number of rental days
    price = current_apartment.price
    currency = "RUB"
    new_price = price * max(user_data.get('rent_days', 1), 1)
    prices = [LabeledPrice(label='Subscription', amount=new_price * 100)]
    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=invoice_payload,
        provider_token=provider_token,
        currency=currency,
        prices=prices
    )


async def handle_successful_payment(bot: Bot, message: types.Message):
    payment_info = message.successful_payment
    # Displaying the payment details in the console
    for k, v in payment_info.__dict__.items():
        print(f"{k} = {v}")
    # Send a confirmation message to the user
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Платеж на сумму {payment_info.total_amount // 100} {payment_info.currency} прошел успешно!"
    )