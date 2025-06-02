from aiogram.fsm.state import State, StatesGroup


class NewUser(StatesGroup):
    locale = State()
    elc = State()
    level = State()
    subscription = State()
    subscribe = State()
    