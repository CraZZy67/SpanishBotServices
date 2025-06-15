from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from typing import Callable, Awaitable, Any, Dict
from db.queries import get_user_locale


class LocaleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery, data: Dict[str, Any]
    ) -> Any:
        
        data['text'] = get_user_locale(user=event.from_user.id)
        return await handler(event, data)