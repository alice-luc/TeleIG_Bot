# import logging

from aiogram import Dispatcher

from data.config import admins


async def on_startup_notify(dispatcher: Dispatcher):
    """
    notifies the owner when the bot's got restarted
    """
    for admin in admins:
        try:
            await dispatcher.bot.send_message(admin, 'Bot was reran')

        except Exception as err:
            pass
            # logging.exception(err)


async def membership_notify(dispatcher: Dispatcher, login, tg_id):
    """
    notifies the owner when someone has registered his new acc
    """
    for admin in admins:
        try:
            await dispatcher.bot.send_message(admin, f'new user, {login}, {tg_id}')
        except Exception as err:
            pass
            # logging.exception(err)


async def errors_notify(dispatcher: Dispatcher, tg_id, login):
    """
    notifies owner when something went wrong(instead of logging
    """
    for admin in admins:
        try:
            await dispatcher.bot.send_message(admin, f'error has appeared {tg_id}, {login}')
        except Exception as err:
            pass
            # logging.exception(err)
