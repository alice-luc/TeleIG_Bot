from data.config import admins
from ..users import notifying
from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted, BadRequest)

    if isinstance(exception, CantDemoteChatCreator):
        await notifying(admins[0], 'Cant demote chat creator')
        return True

    if isinstance(exception, MessageNotModified):
        await notifying(admins[0], 'Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        await notifying(admins[0], 'Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        await notifying(admins[0], 'Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        await notifying(admins[0], 'MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        await notifying(admins[0], f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        await notifying(admins[0], f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        await notifying(admins[0], f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        await notifying(admins[0], f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        await notifying(admins[0], f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, BadRequest):
        await notifying(admins[0], f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    await notifying(admins[0], f'Update: {update} \n{exception}')
