from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice

import datetime
import math
import os

from util.middleware import LocaleMiddleware
from util.callback import GromeCallback, AlphaCallback
from settings import  Settings
from logger import main_logger
from db.queries import get_user_payment_status, get_user_expiry, update_value_user, get_user_elc
from keyboard.onboarding_kb import elc_kb, grome_kb, back_button, start_kb


menu_router = Router()
menu_router.callback_query.middleware(LocaleMiddleware())

@menu_router.callback_query(GromeCallback.filter(F.group == 'menu'))
async def menu_handler(callback: CallbackQuery, text: dict, callback_data: GromeCallback):
    status = get_user_payment_status(callback.from_user.id)
    date = get_user_expiry(callback.from_user.id).date()
    elc = get_user_elc(callback.from_user.id)
    back = back_button(locale_name=text['back']['text'], target='menu')

    if callback_data.name == text['menu']['buttons'][0]:
        elc_markup = elc_kb(buttons=text['elc']['buttons'])
        elc_markup.inline_keyboard.append(back.inline_keyboard[0])

        for row in elc_markup.inline_keyboard:
            for button in row:
                if ',' in elc:
                    for i in elc.split(','):
                        if i == button.callback_data.split(':')[2]:
                            button.text += ' ⏺️'
                else:
                    if elc == button.callback_data.split(':')[2]:
                        button.text += ' ⏺️'
                    

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
async def back_handler(callback: CallbackQuery, text: dict, callback_data: GromeCallback):
    if callback_data.name == 'menu':
        await callback.message.edit_text(text=text['menu']['text'], 
                                        reply_markup=grome_kb(buttons=text['menu']['buttons'], group='menu'))

@menu_router.callback_query(GromeCallback.filter(F.group == 'menu_subscribe'))
async def menu_subscribe_handler(callback: CallbackQuery, text: dict, callback_data: GromeCallback):
    back = back_button(locale_name=text['back']['text'], target='menu')

    if callback_data.name == text['menu_subscribe']['buttons'][0]:
        markup = grome_kb(buttons=text['choice']['buttons'], group='choice_upd')
        markup.inline_keyboard.append(back.inline_keyboard[0])

        await callback.message.edit_text(text=text['choice']['text'], reply_markup=markup)
    else:
        markup = grome_kb(buttons=text['choice']['buttons'], group='choice')
        markup.inline_keyboard.append(back.inline_keyboard[0])

        await callback.message.edit_text(text=text['choice']['text'], reply_markup=markup)

@menu_router.callback_query(GromeCallback.filter(F.group == 'choice_upd'))
async def menu_subscribe_handler(callback: CallbackQuery, text: dict, callback_data: GromeCallback):
    date_diff: datetime.datetime = get_user_expiry(callback.from_user.id) - datetime.datetime.now()
    index = text['choice']['buttons'].index(callback_data.name)

    if date_diff.days < Settings.PERIODS[index]:
        day_diff = Settings.PERIODS[index] - date_diff.days
        missing_price = math.ceil((day_diff / (Settings.PERIODS[index] / 100)) * (Settings.PRICES[index] / 100) / 100)

        if missing_price > 80:
            await callback.message.delete()

            await callback.bot.send_invoice(
                chat_id=callback.message.chat.id,
                title=text['invoice']['title'].format(time=callback_data.name.lower()),
                description=text['invoice']['description'].format(time=callback_data.name.lower()),
                payload=str(day_diff),
                currency='RUB',
                prices=[LabeledPrice(label=text['invoice']['label'], amount=missing_price * 100)],
                provider_token=os.getenv('PROVIDER_TOKEN'),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=text['invoice']['buttons'][0], pay=True)],
                    [InlineKeyboardButton(text=text['invoice']['buttons'][1], callback_data='continue')]
                ])
            )
        else:
            await callback.answer(text=text['dont_upgrade']['text'])
    else:
        await callback.answer(text=text['dont_upgrade']['text'])


@menu_router.callback_query(AlphaCallback.filter(F.group.in_(['elc'])))
async def menu_subscribe_handler(callback: CallbackQuery, text: dict, callback_data: AlphaCallback):
    elc_markup = callback.message.reply_markup

    elc = get_user_elc(callback.from_user.id)

    for row in elc_markup.inline_keyboard:
        for button in row:
            if callback_data.alpha2_form == button.callback_data.split(':')[2]:
                current_button = button

    if not callback_data.alpha2_form in elc:
        elc += ',' + callback_data.alpha2_form
        current_button.text += ' ⏺️'

        update_value_user(value=elc, user=callback.from_user.id, field=callback_data.group)
        await callback.message.edit_text(text=text['elc']['text'], reply_markup=elc_markup)
    else:
        if ',' in elc:
            elc = elc.replace(',' + callback_data.alpha2_form, '')
            current_button.text = current_button.text.replace(' ⏺️', '')

            update_value_user(value=elc, user=callback.from_user.id, field=callback_data.group)
            await callback.message.edit_text(text=text['elc']['text'], reply_markup=elc_markup)

@menu_router.callback_query(AlphaCallback.filter(F.group == 'locale'))
async def menu_subscribe_handler(callback: CallbackQuery, text: dict, callback_data: AlphaCallback):
    update_value_user(value=callback_data.alpha2_form, user=callback.from_user.id, field=callback_data.group)
    await callback.answer(text=text['successful_change']['text'])
    await callback.message.edit_text(text=text['menu']['text'], 
                                        reply_markup=grome_kb(buttons=text['menu']['buttons'], group='menu'))