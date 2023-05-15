from aiogram import types, Dispatcher
import asyncio

from bot.handlers.handler import register_message_handlers
from bot_instance import bot, storage
from bot.DataBase.db import DataBaseEngine


def register_handlers(dp: Dispatcher):
    register_message_handlers(dp)


def on_start():
    print('Bot is activate')


async def main():
    dp = Dispatcher(bot, storage=storage)
    register_handlers(dp)
    engine = DataBaseEngine()
    try:
        await engine.create_db()
        on_start()
        task1 = asyncio.create_task(dp.start_polling())
        task2 = asyncio.create_task(engine.get_pool())
        await asyncio.gather(task1, task2)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    asyncio.run(main())
