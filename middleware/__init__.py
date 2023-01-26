from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

import db.database as db


class UserIsAdminMiddleware(BaseMiddleware):
    '''
    Проверяем, админ ли юзер
    '''

    def __init__(self):
        super(UserIsAdminMiddleware, self).__init__()
    
    async def on_process_message(self, message: types.Message, data: dict):
        admin = await db.get_admin_by_tg_id(message.from_user.id)
        if admin:
            return
        else:
          raise CancelHandler()