from aiogram.dispatcher.filters.state import StatesGroup, State


class TrialState(StatesGroup):
    """
    state is being used when a consumer chooses to run a trial subscription
    """
    T1 = State()
