from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


check_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад'),
        ],
        [
            KeyboardButton(text='Узнать, кто не подписан в ответ'),
        ],
        [
            KeyboardButton(text='Отписать ботов'),
        ],

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)