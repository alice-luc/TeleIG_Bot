import time

import schedule

from utils.set_bot_commands import set_default_commands
from loader import data_base


async def on_startup(dispatcher):
    """
    algorithm to be done on start
    """
    import filters
    import middlewares
    filters.setup(dispatcher)
    middlewares.setup(dispatcher)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)

    try:
        data_base.create_users_ig()
    except Exception as error:
        print(error)


def global_membership_check():
    """
    checks purchase ending
    """
    data_base.global_check()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dispatcher

    executor.start_polling(dispatcher, on_startup=on_startup)

schedule.every().days.do(global_membership_check)

while True:
    schedule.run_pending()
    time.sleep(80000)
