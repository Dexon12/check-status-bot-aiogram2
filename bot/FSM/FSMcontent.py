from aiogram.dispatcher.filters.state import StatesGroup, State


class AlertStates(StatesGroup):
    name = State()
    surname = State()
    nickname = State()
