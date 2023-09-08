# новые импорты!
from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types.base import TelegramObject


class SomeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        print("Before handler")
        result = await handler(event, data)
        print("After handler")
        return result