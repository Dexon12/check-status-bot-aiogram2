from datetime import timedelta, datetime, time
import asyncio

from bot.DataBase.db import UserService
from bot.Keyboards.inlineKb import work_or
from bot_instance import bot, list_for_admin


def delay_time():
    eleven = None

    def time_until_eleven():
        now = datetime.now()
        nonlocal eleven

        if eleven is None:
            eleven = datetime.combine(now.date(), time(hour=16, minute=59))
        if now > eleven:
            eleven += timedelta(seconds=10)
            print(eleven)

        difference = abs(eleven - now)
        return difference.total_seconds()
    return time_until_eleven


delay_test = delay_time()  # Спросить зачем так делать (выносить в отдельную переменную)


async def send_msg():
    all_id = set(await UserService.select_users_id())
    while True:
        delay = delay_test()
        print(2, delay)
        await asyncio.sleep(delay)
        for ids in all_id:
            is_subscribed = await UserService.take_subscribe(int(ids))
            if is_subscribed:  # Получаем актуальное значение задержки перед каждой отправкой сообщения
                await bot.send_message(chat_id=int(ids), text='Работаешь сегодня?', reply_markup=work_or())
            else:
                continue  # Пропускаем отправку сообщения и переходим к следующему пользователю
