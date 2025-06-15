from aiogram import Router
from aiogram.types import PreCheckoutQuery

from db.queries import check_status
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