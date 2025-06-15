from aiohttp import web
from aiogram import Dispatcher
from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler

import os

from glex import bot
from logger import main_logger
from handler.head import head_router


def main() -> None:
    dp = Dispatcher()
    dp.include_routers(head_router)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_requests_handler.register(app, path=os.getenv('WEBHOOK_PATH'))
    
    setup_application(app, dp, bot=bot)
    
    web.run_app(app, host=os.getenv('WEB_SERVER_HOST'), port=int(os.getenv('WEB_SERVER_PORT')), access_log=main_logger)

if __name__ == "__main__":
    main_logger.debug('Payment сервис запущен!')
    main()