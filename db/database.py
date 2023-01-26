from datetime import datetime

from settings import db_connection, COLLECTION_ADMIN, COLLECTION_CHANNELS


async def get_admin_by_tg_id(tg_id: int):
    col = db_connection[COLLECTION_ADMIN]
    return await col.find_one(filter={'tg_id': tg_id})


async def create_channel(channel_id: int, tg_id: int, link: str):
    col = db_connection[COLLECTION_CHANNELS]
    await col.insert_one(
        {
            'channel_id': channel_id,
            'tg_id': tg_id,
            'link': link,
            'count_deleted_users': 0,
            'active': False,
            'start': None
        }
    )


async def get_channel_by_id(channel_id: int):
    col = db_connection[COLLECTION_CHANNELS]
    return await col.find_one({'channel_id': channel_id})


async def get_channel_by_tg_id(tg_id: int):
    col = db_connection[COLLECTION_CHANNELS]
    return await col.find_one({'tg_id': tg_id})


async def change_channel_status(channel_id: int, status: bool):
    col = db_connection[COLLECTION_CHANNELS]
    await col.find_one_and_update(
        {'channel_id': channel_id}, {"$set": {'active': status, 'start': datetime.now()}}
    )


async def change_channel_count_users(tg_id: int):
    col = db_connection[COLLECTION_CHANNELS]
    await col.find_one_and_update(
        {'tg_id': tg_id}, {"$inc": {'count_deleted_users': 1}}
    )


async def get_all_active_channels():
    col = db_connection[COLLECTION_CHANNELS]
    return await col.find({'active': True}).to_list(9999)


async def get_all_channels():
    col = db_connection[COLLECTION_CHANNELS]
    return await col.find({}).to_list(9999)
