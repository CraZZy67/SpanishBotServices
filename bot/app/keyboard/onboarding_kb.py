from aiogram.utils.keyboard import InlineKeyboardBuilder
from settings import Settings


def start_kb():
    builder = InlineKeyboardBuilder()
    
    builder.button(text=Settings.START_BUTTONS[0], callback_data=Settings.START_BUTTONS[0])
    builder.button(text=Settings.START_BUTTONS[1], callback_data=Settings.START_BUTTONS[1])
    builder.button(text=Settings.START_BUTTONS[2], callback_data=Settings.START_BUTTONS[2])
    
    return builder.as_markup()