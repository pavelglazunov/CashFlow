from aiogram.dispatcher.filters.state import State, StatesGroup


class StartGame(StatesGroup):
    start = State()


class JoinGame(StatesGroup):
    token = State()


class RemoveGame(StatesGroup):
    token = State()


class Professionals(StatesGroup):
    prof = State()


class UserAnswer(StatesGroup):
    vv_answer = State()
    answer2 = State()
    answer3 = State()
    answer4 = State()
    answer5 = State()

    __session_name__ = ""


class DealData(StatesGroup):
    answer1 = State()
    answer2 = State()
    answer3 = State()
    answer4 = State()
    answer5 = State()
    answer6 = State()

    __session_name__ = ""
    __user_id__ = ""
    __message__ = ""
