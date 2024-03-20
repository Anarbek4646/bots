from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, dp
from aiogram.types import ContentTypes
from keybords.client_kb import gender_markup, location_markup,submit_markup, cancel_markup, lenguage_markup
from database.bot_db import sql_command_insert, sql_command_find, sql_command_delete


class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    gender = State()
    region = State()
    photo = State()
    submit = State()


@dp.message_handler(state="*", commands='cancel')
async def cancel_handler_command(message: types.Message, state: FSMContext):
    await cancel_handler_logic(message, state)


@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler_text(message: types.Message, state: FSMContext):
    await cancel_handler_logic(message, state)


async def cancel_handler_logic(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Регистрация отменена.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'registration')
async def fsm_start(message: types.Message):

    if message.chat.type == 'private':
        result = await sql_command_find(message)
        if not result:
            await FSMAdmin.name.set()
            await message.answer('как звать?', reply_markup=cancel_markup)
        else:
            await message.answer('выберите язык?', reply_markup=lenguage_markup)

    else:
        await message.answer('заполнение анкету только в личке')


@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f'@{message.from_user.username}'
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('сколько лет?', reply_markup=cancel_markup)


@dp.message_handler(state=FSMAdmin.age)
async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('пиши только число')
    elif int(message.text) < 5 or int(message.text) > 50:
        await message.answer('возрастное ограничение')
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("Какого ты пола?")
        await bot.send_message(message.chat.id, "Выбери свой пол:", reply_markup=gender_markup)


# @dp.message_handler(state=FSMAdmin.gender)
async def load_gender(message: types.Message, state: FSMContext):
    if message.text not in ['я парень', 'я девушка', 'хз']:
        await message.answer('выберите из варианта')
    else:
        async with state.proxy() as data:
            if message.text == 'я парень':
                data['gender'] = 'male'
            elif message.text == 'я девушка':
                data['gender'] = 'female'
            else:
                data['gender'] = 'оно'
        await FSMAdmin.next()
        await message.answer("Из какого ты региона?")
        await bot.send_message(message.chat.id, 'отправьте свою локацию или напишите город', reply_markup=location_markup)


@dp.message_handler(state=FSMAdmin.region)
async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
    await FSMAdmin.next()
    await message.answer("Пришли свою фотографию")


# Load photo
@dp.message_handler(content_types=ContentTypes.PHOTO, state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Assuming you're saving the file_id of the photo
        data['photo'] = message.photo[0].file_id
        await message.answer_photo(data['photo'],
                                   caption=f'{data["name"]} {data["age"]} {data["gender"]} {data["region"]} {data["username"]}')
    await FSMAdmin.next()
    await message.answer("Все ли верно? Отправь 'Да' для подтверждения или 'Нет' для отмены.", reply_markup=submit_markup)


@dp.message_handler(state=FSMAdmin.submit)
async def confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() not in ['да', 'нет']:
        await message.answer('выберите из варианта ниже')
    else:
        if message.text.lower() == 'да':
            await sql_command_insert(state)
            await state.finish()
            await message.answer("Ты успешно зарегистрирован!", reply_markup=types.ReplyKeyboardRemove())

        else:
            await message.answer("Регистрация отменена.", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel_handler_command)
    dp.register_message_handler(cancel_handler_text)
    dp.register_message_handler(fsm_start)
    dp.register_message_handler(load_name)
    dp.register_message_handler(load_age)
    dp.register_message_handler(load_gender, state=FSMAdmin.gender)
    dp.register_message_handler(load_region)
    dp.register_message_handler(load_photo)
    dp.register_message_handler(confirmation)

