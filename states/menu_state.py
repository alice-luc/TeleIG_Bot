from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuState(StatesGroup):
    """
    'menu state' is being used to set a state when consumer chooses the options
    """

    M1 = State()
    M2 = State()


