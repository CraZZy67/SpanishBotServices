from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message

from db.queries import check_status, update_subscribe
from logger import  main_logger


head_router = Router()

@head_router.pre_checkout_query()
async def pre_checkout(pre_checkout: PreCheckoutQuery):
    if not check_status(pre_checkout.from_user.id):
        await pre_checkout.answer(True)
        main_logger.debug('Pre-checkout True')
    else:
        await pre_checkout.answer(False, error_message='Already paid')
        main_logger.debug('Pre-checkout False')

@head_router.message(F.successful_payment)
async def handl_payment(message: Message):
    update_subscribe(message.successful_payment, message.from_user.id)
    main_logger.debug('Данные обновлены')
