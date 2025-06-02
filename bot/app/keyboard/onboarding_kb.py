from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
import pycountry

from settings import Locale
from utils.callback import LocaleCallback, ElcCallback, LevelCallback, SubscribeCallback, MenuCallback


def start_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for alpha2 in Locale.locales:
        builder.button(text=pycountry.languages.get(alpha_2=alpha2).name, 
                       callback_data=LocaleCallback(group='locale', alpha2_form=alpha2))

    return builder.as_markup()

def elc_kb(buttons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for name in buttons:
        country = pycountry.countries.get(name=name)
        builder.button(text=name, callback_data=ElcCallback(group='elc', alpha2_form=country.alpha_2))
    
    return builder.as_markup()

def level_kb(buttons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for index, name in enumerate(buttons):
        builder.button(text=name, callback_data=LevelCallback(group='level', number=index))
    
    return builder.as_markup()

def subscribe_kb(buttons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for name in buttons:
        builder.button(text=name, callback_data=SubscribeCallback(group='subscribe', name=name))
    
    return builder.as_markup()

def menu_kb(buttons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for name in buttons:
        builder.button(text=name, callback_data=MenuCallback(group='menu', name=name))
    
    return builder.as_markup()