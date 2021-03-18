import time

import schedule

from utils.set_bot_commands import set_default_commands
from loader import db


async def on_startup(dp):
    """
    algorithm to be done on start
    """
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)

    # try:
    #     db.create_users_tg()
    # except:
    #     pass
    try:
        db.create_users_ig()
    except:
        pass


def global_membership_check():
    """
    checks purchase ending
    """
    db.global_check()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)

schedule.every().days.do(global_membership_check)

while True:
    schedule.run_pending()
    time.sleep(80000)
