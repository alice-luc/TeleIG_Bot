from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


insta_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад'),
        ],
        [
            KeyboardButton(text='Раздавать лайки'),
        ],
        [
            KeyboardButton(text='Проверить подписчиков'),
        ],

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)