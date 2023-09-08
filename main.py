import asyncio
import logging

from aiogram import types, Dispatcher

from bot.handlers.handler import register_message_handlers
from bot_instance import bot, storage
from bot.DataBase.db import DataBaseEngine
from bot.middlewares.throttling_middleware import register_throttle_middleware
from bot.services.sending_msg import send_msg


def register_handlers(dp: Dispatcher):
    register_message_handlers(dp)

def register_middlewares(dp: Dispatcher):
    register_throttle_middleware(dp)

async def on_start():
    await send_msg()

async def main() -> None:
    """Entry Point"""

    dp = Dispatcher(bot, storage=storage)
    register_handlers(dp)
    register_middlewares(dp)

    engine = DataBaseEngine()
    await engine.create_db()

    try:
        
        task1 = asyncio.create_task(dp.start_polling())
        task2 = asyncio.create_task(engine.get_pool())
        await on_start()
        logging.info('[INFO]: Bot has been started')
        await asyncio.gather(task1, task2)
    except Exception as _ex:
        logging.error(f'[ERROR]: An error has occured - {_ex}')
    finally:
        logging.info('[INFO]: Bot has been terminated')
        


if __name__ == '__main__':
    fmt = '%(asctime)s: %(message)s'

    logging.basicConfig(
        filename='logs.txt',
        filemode='a+',
        format=fmt,
        level=logging.INFO
    )

    asyncio.run(main())
