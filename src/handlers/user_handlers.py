'''
This bot make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 18/09/2025
Ending //
'''

import datetime
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from src.states import BookingState, ReviewState, QuestionState
from src.db.crud import is_apartment_available, check_user_exists, insert_user_data, insert_booking_data, insert_review
from src.keyboards.user_keyboard import start_keyboard, booking_keyboard
from src.payment import send_invoice
from src.nlp.llm_client import ask_gpt
from src.utils.catalog_utils import USER_DATA

router = Router()


@router.message(F.command("start"))
async def start(message: types.Message):
    USER_DATA.clear()
    keyboard = start_keyboard(message.from_user.id)
    me = await message.bot.get_me()
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!\n"
                         f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
                         parse_mode='html', reply_markup=keyboard)


#  Inform user about website availability
@router.message(F.text == '🌐 Наш сайт')
async def website(message: types.Message):
    await message.answer('Сожалею, но у нас пока нет сайта')


# Provide contact information
@router.message(F.text == '☎️ Контакты')
async def contact(message: types.Message):
    await message.answer('Наш телефон: 8-901-133-00-00')


# Navigate to the next or previous apartment details
@router.callback_query(F.data == "add")
async def add_button(callback_query: types.CallbackQuery, state: FSMContext):
    apartments = USER_DATA.get('apartments')
    if apartments:
        apartment = apartments[0]
        USER_DATA['current_apartment'] = apartment
        user_id = callback_query.from_user.id
        start_date = datetime.datetime.now().date()
        rent_days = USER_DATA.get('rent_days', 1)
        end_date = start_date + datetime.timedelta(days=rent_days)
        # Check if the apartment is available
        if is_apartment_available(apartment.id, start_date, end_date):
            # Check if there is a user in the database
            if check_user_exists(user_id):
                # If the user is already registered, proceed to booking
                keyboard = booking_keyboard()
                await callback_query.message.edit_reply_markup(reply_markup=keyboard)
            else:
                # If the user is not registered, request data
                await state.set_state(BookingState.FIRST_NAME)
                await callback_query.message.answer("👤Для бронирования квартиры потребуется небольшая регистрация. Это займет всего пару минут!\n Эти данные мы не передаем третьим лицам и нигде не публикуем кроме внутренних ресурсов.")
                await callback_query.message.answer("Шаг 1 из 3. 🟩⬜️⬜️")
                await callback_query.message.answer("Введите ваше имя:")
        else:
            # Notify the user that the apartment is already booked
            await callback_query.answer("К сожалению, квартира уже забронирована. Пожалуйста, выберите другую квартиру.")
    else:
        await callback_query.answer("Ошибка: данные о квартире не найдены.")


# FSM: process first name input
@router.message(BookingState.FIRST_NAME)
async def process_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(BookingState.LAST_NAME)
    await message.answer("Шаг 2 из 3. 🟩🟩⬜️")
    await message.answer("Введите вашу фамилию:")


# FSM: process last name input
@router.message(BookingState.LAST_NAME)
async def process_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(BookingState.PHONE)
    await message.answer("Шаг 3 из 3. 🟩🟩🟩")
    await message.answer("Введите ваш номер телефона:")


# FSM: process phone number input
@router.message(BookingState.PHONE)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    user_data = await state.get_data()
    user_id = message.from_user.id

    # Adding the user to the database
    insert_user_data(user_id, user_data['first_name'], user_data['last_name'], user_data['phone'])
    await state.clear()
    await message.answer("Данные сохранены! Теперь вы можете использовать их для будущих бронирований. Продолжайте бронирование.")
    # Getting information about the current apartment and calculating total price
    apartment = USER_DATA['current_apartment']
    rent_days = USER_DATA.get('rent_days', 1)
    total_price = apartment.price * rent_days
    text = f"Количество дней аренды: {rent_days}\nОбщая сумма к оплате: {total_price} RUB"
    keyboard = booking_keyboard()
    await message.answer(text, reply_markup=keyboard)


