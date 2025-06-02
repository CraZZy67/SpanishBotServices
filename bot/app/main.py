from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

import os

from glex import bot
from settings import Locale
from handler.onboarding import onboarding_router, payments_router


load_dotenv()

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{os.getenv('BASE_WEBHOOK_URL')}{os.getenv('WEBHOOK_PATH')}")

def main() -> None:
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_routers(onboarding_router, payments_router)
    
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    
    webhook_requests_handler.register(app, path=os.getenv('WEBHOOK_PATH'))
    
    setup_application(app, dp, bot=bot)
    
    Locale.get_locales()
    
    web.run_app(app, host=os.getenv('WEB_SERVER_HOST'), port=int(os.getenv('WEB_SERVER_PORT')))

if __name__ == "__main__":
    main()