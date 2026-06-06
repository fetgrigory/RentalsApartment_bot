from aiogram.fsm.state import StatesGroup, State


# States group
class BookingState(StatesGroup):
    FIRST_NAME = State()
    LAST_NAME = State()
    PHONE = State()


class ReviewState(StatesGroup):
    TEXT = State()


class QuestionState(StatesGroup):
    WAITING_QUESTION = State()


class AddDocumentState(StatesGroup):
    TEXT = State()
