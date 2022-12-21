from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from IgSide.Server.trial_bot import trial_purchase
from keyboards.default import start_menu_buttons
from states import TrialState
from loader import data_base, dispatcher
from utils.misc import rate_limit
from utils.notify_admins import membership_notify, errors_notify
import threading


@rate_limit(5, 'trial')
@dispatcher.message_handler(Command('trial'))
async def trial_go(message: types.Message):
    """
    starts trial 3 days version with the given data
    :param message:
    :return:
    """
    await TrialState.T1.set()
    await message.answer('🥳Для начала пробной 3х-дневной версии введи свой логин и пароль. \n⛔️Данные не хранятся в \
системе. \nПосле запуска бота советую удалить сообщение с паролем в целях безопасности')


@dispatcher.message_handler(state=TrialState.T1)
async def trial_start(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    login, password = message.text.split(' ')
    await state.finish()
    if not data_base.trial_select_user(tg_id, login):
        await message.answer('✅Поехали работать!\nВернусь через 3 дня с отчетом\n😎')
        await membership_notify(dispatcher, login, tg_id)
        threading.Thread(target=trial_purchase, args=(login, password)).start()
    else:
        await message.answer('😔Твоя пробная подписка истекла, для продолжения работы оплати 15$ или напиши \n\
@alohayoung\n для получения индивидуальной или групповой скидки😉')



