import threading

from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from data.config import admins
from keyboards.default import like_menu_buttons, menu_buttons, start_menu_buttons
from loader import dispatcher, data_base
from aiogram import types
from states import LikeState, MenuState
from utils.misc import rate_limit
from handlers.users.subscription_handler import notifying


@rate_limit(1, 'Назад')
@dispatcher.message_handler(state=LikeState, text='Назад')
async def back_activating(message: types.Message):
    """
    if user chose back option
    """
    await MenuState.M1.set()
    await message.answer('Выбери дейсивие', reply_markup=menu_buttons)


@dispatcher.message_handler(state=LikeState.Li2)
async def taking_datas_for_likes(message: types.Message):
    """
    starts ig-side code which likes followers of consumer's followers
    """
    from IgSide.Server import like_start
    login = message.text.split(' ')[0]
    tg_id = message.from_user.id
    await MenuState.M1.set()
    membership = data_base.check_membership(tg_id, login)
    if membership != 0:
        await notifying(admins[0], f'Лайки поехали {login}')
        threading.Thread(target=like_start, args=(login,)).start()
        await message.answer(f'✅ Процесс пошел!\
Я начал раздавать лайки подписчикам твоих подписчиков на аккаунте: {login}\
Если хочешь посмотреть статистику поставленных лайков, напиши @alohayoung')
    else:
        await message.answer('Кажется, твоя подписка не активна 🥺\n\
Оплати подписку <a href="https://www.tinkoff.ru/rm/khvorostova.alisa1/RluPE17867">по этой ссылке</a> или попробуй ещё \
раз позднее.', reply_markup=menu_buttons, parse_mode=ParseMode.HTML)


@dispatcher.message_handler(state=LikeState.Li3)
async def dif_consuming_data_for_likes(message: types.Message, state: FSMContext):
    """
    another method of likes is to go to hashtags' posts
    """
    from IgSide.Server import like_start
    login = message.text.split(' ')[0]
    hashtags_list = message.text.split(' ')[1:]
    tg_id = message.from_user.id
    await state.finish()
    print(login, hashtags_list)
    membership = data_base.check_membership(tg_id, login)
    print(membership)
    if membership != 0:
        print(data_base.ig_select_user(tg_id, login))
        await notifying(admins[0], f'Лайки поехали {login}')
        try:
            threading.Thread(target=like_start, args=(login,)).start()
        except:
            pass
        await message.answer(f'✅\nЗапущен алгоритм лайков по локации и хэштегам с аккаунта{login}',
                             reply_markup=start_menu_buttons)
    else:
        await MenuState.M1.set()
        await message.answer('Кажется, твоя подписка не активна 🥺\n\
Оплати подписку <a href="https://www.tinkoff.ru/rm/khvorostova.alisa1/RluPE17867">по этой ссылке</a> или попробуй ещё \
раз позднее.', reply_markup=menu_buttons, parse_mode=ParseMode.HTML)


@rate_limit(5, 'Друзей друзей')
@dispatcher.message_handler(state=LikeState.Li1, text='Друзей друзей')
async def choosing_the_method_of_likes(message: types.Message):
    """
    asks for a login to begin likes method
    """
    await LikeState.Li2.set()
    await message.answer('Введи свой логин для продолжения или "Назад" для возвращения в главное меню.\n\
После старта программы сообщение можно удалить')


@rate_limit(5, 'Хэштеги и локации')
@dispatcher.message_handler(state=LikeState.Li1, text='Хэштеги и локации')
async def choosing_the_method_of_likes1(message: types.Message):
    """
    collects hashtags' list within the next message
    """
    await LikeState.Li3.set()
    await message.answer('Введи свой логин и список хэштегов и локаций через пробел для продолжения или "Назад"\
для возвращения в главное меню\nЛокации вводи целыми ссылками,а хэштэги отдельными словами как на скрине\
\n⛔️Данные не хранятся в \
системе. \nПосле запуска бота советую удалить сообщение в целях безопасности')


@rate_limit(5, 'Раздавать лайки')
@dispatcher.message_handler(state=MenuState.M2, text='Раздавать лайки')
async def like_activating(message: types.Message):
    """
    determines a method of likes that will be used
    """
    await LikeState.Li1.set()
    await message.answer('Как будем лайкать?', reply_markup=like_menu_buttons)


# async def run_ig_side(func, *args):
#     loop = asyncio.get_running_loop()
#     with concurrent.futures.ThreadPoolExecutor() as pool:
#         result = await loop.run_in_executor(
#             pool, func, *args
#         )
#     return result
#
# @dp.message_handler(state=LikeState.Li4)
# async def taking_datas_for_likes(message: types.Message, state: FSMContext):
#     hashtags_list = message.text.split(' ')
#     tg_id = message.from_user.id
#     login = (await state.get_data()).get('login')
#     await state.finish()
#     await message.answer('Запущен алгоритм лайков по локации и хэштегам с аккаунта', login)