# Increase the rental period and calculate the total price
@router.callback_query(F.data == "add_days")
async def add_days(callback_query: types.CallbackQuery):
    apartment = USER_DATA['current_apartment']
    USER_DATA['rent_days'] = USER_DATA.get('rent_days', 1) + 1
    new_price = apartment.price * USER_DATA['rent_days']
    text = f"Количество дней аренды: {USER_DATA['rent_days']}\nОбщая сумма к оплате: {new_price} RUB"
    keyboard = booking_keyboard()
    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


# Decrease the rental period and calculate the total price
@router.callback_query(F.data == "subtract_days")
async def subtract_days(callback_query: types.CallbackQuery):
    apartment = USER_DATA['current_apartment']
    USER_DATA['rent_days'] = max(USER_DATA.get('rent_days', 1) - 1, 1)
    new_price = apartment.price * USER_DATA['rent_days']
    text = f"Количество дней аренды: {USER_DATA['rent_days']}\nОбщая сумма к оплате: {new_price} RUB"
    keyboard = booking_keyboard()
    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


# Update the payment handler to use the current apartment
@router.callback_query(F.data == "pay")
async def pay_for_apartment(callback_query: types.CallbackQuery):
    await send_invoice(callback_query.bot, callback_query, USER_DATA)


# Confirm pre-checkout queries
@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await pre_checkout_q.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# Handle successful payment confirmation
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await handle_successful_payment(message.bot, message)


# Handle successful payment
async def handle_successful_payment(bot, message):
    user_id = message.from_user.id
    apartment = USER_DATA['current_apartment']
    start_date = datetime.datetime.now().date()
    rent_days = USER_DATA.get('rent_days', 1)
    total_price = apartment.price * rent_days
    insert_booking_data(user_id, apartment.id, start_date, rent_days, total_price)
    await bot.send_message(user_id, "Оплата прошла успешно! Ваше бронирование подтверждено.")


# Add apartment review
@router.callback_query(F.data == "add_review")
async def request_review(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(ReviewState.TEXT)
    await callback_query.message.answer("Пожалуйста, введите ваш отзыв:")


# Save review and analyze sentiment
@router.message(ReviewState.TEXT)
async def save_review(message: types.Message, state: FSMContext):
    apartment = USER_DATA['current_apartment']
    user_id = message.from_user.id
    insert_review(user_id, apartment.id, message.text)
    await message.answer("Спасибо за ваш отзыв!")
    await state.clear()


# User support: question input handler
@router.message(F.text == "🎧 Задать вопрос")
async def ask_question_handler(message: types.Message, state: FSMContext):
    await state.set_state(QuestionState.WAITING_QUESTION)
    await message.answer("Пожалуйста, задайте ваш вопрос по аренде жилья. Я постараюсь помочь!")


# Handles user's question, saves message history, and returns GPT's response
@router.message(QuestionState.WAITING_QUESTION)
async def handle_question(message: types.Message):
    user_id = message.from_user.id
    # Initialize message history if the user is new
    USER_DATA.setdefault(user_id, {'messages': []})
    # Save user's question
    USER_DATA[user_id]['messages'].append({"role": "user", "content": message.text})
    user_query = message.text
    thinking_msg = await message.answer("Думаю над ответом...")
    try:
        # Get GPT's response, remove the indicator, and send the response
        response = ask_gpt(USER_DATA[user_id]['messages'], user_query)
        await message.bot.delete_message(chat_id=message.chat.id, message_id=thinking_msg.message_id)
        USER_DATA[user_id]['messages'].append({"role": "assistant", "content": response})
        await message.answer(response)
    except Exception as e:
        print(f"Error (User {user_id}): {e}")
        await message.answer("Произошла ошибка при обработке вашего вопроса. Пожалуйста, попробуйте позже.")
