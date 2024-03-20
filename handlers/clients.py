from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import dp, bot
from keybords.client_kb import start_markup, register_start__markup, lenguage_markup, start_user_markup, like_markup
from database.bot_db import sql_create
from database.bot_db import sql_command_random, sql_command_find, sql_command_find2, sql_name_update, sql_photo_update
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def on_startup(_):
    sql_create()
    await bot.send_message(chat_id=5257782766, text='бот запущен')


async def on_shutdown(_):
    # chat_id = -4107009129
    chat_id = 5257782766
    await bot.send_message(chat_id, "Ужс устал, я спать.")

# @dp.message_handler(commands=['/registration'])
#


@dp.message_handler(lambda message: message.text == '💤')
async def sleep(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='давайте подождем пока кто то вас не лайкнет')
    await bot.send_message(chat_id=message.chat.id, text='1. Смотреть анкеты.\n'
                                                         '2. Моя анкета.\n'
                                                         '3. Я больше не хочу никого искать.\n'
                                                         '***\n'
                                                         '4. Пригласи друзей - получи больше лайков 😎.',
                                                    reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,row_width=4).add(KeyboardButton('1 🚀'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('4')))


@dp.message_handler(lambda message: message.text == '1.1')
async def reregistration(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='заполните анкету заново', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False).add(KeyboardButton('reregistration')))


@dp.message_handler(lambda message: message.text == '/myprofile' or message.text == '🇷🇺 русский' or message.text == '2')
async def my_profile(message: types.Message):
    result = await sql_command_find(message)
    if result:
        await message.answer('Так выглядит твоя анкета: ')
        await sql_command_find2(message)
        await bot.send_message(
            chat_id=message.chat.id,
            text="1.1. Заполнить анкету заново.\n"
                 "2. Изменить фото/видео.\n"
                 "3. Изменить имя анкеты.\n"
                 "4. Привязка age.\n"
                 "5. Смотреть анкеты.",
            reply_markup=register_start__markup
        )
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('registration'))

        # Отправка сообщения без текста, только с клавиатурой
        await bot.send_message(chat_id=message.chat.id, text='давайте зарегистрируемся', reply_markup=keyboard)


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    if message.from_user.id == 52577827664:

        await bot.send_message(chat_id=message.chat.id,
                               text=f'Салам хозяин {message.from_user.first_name}',reply_markup=start_markup)
    else:
        await bot.send_message(chat_id=message.chat.id, text=f'Привет!')
        result = await sql_command_find(message)
        if result:
            await bot.send_message(chat_id=message.chat.id, text='выберите язык', reply_markup=lenguage_markup)
        else:
            await bot.send_message(message.from_user.id, "выберите функционал: ", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False).add(KeyboardButton('registration')))


@dp.message_handler(commands=['info'])
async def info_handler(message: types.Message):
    await message.reply('Сам разбирайся')


@dp.message_handler(commands=['quiz'])
async def quiz_command(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('100%', callback_data='answer_1')
    button_2 = InlineKeyboardButton('Не уверен(а)', callback_data='answer_2')
    markup.add(button_1, button_2)

    question = "Какой процент твоей любви к Тиме?"
    await message.answer(question, reply_markup=markup)


@dp.message_handler(commands=['quiz2'])
async def quiz2_command(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('легенды питона', callback_data='channel_legends_of_python')
    button_2 = InlineKeyboardButton('bots_chanel', callback_data='channel_bots_channel')
    markup.add(button_1, button_2)
    await bot.send_message(chat_id=message.chat.id, text='Выберите канал для отправки опроса:', reply_markup=markup)


@dp.message_handler(lambda message: message.text == '/get' or message.text == '🚀 5' or message.text == '❤️' or message.text == '👎' or message.text == '1 🚀')
async def get_user(message: types.Message):
    print('get')
    await bot.send_message(chat_id=message.from_user.id, text = '✨🔍', reply_markup=like_markup)
    await sql_command_random(message)


def register_handler_clients(dp: Dispatcher):
    dp.register_message_handler(start_handler)
    dp.register_message_handler(info_handler)
    dp.register_message_handler(quiz_command)
    dp.register_message_handler(quiz2_command)
    dp.register_message_handler(get_user)




