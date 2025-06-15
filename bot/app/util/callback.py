from aiogram.filters.callback_data import CallbackData


class AlphaCallback(CallbackData, prefix='alpha'):
    group: str
    alpha2_form: str
    
class LevelCallback(CallbackData, prefix='level'):
    group: str
    number: int

class GromeCallback(CallbackData, prefix='grome'):
    group: str
    name: str
