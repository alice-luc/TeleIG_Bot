from aiogram.dispatcher.filters.state import StatesGroup, State


class CheckState(StatesGroup):
    """
    'check state' is being used to set a state on a certain IG-side option(check followers, etc)
    """
    C1 = State()
    C2 = State()
    C3 = State()

