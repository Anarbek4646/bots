from aiogram import types, Dispatcher
from config import bot, dp
from config import admin


@dp.message_handler(commands=['ban'], commands_prefix='!/')
async def ban(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in admin:
            await message.answer('ты не мой босс')
        elif not message.reply_to_message:
            await message.answer('команда должна быть ответом на сообщение!')
        else:
            await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.answer(f'{message.from_user.first_name}  братан кикнул'
                                 f'{message.reply_to_message.from_user.full_name}')

    else:
        await message.answer('пиши в группу')


@dp.message_handler(commands=['pin'], commands_prefix='!/')
async def pin(message: types.Message):
    print(message)
    if message.chat.type != 'private':
        await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    else:
        await message.answer('пиши в группу')


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(ban)
    dp.register_message_handler(pin)

