from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def keyboard():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Подписаться на оповещения', callback_data='AlertTrue'), InlineKeyboardButton(
            'Не подписываться', callback_data='AlertFalse')]
    ])
    return ikb


def yes_no_kb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Да', callback_data='yes'), InlineKeyboardButton('Нет', callback_data='no')]
    ])
    return ikb


def yes_or_no_kb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='da'), InlineKeyboardButton(text='Нет', callback_data='net')]
    ])
    return ikb


def work_or():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='yep'), InlineKeyboardButton(text='Нет', callback_data='nope')]
    ])
    return ikb
