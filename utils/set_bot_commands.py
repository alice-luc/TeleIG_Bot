from aiogram import types


async def set_default_commands(dp):
    """
    method sets the list of commands
    """
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запуск бота"),
        types.BotCommand("trial", "Начало пробной трехдневной версии"),
    ])

