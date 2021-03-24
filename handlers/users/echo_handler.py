from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.misc import rate_limit


@rate_limit(2)
@dp.message_handler()
async def bot_echo(message: types.Message, state: FSMContext):
    """
    returns messages back to user
    """
    await state.finish()
    await message.answer('Для старта введите команду\n/start')
