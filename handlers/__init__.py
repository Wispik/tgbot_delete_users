from aiogram import Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher.filters import Text

import handlers.admin as h

from states import AppStates


def setup_handlers(dp: Dispatcher):
    dp.register_message_handler(h.start_command, commands=['start'], state=['*'])

    dp.register_message_handler(h.add_channel_step1_command, Text('Добавить канал'))
    dp.register_message_handler(h.add_channel_step2_command, state=[AppStates.STATE_WAIT_CHANNEL_ID], regexp=r"\d+")
    dp.register_message_handler(h.add_channel_step3_command, state=[AppStates.STATE_WAIT_CHANNEL_TG_ID], regexp=r"\d+")
    dp.register_message_handler(h.add_channel_step4_command, state=[AppStates.STATE_WAIT_CHANNEL_LINK])

    dp.register_message_handler(h.information_command, Text('Информация'))

    dp.register_callback_query_handler(h.channel_info_callback, Text(startswith="stats_"))
    dp.register_callback_query_handler(h.channel_change_status_callback, Text(startswith="status_"))

