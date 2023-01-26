from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup,\
                            ReplyKeyboardMarkup, KeyboardButton


kb_main = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Добавить канал')],
        [KeyboardButton('Информация')]
    ], resize_keyboard=True
)


def kb_channels(channels):
    kb = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        kb.add(
            InlineKeyboardButton(
                f"{channel['channel_id']} {channel['link']}",
                callback_data=f"stats_{channel['channel_id']}"
            )
        )
    return kb

def kb_change_channel_active(channel_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton('Включить', callback_data=f'status_active_{channel_id}'))
    kb.add(InlineKeyboardButton('Выключить', callback_data=f'status_disable_{channel_id}'))
    return kb
