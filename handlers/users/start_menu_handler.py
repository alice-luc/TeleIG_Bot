from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from data.config import greating_text
from loader import dispatcher
from keyboards.default import start_menu_buttons
from utils.misc import rate_limit


@rate_limit(10, 'start')
@dispatcher.message_handler(Command('start'))
async def bot_start(message: types.Message):
    """
    returns start menu keyboard
    """
    await message.answer(f'Привет, {message.from_user.full_name}! 🤗\n{greating_text}', reply_markup=start_menu_buttons)


@rate_limit(10, 'Подробнее')
@dispatcher.message_handler(text='Подробнее')
async def bot_info(message: types.Message):
    """
    Method returns supporting text for new users
    """
    from data.config import more_text
    await message.answer(more_text, reply_markup=start_menu_buttons)
