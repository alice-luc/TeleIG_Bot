from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подробнее'),
        ],
        [
            KeyboardButton(text='Оформить подписку'),
        ],
        [
            KeyboardButton(text='Меню'),

        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)