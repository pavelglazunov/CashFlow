from aiogram.dispatcher.filters.state import State, StatesGroup


class StartGame(StatesGroup):
    start = State()


class JoinGame(StatesGroup):
    token = State()


class RemoveGame(StatesGroup):
    token = State()