from aiogram import types
from aiogram.dispatcher import FSMContext

import db.database as db
from states import AppStates
from settings import bot
import keyboards as kb


async def start_command(
    message: types.Message,
    state: FSMContext
):
    await state.reset_data()
    await state.reset_state()

    await message.answer('Выберите действие:', reply_markup=kb.kb_main)


async def add_channel_step1_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_state(AppStates.STATE_WAIT_CHANNEL_ID)
    await message.answer('Введите ID канала')


async def add_channel_step2_command(
    message: types.Message,
    state: FSMContext
):
    await state.set_data({'channel_id': int(message.text)})
    await state.set_state(AppStates.STATE_WAIT_CHANNEL_TG_ID)
    await message.answer('Введите JSON ID канала')


async def add_channel_step3_command(
    message: types.Message,
    state: FSMContext
):
    _channel = await db.get_channel_by_tg_id(int(message.text))
    if _channel:
        await message.answer(f'Канал JSON ID: {message.text} уже есть в базе')
        return
    await state.update_data({'tg_id': int(message.text)})
    await state.set_state(AppStates.STATE_WAIT_CHANNEL_LINK)
    await message.answer('Введите ссылку канала')


async def add_channel_step4_command(
    message: types.Message,
    state: FSMContext
):
    state_data = await state.get_data()
    await db.create_channel(
        state_data['channel_id'],
        state_data['tg_id'],
        message.text,
    )
    await message.answer(f"Канал ID: {state_data['channel_id']} LINK: {message.text} - добавлен!")
    await state.reset_data()
    await state.reset_state()


async def information_command(
    message: types.Message
):
    channels = await db.get_all_channels()
    _kb = kb.kb_channels(channels)
    await message.answer('Список каналов:', reply_markup=_kb)


async def channel_info_callback(
    callback_query: types.CallbackQuery
):
    channel_id = int(callback_query.data.split('_')[1])
    channel = await db.get_channel_by_id(channel_id)
    text = f"""
        {channel_id} {channel['link']}\nСтатус: {'❇️ Активна' if channel['active'] else '🛑 Не активна '}\nРезультат: {channel['count_deleted_users']} удаленных подписчиков
    """
    await bot.send_message(
        callback_query.message.chat.id,
        text,
        reply_markup=kb.kb_change_channel_active(channel_id)
    )
    print(channel['start'])


async def channel_change_status_callback(
    callback_query: types.CallbackQuery
):
    channel_id = int(callback_query.data.split('_')[2])
    new_status = callback_query.data.split('_')[1] == 'active'
    await db.change_channel_status(channel_id, new_status)
    await bot.send_message(callback_query.message.chat.id, 'Статус изменен!')
