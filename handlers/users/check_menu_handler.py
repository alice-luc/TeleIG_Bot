from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from keyboards.default import check_menu_buttons, menu_buttons
from loader import dp, db
from aiogram import types
from states import MenuState, CheckState
import threading

from utils.misc import rate_limit


@rate_limit(1, 'Назад')
@dp.message_handler(state=CheckState, text='Назад')
async def back_activating(message: types.Message):
    """
    goes back to menu
    :param message:
    """
    await MenuState.M1.set()
    await message.answer('Выбери действие', reply_markup=menu_buttons)


@rate_limit(5, 'Узнать, кто не подписан в ответ')
@dp.message_handler(state=CheckState.C1, text='Узнать, кто не подписан в ответ')
async def rats_check_activating(message: types.Message):
    """
    sets the state ad asks for auth data
    :param message:
    """
    await CheckState.C2.set()
    await message.answer('Введи логин для продолжения или "Назад" для возвращения в главное меню\n\
\n⛔️Данные не хранятся в \
системе. \nПосле запуска бота советую удалить сообщение в целях безопасности')


@rate_limit(5, 'Отписать ботов')
@dp.message_handler(state=CheckState.C1, text='Отписать ботов')
async def bots_block_activating(message: types.Message):
    """
    sets the state ad asks for auth data

    :param message:
    """
    await CheckState.C3.set()
    await message.answer('Введи логин для продолжения или "Назад" для возвращения в главное меню')


@rate_limit(5, 'Проверить подписчиков')
@dp.message_handler(state=MenuState.M2, text='Проверить подписчиков')
async def check_activating(message: types.Message):
    """
        sets the state ad asks for the further action


    :param message:
    """
    await CheckState.C1.set()
    await message.answer('Что ты хочешь?', reply_markup=check_menu_buttons)


@dp.message_handler(state=CheckState.C2)
async def rats_detecting_start(message: types.Message, state: FSMContext):
    """
    returns list of follows that dont follow the consumer back
    :param message:
    :param state:
    """
    from IgSide.Server.check_bot import rats_detection
    login = message.text.split(' ')[-1]
    tg_id = message.from_user.id
    await state.finish()
    if db.check_membership(tg_id, login):
        rats = rats_detection(login)
        if rats:
            await message.answer('💩\nВот список крысёнышей, не подписанных в ответ:')
            await message.answer('\n'.join(rats))
        else:
            await message.answer('Либо у тебя очень интересный профиль, либо ты забыл авторизоваться\n\
Крысёнышей не обнаружено👍🏻')


@dp.message_handler(state=CheckState.C3)
async def login_unfollow_activating(message: types.Message):
    """
    when data is given it goes to ig_bot and runs the unfollowing algorithm
    :param message:
    """
    from IgSide.Server import unfollow_bots_start
    from handlers.users.subscription_handler import notifying
    login = message.text
    tg_id = message.from_user.id
    await MenuState.M1.set()
    if db.check_membership(tg_id, login):
        threading.Thread(target=unfollow_bots_start, args=(login, tg_id)).start()
        from config import admins
        await notifying(admins[0], f'Запущена проверка подписчиков у {login}')
        await message.answer('✅ Принято!\nЯ начал чистить список твоих подписчиков от ботов. Когда закончу, дам знать!',
                             reply_markup=menu_buttons)
    else:
        await message.answer('Кажется, твоя подписка не активна 🥺\n\
Оплати подписку <a href="https://www.tinkoff.ru/rm/khvorostova.alisa1/RluPE17867">по этой ссылке</a> или попробуй ещё \
раз позднее.', reply_markup=menu_buttons, parse_mode=ParseMode.HTML)


#
# @dp.message_handler(state=CheckState.C2)
# async def login_check_activating(message: types.Message):
#     """
#
#     :param message:
#     """
#     login = message.text
#     await MenuState.M1.set()
#     await message.answer('Функция проверки подписчиков и подписок запущена на аккаунте ', login,
#                          reply_markup=menu_buttons)
