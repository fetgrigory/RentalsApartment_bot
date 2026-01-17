'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 15/09/2025
Ending //
'''
from aiogram.fsm.state import StatesGroup, State


# States group
class AddApartmentState(StatesGroup):
    PHOTO1 = State()
    PHOTO2 = State()
    PHOTO3 = State()
    TOTAL_AREA = State()
    LIVING_AREA = State()
    KITCHEN_AREA = State()
    DESCRIPTION = State()
    ADDRESS = State()
    PRICE = State()
    CATEGORY = State()


class EditApartmentState(StatesGroup):
    PHOTO1 = State()
    PHOTO2 = State()
    PHOTO3 = State()
    TOTAL_AREA = State()
    LIVING_AREA = State()
    KITCHEN_AREA = State()
    DESCRIPTION = State()
    ADDRESS = State()
    PRICE = State()
    CATEGORY = State()


class BookingState(StatesGroup):
    FIRST_NAME = State()
    LAST_NAME = State()
    PHONE = State()


class ReviewState(StatesGroup):
    TEXT = State()


class QuestionState(StatesGroup):
    WAITING_QUESTION = State()
