from aiogram import Router, F
from aiogram.types import CallbackQuery

from util.middleware import LocaleMiddleware
from util.callback import GromeCallback
from settings import  Settings
from db.queries import get_user_payment_status, get_user_expiry
from keyboard.onboarding_kb import elc_kb, grome_kb, back_button, start_kb


menu_router = Router()
menu_router.callback_query.middleware(LocaleMiddleware())

@menu_router.callback_query(GromeCallback.filter(F.group == 'menu'))
async def menu_handler(callback: CallbackQuery, text: dict, callback_data: GromeCallback):
    status = get_user_payment_status(callback.from_user.id)
    date = get_user_expiry(callback.from_user.id).date()
    back = back_button(locale_name=text['back']['text'], target='menu')

    if callback_data.name == text['menu']['buttons'][0]:
        elc_markup = elc_kb(buttons=text['elc']['buttons'])
        elc_markup.inline_keyboard.append(back.inline_keyboard[0])

        await callback.message.edit_text(text=text['elc']['text'], reply_markup=elc_markup)

    elif callback_data.name == text['menu']['buttons'][1]:
        grome_markup = grome_kb(buttons=text['menu_subscribe']['buttons'], group='menu_subscribe')
        grome_markup.inline_keyboard.append(back.inline_keyboard[0])
        
        if status == 'Paid':
            necessary_button = grome_markup.model_copy()
            necessary_button.inline_keyboard[0].pop(1)

            text = text['menu_subscribe']['text_if_paid'].format(date=date)

            await callback.message.edit_text(text=text, reply_markup=necessary_button)

        else:
            necessary_button = grome_markup.model_copy()
            necessary_button.inline_keyboard[0].pop(0)

            if status == 'Trial':
                text = text['menu_subscribe']['text_if_trial'].format(date=date)

                await callback.message.edit_text(text=text, reply_markup=necessary_button)
            else:
                text = text['menu_subscribe']['text_if_npaid'].format(date=date)

                await callback.message.edit_text(text=text, reply_markup=necessary_button)
    
    elif callback_data.name == text['menu']['buttons'][2]:
        start_markup = start_kb()
        start_markup.inline_keyboard.append(back.inline_keyboard[0])

        await callback.message.edit_text(Settings.START_TEXT, reply_markup=start_markup)
    
    elif callback_data.name == text['menu']['buttons'][3]:
        text = text['support']['text'].format(user=Settings.SUPPORT_USER)

        await callback.message.edit_text(text=text, reply_markup=back)

@menu_router.callback_query(GromeCallback.filter(F.group == 'back'))
async def example(callback: CallbackQuery, text: dict, callback_data: GromeCallback):
    if callback_data.name == 'menu':
        await callback.message.edit_text(text=text['menu']['text'], 
                                        reply_markup=grome_kb(buttons=text['menu']['buttons'], group='menu'))