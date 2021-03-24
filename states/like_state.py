from aiogram.dispatcher.filters.state import StatesGroup, State


class LikeState(StatesGroup):
    """
    'Like state' is being used to set a state on a certain IG-side option(like friends, etc)
    """

    Li1 = State()
    Li2 = State()
    Li3 = State()

