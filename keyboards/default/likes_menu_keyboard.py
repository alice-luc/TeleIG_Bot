from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton


like_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад'),
        ],
        [
            KeyboardButton(text='Друзей друзей'),
        ],
        [
            KeyboardButton(text='Хэштеги и локации'),
        ]

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)