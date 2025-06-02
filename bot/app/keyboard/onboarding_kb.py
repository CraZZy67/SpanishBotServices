from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
import pycountry

from settings import Locale
from utils.callback import AlphaCallback, LevelCallback, GromeCallback


def start_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for alpha2 in Locale.locales:
        builder.button(text=pycountry.languages.get(alpha_2=alpha2).name, 
                       callback_data=AlphaCallback(group='locale', alpha2_form=alpha2))

    builder.adjust(2, repeat=True)
    return builder.as_markup()

def elc_kb(buttons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for name in buttons:
        country = pycountry.countries.get(name=name)
        builder.button(text=name, callback_data=AlphaCallback(group='elc', alpha2_form=country.alpha_2))
    
    builder.adjust(2, repeat=True)
    return builder.as_markup()

def level_kb(buttons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for index, name in enumerate(buttons):
        builder.button(text=name, callback_data=LevelCallback(group='level', number=index))
    
    builder.adjust(2, repeat=True)
    return builder.as_markup()

def grome_kb(buttons: list, group: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for name in buttons:
        builder.button(text=name, callback_data=GromeCallback(group=group, name=name))
    
    builder.adjust(2, repeat=True)
    return builder.as_markup()