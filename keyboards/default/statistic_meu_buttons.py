from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

statistic_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад'),
        ],
        [
            KeyboardButton(text='Оплатить подписку'),
        ],
        [
            KeyboardButton(text='Проверить подписку на аккаунте'),

        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)