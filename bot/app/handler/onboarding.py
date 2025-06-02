from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from settings import Settings, Locale
from keyboard.onboarding_kb import start_kb, elc_kb, level_kb, subscribe_kb, menu_kb
from utils.fsm import NewUser
from db.queries import new_user_info
from utils.callback import LocaleCallback, ElcCallback, LevelCallback, SubscribeCallback


onboarding_router = Router()

@onboarding_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(Settings.START_TEXT, reply_markup=start_kb())
    
    await state.set_state(NewUser.locale)
    await state.update_data(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

@onboarding_router.callback_query(NewUser.locale, LocaleCallback.filter(F.group == 'locale'))
async def catch_locale(callback: CallbackQuery, callback_data: LocaleCallback, state: FSMContext):
    text = Locale.get_locale_text(callback_data.alpha2_form)
    await callback.message.edit_text(text=text['elc']['text'], reply_markup=elc_kb(buttons=text['elc']['buttons']))
    
    await state.set_state(NewUser.elc)
    await state.update_data(locale=callback_data.alpha2_form, text=text)

@onboarding_router.callback_query(NewUser.elc, ElcCallback.filter(F.group == 'elc'))
async def catch_elc(callback: CallbackQuery, callback_data: ElcCallback, state: FSMContext):
    data = await state.get_data()
    text = data['text']
    await callback.message.edit_text(text=text['level']['text'], reply_markup=level_kb(buttons=text['level']['buttons']))
    
    await state.set_state(NewUser.level)
    await state.update_data(elc=callback_data.alpha2_form)

@onboarding_router.callback_query(NewUser.level, LevelCallback.filter(F.group == 'level'))
async def catch_level(callback: CallbackQuery, callback_data: LevelCallback, state: FSMContext):
    data = await state.get_data()
    text = data['text']
    await callback.message.edit_text(text=text['subscribe']['text'], reply_markup=subscribe_kb(buttons=text['subscribe']['buttons']))
    
    await state.set_state(NewUser.subscription)
    await state.update_data(level=callback_data.number)

@onboarding_router.callback_query(NewUser.subscription, SubscribeCallback.filter(F.group == 'subscribe'))
async def catch_level(callback: CallbackQuery, callback_data: SubscribeCallback, state: FSMContext):
    data = await state.get_data()
    text = data['text']
    
    if text['subscribe']['buttons'][0] == callback_data.name:
        new_user_info(
            user_id=data['user_id'], first_name=data['first_name'],
            last_name=data['last_name'], locale=data['locale'],
            elc=data['elc'], level=data['level']
        )
        
        await callback.message.edit_text(text=text['menu']['text'], reply_markup=menu_kb(buttons=text['menu']['buttons']))
        await state.clear()
    else:
        await callback.answer('В разработке')