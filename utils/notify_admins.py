# import logging

from aiogram import Dispatcher

from data.config import admins


async def on_startup_notify(dp: Dispatcher):
    """
    notifies the owner when bot restarts
    """
    for admin in admins:
        try:
            await dp.bot.send_message(admin, 'Bot was reran')

        except Exception as err:
            pass
            # logging.exception(err)


async def membership_notify(dp: Dispatcher, login, tg_id):
    """
    notifies the owner when someone has registered its new acc
    """
    for admin in admins:
        try:
            await dp.bot.send_message(admin, f'new user, {login}, {tg_id}')
        except Exception as err:
            pass
            # logging.exception(err)


async def errors_notify(dp: Dispatcher, tg_id, login):
    """
    notifies the owner when someone has registered its new acc
    """
    for admin in admins:
        try:
            await dp.bot.send_message(admin, f'error has appeared {tg_id}, {login}')
        except Exception as err:
            pass
            # logging.exception(err)
