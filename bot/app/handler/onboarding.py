from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

import os

from settings import Settings, Locale
from keyboard.onboarding_kb import start_kb, elc_kb, level_kb, grome_kb
from util.fsm import NewUser
from util.callback import AlphaCallback, LevelCallback, GromeCallback
from util.middleware import LocaleMiddleware
from glex import bot
from db.queries import add_user_info, check_user, get_user_locale


onboarding_router = Router()
payments_router = Router()

payments_router.callback_query.middleware(LocaleMiddleware())

@onboarding_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if check_user(message.from_user.id):
        text = get_user_locale(message.from_user.id) 
        await message.answer(text=text['menu']['text'], reply_markup=grome_kb(buttons=text['menu']['buttons'],
                                                                                          group='menu'))
    else:
        await message.answer(Settings.START_TEXT, reply_markup=start_kb())
        
        await state.set_state(NewUser.locale)
        await state.update_data(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )

@onboarding_router.callback_query(NewUser.locale, AlphaCallback.filter(F.group == 'locale'))
async def catch_locale(callback: CallbackQuery, callback_data: AlphaCallback, state: FSMContext):
    text = Locale.get_locale_text(callback_data.alpha2_form)
    await callback.message.edit_text(text=text['elc']['text'], reply_markup=elc_kb(buttons=text['elc']['buttons']))
    
    await state.set_state(NewUser.elc)
    await state.update_data(locale=callback_data.alpha2_form, text=text)

@onboarding_router.callback_query(NewUser.elc, AlphaCallback.filter(F.group == 'elc'))
async def catch_elc(callback: CallbackQuery, callback_data: AlphaCallback, state: FSMContext):
    data = await state.get_data()
    text = data['text']
    await callback.message.edit_text(text=text['level']['text'], reply_markup=level_kb(buttons=text['level']['buttons']))
    
    await state.set_state(NewUser.level)
    await state.update_data(elc=callback_data.alpha2_form)

@onboarding_router.callback_query(NewUser.level, LevelCallback.filter(F.group == 'level'))
async def catch_level(callback: CallbackQuery, callback_data: LevelCallback, state: FSMContext):
    data = await state.get_data()
    text = data['text']

    add_user_info(
        user_id=data['user_id'], first_name=data['first_name'],
        last_name=data['last_name'], locale=data['locale'],
        elc=data['elc'], level=callback_data.number
        )
    
    await callback.message.edit_text(text=text['subscribe']['text'], reply_markup=grome_kb(buttons=text['subscribe']['buttons'],
                                                                                           group='subscribe'))
    
    await state.set_state(NewUser.subscription)

@onboarding_router.callback_query(NewUser.subscription, GromeCallback.filter(F.group == 'subscribe'))
async def catch_subscription(callback: CallbackQuery, callback_data: GromeCallback, state: FSMContext):
    data = await state.get_data()
    text = data['text']
    
    if text['subscribe']['buttons'][0] == callback_data.name:
        await callback.message.edit_text(text=text['menu']['text'], reply_markup=grome_kb(buttons=text['menu']['buttons'],
                                                                                          group='menu'))
    else:
        await callback.message.edit_text(text=text['choice']['text'], reply_markup=grome_kb(buttons=text['choice']['buttons'],
                                                                                          group='choice'))
        
    await state.clear()

@payments_router.callback_query(GromeCallback.filter(F.group == 'choice'))
async def choice(callback: CallbackQuery, text: dict, callback_data: GromeCallback):
    for index, name in enumerate(text['choice']['buttons']):
        if name == callback_data.name:
            number = index
            
    await callback.message.delete()
    
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=text['invoice']['title'].format(time=callback_data.name.lower()),
        description=text['invoice']['description'].format(time=callback_data.name.lower()),
        payload=str(Settings.PERIODS[number]),
        currency='RUB',
        prices=[LabeledPrice(label=text['invoice']['label'], amount=Settings.PRICES[number])],
        provider_token=os.getenv('PROVIDER_TOKEN'),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=text['invoice']['buttons'][0], pay=True)],
            [InlineKeyboardButton(text=text['invoice']['buttons'][1], callback_data='cancel')]
        ])
    )

@payments_router.callback_query(F.data == 'cancel')
async def choice(callback: CallbackQuery, text: dict):
    await callback.message.delete()
    await callback.message.answer(text=text['menu']['text'], 
                                     reply_markup=grome_kb(buttons=text['menu']['buttons'], group='menu'))