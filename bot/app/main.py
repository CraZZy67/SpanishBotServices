from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from glex import bot
from settings import Locale
from handler.onboarding import onboarding_router


WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 8080
WEBHOOK_PATH = "/"
BASE_WEBHOOK_URL = "https://devoutly-wholesome-gadwall.cloudpub.ru"

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")

def main() -> None:
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_routers(onboarding_router)
    
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    setup_application(app, dp, bot=bot)
    
    Locale.get_locales()
    
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    main()