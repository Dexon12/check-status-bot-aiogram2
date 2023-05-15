from aiogram import types, Dispatcher, Bot
from datetime import datetime
from aiogram.dispatcher.storage import FSMContext
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_instance import bot
from bot.Keyboards.inlineKb import keyboard, yes_no_kb
from bot.DataBase.db import DataBaseEngine
from bot.FSM.FSMcontent import AlertStates
from bot.DataBase.db import UserService
# admins = [973459911]



async def start_command(message: types.Message) -> None:
    await message.answer('Привет! Я TexDocktor Bot, нам важно знать выходишь ли ты сегодня на работу, '
                         'мы можем получить эту информацию? :)', reply_markup=keyboard())
    await message.delete()


async def cb_alerttrue(callback: types.CallbackQuery) -> None:
    await callback.answer('Вы подписались на рассылку!')
    await AlertStates.name.set()
    await callback.message.answer('Подскажите пожалуйста как вас зовут?')


async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        data['user_id'] = message.from_user.id
    await message.answer('Подскажите пожалуйста какая у вас фамилия?')
    await AlertStates.next()


async def set_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await AlertStates.next()
    await message.answer('Напишите пожалуйста ваш Никнейм')


async def set_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.from_user.username

    await message.answer('Спасибо, все готово')
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id,
                               text=f"Все верно: Имя: {data['name']}, Фамилия: {data['surname']}?",
                               reply_markup=yes_no_kb())

    async with state.proxy() as data:
        await UserService.insert_user(data['user_id'], data['name'], data['surname'], data['nickname'],
                             False, datetime.now().date())
        await state.finish()


async def yes_callback(callback: types.CallbackQuery):
    await callback.message.answer('Отлично вы зарегистрированы, уведомление будет приходить в 11 часов! Спасибо!')


async def no_callback(callback: types.CallbackQuery):
    await callback.message.answer('Хорошо, попробуем еще раз')
    await AlertStates.name.set()
    await callback.message.answer('Подскажите пожалуйста как вас зовут?')


async def cb_alertfalse(callback: types.CallbackQuery) -> None:
    await callback.answer('Чтобы подписаться на рассылку напишите команду /start')
    await callback.message.answer('Чтобы подписаться на рассылку напишите команду /start')


async def help_command(message: types.Message) -> None:
    await message.answer('Привет! Чтобы подписаться на уведомления напишите "/start"')
    await message.delete()


# async def send_alert(bot: Bot) -> None:
#     await bot.send_message(chat_id=db.select_something(user_id="telegram_id"), text='fdsdsf')


def register_message_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command, commands=['start'], state=None)
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_callback_query_handler(cb_alerttrue, text='AlertTrue')
    dp.register_callback_query_handler(cb_alertfalse, text='AlertFalse')
    dp.register_message_handler(set_name, state=AlertStates.name)
    dp.register_message_handler(set_surname, state=AlertStates.surname)
    dp.register_message_handler(set_finish, state=AlertStates.nickname)
    dp.register_callback_query_handler(no_callback, text='no', state=None)
    dp.register_callback_query_handler(yes_callback, text='yes')
