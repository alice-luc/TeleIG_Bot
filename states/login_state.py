from aiogram.dispatcher.filters.state import StatesGroup, State


class LoginState(StatesGroup):
    """
    'Login state' is being used to set a state on a certain IG-side option(log in)
    """

    L2 = State()

