'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2024
Ending //

'''
import os
from aiogram import Bot, types
from aiogram.types import LabeledPrice
from app.database.sqlite3_db import get_catalog_data
# from app.database.PostgreSQL_db import get_catalog_data


async def send_invoice(bot: Bot, callback_query: types.CallbackQuery, user_data: dict):
    chat_id = callback_query.from_user.id
    # Set the title and description for the invoice
    title = "Аренда квартиры"
    description = "Аренда квартиры"
    invoice_payload = "month_sub"
    # Retrieve the payment provider token from environment variables
    provider_token = os.getenv('PAYMENTS_TOKEN')
    # Get the current apartment data directly from user_data
    current_apartment = user_data.get('current_apartment')
    if not current_apartment:
        await callback_query.answer("Ошибка: данные квартиры не найдены")
        return
    # Retrieve catalog data and get the price for the selected apartment
    data = get_catalog_data()
    if not data:
        await callback_query.answer("Ошибка: данные каталога не найдены")
        return

    # Price is located at the 8th position (index 7) in the data list
    price = int(current_apartment[7])
    # Set the currency for the invoice
    currency = "RUB"
    # Calculate the total price based on the number of days the apartment is rented
    new_price = price * max(user_data.get('rent_days', 1), 1)
    # Create a labeled price for the invoice
    prices = [LabeledPrice(label='Subscription', amount=new_price * 100)]
    # This function sends an invoice to the user
    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=invoice_payload,
        provider_token=provider_token,
        currency=currency,
        prices=prices
    )


# This function handles successful payment notification.
async def handle_successful_payment(bot: Bot, message: types.Message):
    payment_info = message.successful_payment
    # Print each attribute of the successful payment information
    for k, v in payment_info.__dict__.items():
        print(f"{k} = {v}")
    # Send a confirmation message to the user
    await bot.send_message(
        chat_id=message.chat.id,
        # Inform the user of the successful payment
        text=f"Платеж на сумму {payment_info.total_amount // 100} {payment_info.currency} прошел успешно!"
    )
