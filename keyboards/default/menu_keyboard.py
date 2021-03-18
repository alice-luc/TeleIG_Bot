from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад'),
        ],
        [
            KeyboardButton(text='Продвигать инстаграм аккаунт'),

        ],
        [
            KeyboardButton(text='Посмотреть статистику'),
        ],

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)