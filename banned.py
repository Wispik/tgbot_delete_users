import asyncio

from pyrogram import Client
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus

import db.database as db
from settings import API_HASH, API_ID, WATCH_CHANNELS_DELAY, TOKEN_BANNED_BOT


async def watch_channels():
    async with Client("my_bot", api_hash=API_HASH, api_id=API_ID, bot_token=TOKEN_BANNED_BOT) as app:
        while True:
            try:
                all_channels = await db.get_all_active_channels()
                for channel in all_channels:
                    async for res in app.get_chat_members(channel['tg_id'], filter=ChatMembersFilter.RECENT, limit=20):
                        if res.status == ChatMemberStatus.MEMBER:
                            if res.joined_date > channel['start']:
                                await app.ban_chat_member(channel['tg_id'], res.user.id)
                                await db.change_channel_count_users(channel['tg_id'])
            except Exception as e:
                print(f'ERROR: {e}')
            await asyncio.sleep(WATCH_CHANNELS_DELAY)


async def run_watch_channels():
    loop = asyncio.get_event_loop()
    loop.create_task(watch_channels())
