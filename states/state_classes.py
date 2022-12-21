from aiogram.dispatcher.filters.state import StatesGroup, State


class LoginState(StatesGroup):
    """
    Allows to track whether user is logged in
    """

    L2 = State()


class MenuState(StatesGroup):
    """
    Allows to set specific menu keyboards depending on stage
    M1 - check followers or give likes?
    M2 - when user chooses to check followers or to get statistics
    """

    M1 = State()
    M2 = State()


class LikeState(StatesGroup):
    """
    Allows to offer different options and keyboards to user
    Li1 - User decides what type of likes to perform
    Li2 - Likes of followers' followers list
    Li3 - Likes of hashtags
    """

    Li1 = State()
    Li2 = State()
    Li3 = State()


class CheckState(StatesGroup):
    """
    Allows to offer different options and keyboards to user
    C1 - requests user's username
    C2 - check who is not following back
    C3 - check whether there are bots in followers' list
    """
    C1 = State()
    C2 = State()
    C3 = State()


class TrialState(StatesGroup):
    """
    Allows user to user trial period
    """
    T1 = State()
