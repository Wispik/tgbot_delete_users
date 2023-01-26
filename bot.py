from aiogram.utils import executor

from handlers import setup_handlers
from settings import dp
import middleware
from banned import run_watch_channels


def on_startup():
    setup_handlers(dp)


async def run_watch(_):
    await run_watch_channels()


if __name__ == '__main__':
    on_startup()
    dp.middleware.setup(middleware.UserIsAdminMiddleware())

    executor.start_polling(dp, on_startup=run_watch)
