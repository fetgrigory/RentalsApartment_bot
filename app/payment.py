'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2024
Ending //

'''
import os
from aiogram import types
from app.database import get_catalog_data


async def send_invoice(bot, callback_query, user_data):
    """AI is creating summary for send_invoice

    Args:
        bot ([type]): [description]
        callback_query ([type]): [description]
        user_data ([type]): [description]
    """
    chat_id = callback_query.from_user.id
    # Set the title and description for the invoice
    title = "Аренда квартиры"
    description = "Аренда квартиры"
    invoice_payload = "month_sub"
    # Retrieve the payment provider token from environment variables
    provider_token = os.getenv('PAYMENTS_TOKEN')
    # Get the apartment index from user data
    index = user_data['apartment_index']
    # Retrieve catalog data and get the price for the selected apartment
    data = get_catalog_data()
    # Price is located at the 7th position (index 6) in the data list
    price = int(data[index][6])
    # Set the currency for the invoice
    currency = "RUB"
    # Calculate the total price based on the number of days the apartment is rented
    new_price = price * max(user_data.get('rent_days', 1), 1)
    # Create a labeled price for the invoice
    prices = [types.LabeledPrice(label='Subscription', amount=new_price * 100)]
    # Send the invoice to the user
    await bot.send_invoice(chat_id, title, description, invoice_payload, provider_token, currency, prices)


async def handle_successful_payment(bot, message):
    """AI is creating summary for handle_successful_payment

    Args:
        bot ([type]): [description]
        message ([type]): [description]
    """
    # Convert successful payment information to a Python dictionary
    payment_info = message.successful_payment.to_python()
    # Print all payment information for debugging purposes
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    # Notify the user about the successful payment
    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")