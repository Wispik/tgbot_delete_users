from aiogram.utils.helper import Helper, HelperMode, Item


class AppStates(Helper):
    mode = HelperMode.snake_case

    STATE_WAIT_CHANNEL_ID = Item()
    STATE_WAIT_CHANNEL_TG_ID = Item()
    STATE_WAIT_CHANNEL_LINK = Item()