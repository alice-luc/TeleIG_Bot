from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from keyboards import insta_menu_buttons, menu_buttons, start_menu_buttons
from states import MenuState
from utils.misc import rate_limit


@rate_limit(5, 'Меню')
@dp.message_handler(text="Меню")
async def show_menu(message: types.Message):
    """
    returns menu buttons to be chosen
    """
    await message.answer('Выберите действие', reply_markup=menu_buttons)
    await MenuState.M1.set()


@rate_limit(5, 'Продвигать Instagram-аккаунт')
@dp.message_handler(state=MenuState.M1, text='Продвигать инстаграм аккаунт')
async def insta_choice(message: types.Message):
    """
    returns insta options keyboard
    """
    await MenuState.M2.set()
    await message.answer('Что мне делать?', reply_markup=insta_menu_buttons)


@rate_limit(1, 'Назад')
@dp.message_handler(state=MenuState.M1, text='Назад')
async def back_activating(message: types.Message, state: FSMContext):
    """
    returns None of states and none of keyboards
    """
    await state.finish()
    await message.answer('Выбери действие', reply_markup=start_menu_buttons)


@rate_limit(60, 'Посмотреть статистику')
@dp.message_handler(state=MenuState.M1, text='Посмотреть статистику')
async def statistic(message: types.Message):
    """
    NEEDS TO BE FIXED
    returns statistic of serving insta accounts registered by current user

    """
    tg_id = message.from_user.id
    tg_username = message.from_user.username
    accs_row = db.check_accounts(tg_id, tg_username)
    if len(accs_row) == 1:
        accs = ['Ник'+': '+str(accs_row[0]), 'Дата истечения подписки'+': '+str(accs_row[1])]
    elif len(accs_row) > 1:
        accs = []
        iteration = 1
        for acc in accs_row:
            if iteration % 2 == 1:
                updating = 'Ник'+': '+str(acc)
                iteration += 1
            elif iteration % 2 == 0:
                updating = 'Подписка истекает'+': '+str(acc)+'\n'
                iteration += 1
            accs.append(updating)
    else:
        accs = accs_row
    await message.answer('\n'.join(accs), reply_markup=menu_buttons)
