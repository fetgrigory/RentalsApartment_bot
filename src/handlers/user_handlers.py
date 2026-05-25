from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from src.states import BookingState, ReviewState, QuestionState
from src.services.reservation_draft import process_add_apartment_to_draft
from src.db.crud import is_apartment_available, check_user_exists, insert_user_data, insert_booking_data, insert_review, get_user_reservation_draft, delete_reservation_draft
from src.keyboards.user_keyboard import start_keyboard, booking_keyboard, catalog_categories_keyboard
from src.payment import send_invoice
from src.services.booking_service import calculate_days, calculate_price, get_dates
from src.services.ai_service import process_question

router = Router()


@router.message(F.command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.update_data(apartments=None, rent_days=1, messages=[])
    keyboard = start_keyboard(message.from_user.id)
    me = await message.bot.get_me()
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!\n"
                         f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
                         parse_mode='html', reply_markup=keyboard)


# Add to draft action
@router.callback_query(F.data == "add_to_draft")
async def add_to_draft_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await process_add_apartment_to_draft(callback_query, state)


# Start booking process
@router.callback_query(F.data == "add")
async def add_button(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    apartments = data.get('apartments')
    if apartments:
        apartment = apartments[0]
        await state.update_data(current_apartment=apartment)
        user_id = callback_query.from_user.id
        rent_days = data.get('rent_days', 1)
        start_date, end_date = get_dates(rent_days)
        if is_apartment_available(apartment.id, start_date, end_date):
            if check_user_exists(user_id):
                keyboard = booking_keyboard()
                await callback_query.message.edit_reply_markup(reply_markup=keyboard)
            else:
                # If the user is not registered, request data
                await state.set_state(BookingState.FIRST_NAME)
                await callback_query.message.answer("👤Для бронирования квартиры потребуется небольшая регистрация. Это займет всего пару минут!\n Эти данные мы не передаем третьим лицам и нигде не публикуем кроме внутренних ресурсов.")
                await callback_query.message.answer("Шаг 1 из 3. 🟩⬜️⬜️")
                await callback_query.message.answer("Введите ваше имя:")
        else:
            await callback_query.answer("К сожалению, квартира уже забронирована. Пожалуйста, выберите другую квартиру.")
    else:
        await callback_query.answer("Ошибка: данные о квартире не найдены.")


# Get username
@router.message(BookingState.FIRST_NAME)
async def process_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(BookingState.LAST_NAME)
    await message.answer("Шаг 2 из 3. 🟩🟩⬜️")
    await message.answer("Введите вашу фамилию:")


# Get user last name
@router.message(BookingState.LAST_NAME)
async def process_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(BookingState.PHONE)
    await message.answer("Шаг 3 из 3. 🟩🟩🟩")
    await message.answer("Введите ваш номер телефона:")


# Get user phone number
@router.message(BookingState.PHONE)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    user_data = await state.get_data()
    user_id = message.from_user.id

    insert_user_data(user_id, user_data['first_name'], user_data['last_name'], user_data['phone'])
    await state.clear()
    await message.answer("Данные сохранены! Теперь вы можете использовать их для будущих бронирований. Продолжайте бронирование.")
    apartment = user_data['current_apartment']
    rent_days = user_data.get('rent_days', 1)
    total_price = calculate_price(apartment.price, rent_days)
    text = f"Количество дней аренды: {rent_days}\nОбщая сумма к оплате: {total_price} RUB"
    keyboard = booking_keyboard()
    await message.answer(text, reply_markup=keyboard)


# Increase the rental period and calculate the total price
@router.callback_query(F.data == "add_days")
async def add_days(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    apartment = data['current_apartment']

    rent_days = calculate_days(data.get('rent_days', 1), 1)
    await state.update_data(rent_days=rent_days)

    new_price = calculate_price(apartment.price, rent_days)

    text = f"Количество дней аренды: {rent_days}\nОбщая сумма к оплате: {new_price} RUB"
    keyboard = booking_keyboard()

    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


# Decrease the rental period and calculate the total price
@router.callback_query(F.data == "subtract_days")
async def subtract_days(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    apartment = data['current_apartment']

    rent_days = calculate_days(data.get('rent_days', 1), -1)
    await state.update_data(rent_days=rent_days)

    new_price = calculate_price(apartment.price, rent_days)

    text = f"Количество дней аренды: {rent_days}\nОбщая сумма к оплате: {new_price} RUB"
    keyboard = booking_keyboard()

    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


# Payment processing
@router.callback_query(F.data == "pay")
async def pay_for_apartment(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await send_invoice(callback_query.bot, callback_query, data)


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await pre_checkout_q.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, state: FSMContext):
    await handler_successful_payment(message.bot, message, state)


async def handler_successful_payment(bot, message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    apartment = data['current_apartment']
    rent_days = data.get('rent_days', 1)
    start_date, _ = get_dates(rent_days)
    total_price = calculate_price(apartment.price, rent_days)

    insert_booking_data(user_id, apartment.id, start_date, rent_days, total_price)

    await bot.send_message(user_id, "Оплата прошла успешно! Ваше бронирование подтверждено.")


# User review input
@router.callback_query(F.data == "add_review")
async def request_review(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(ReviewState.TEXT)
    await callback_query.message.answer("Пожалуйста, введите ваш отзыв:")


@router.message(ReviewState.TEXT)
async def save_review(message: types.Message, state: FSMContext):
    data = await state.get_data()
    apartment = data['current_apartment']

    user_id = message.from_user.id
    insert_review(user_id, apartment.id, message.text)

    await message.answer("Спасибо за ваш отзыв!")
    await state.clear()


# AI support chat
@router.message(F.text == "🎧 Задать вопрос")
async def ask_question_handler(message: types.Message, state: FSMContext):
    await state.set_state(QuestionState.WAITING_QUESTION)
    await state.update_data(messages=[])
    await message.answer("Пожалуйста, задайте ваш вопрос. Я помогу с правилами проживания, каталогом квартир и бронированием через сервис.")


@router.message(QuestionState.WAITING_QUESTION)
async def handler_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    messages = data.get('messages', [])
    user_id = message.from_user.id
    thinking_msg = await message.answer("Думаю над ответом...")
    try:
        response, updated_messages = process_question(message.text, messages)
        await message.bot.delete_message(chat_id=message.chat.id, message_id=thinking_msg.message_id)
        await state.update_data(messages=updated_messages)
        await message.answer(response)
    except Exception as e:
        print(f"Error (User {user_id}): {e}")
        await message.answer("Произошла ошибка при обработке вашего вопроса. Пожалуйста, попробуйте позже.")


# Reservation draft
@router.message(F.text == "🛒 Корзина")
async def show_booking_draft(message: types.Message):
    draft = get_user_reservation_draft(message.from_user.id)
    if not draft or not draft.apartment:
        await message.answer("🛒 Ваша корзина пуста", reply_markup=start_keyboard(message.from_user.id))
        return
    days = (draft.end_date - draft.start_date).days
    total_price = calculate_price(draft.apartment.price, days)
    text = (
        f"🛒 **Ваш черновик бронирования:**\n\n"
        f"🏠 {draft.apartment.address}\n"
        f"📅 Заезд: {draft.start_date.strftime('%d.%m.%Y')}\n"
        f"🏁 Выезд: {draft.end_date.strftime('%d.%m.%Y')}\n"
        f"⏱️ {days} дней\n"
        f"💰 {total_price} ₽"
    )

    keyboard = booking_keyboard()
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "clear_draft")
async def clear_draft(callback: types.CallbackQuery):
    delete_reservation_draft(callback.from_user.id)
    await callback.message.edit_text("🧹 Корзина очищена")
    await callback.answer()


@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите категорию квартир:",reply_markup=catalog_categories_keyboard())
    await callback.answer()
