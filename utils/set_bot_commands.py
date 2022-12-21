from aiogram import types, Dispatcher


async def set_default_commands(dispatcher: Dispatcher):
    """
    method sets the list of commands
    """
    await dispatcher.bot.set_my_commands([
        types.BotCommand("start", "Запуск бота"),
        types.BotCommand("trial", "Начало пробной трехдневной версии"),
    ])

