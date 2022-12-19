from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from config import greating_text
from loader import dp
from keyboards.default import start_menu_buttons
from utils.misc import rate_limit


@rate_limit(10, 'start')
@dp.message_handler(Command('start'))
async def bot_start(message: types.Message):
    """
    returns start menu keyboard
    """
    await message.answer(f'Привет, {message.from_user.full_name}! 🤗\n{greating_text}', reply_markup=start_menu_buttons)


@rate_limit(10, 'Подробнее')
@dp.message_handler(text='Подробнее')
async def bot_info(message: types.Message):
    """
    Method returns supporting text for new users
    """
    from config import more_text
    await message.answer(more_text, reply_markup=start_menu_buttons)
