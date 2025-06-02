from aiogram.filters.callback_data import CallbackData


class LocaleCallback(CallbackData, prefix='locale'):
    group: str
    alpha2_form: str

class ElcCallback(CallbackData, prefix='elc'):
    group: str
    alpha2_form: str

class LevelCallback(CallbackData, prefix='level'):
    group: str
    number: int

class SubscribeCallback(CallbackData, prefix='subscribe'):
    group: str
    name: str

class MenuCallback(CallbackData, prefix='menu'):
    group: str
    name: str