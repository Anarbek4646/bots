from aiogram import types, Dispatcher
from config import dp, bot, admin
from random import choice

value = {}


@dp.message_handler()
async def get_id(message: types.Message):
    global value
    print(message)
    print((admin))
    if message.chat.type != 'private':
        bad_words = ['java', 'html', 'дурак', 'дебик']
        for word in bad_words:
            if word in message.text.lower():

                await message.reply(f'сам ты дурак {message.from_user.first_name}')
                print(message)
                await bot.delete_message(message.chat.id, message.message_id)
    if message.text.startswith('.'):
        await bot.pin_chat_message(message.chat.id, message.message_id)

    if message.text == 'dice':
        await bot.send_dice(message.chat.id, emoji='🎳')
    if message.text == 'game' and message.from_user.first_name not in value:
        games = ['🎰', '🎲', '🎯', '⚽️', '🏀', '🎳']
        res = await bot.send_dice(message.chat.id, emoji=games[1])

        value[message.from_user.first_name] = res.dice.value
    elif message.text == 'result':
        key_with_max_value = max(value, key=value.get)
        max_value = value[key_with_max_value]
        await bot.send_message(message.from_user.id, text=f"выйграл: {key_with_max_value}, очко: {max_value}")
    elif message.from_user.first_name in value and message.text == 'game':
        await message.answer('вы уже кидали')
    elif message.text == 'clear':
        value = {}

    elif message.text == 'game' and message.from_user.first_name not in value:
        games = ['🎰', '🎲', '🎯', '⚽️', '🏀', '🎳']
        res = await bot.send_dice(message.chat.id, emoji=games[1])
        value[message.from_user.first_name] = res.dice.value


def registrate_handler_extra(dp: Dispatcher):
    dp.register_message_handler(get_id)
