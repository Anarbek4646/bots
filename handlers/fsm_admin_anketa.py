from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from config import bot, dp, new_admins
from aiogram.types import ContentTypes
from keybords.client_kb import gender_markup, location_markup,submit_markup, cancel_markup


class FsmAdminAnketa(StatesGroup):
    name = State()
    age = State()
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


@dp.message_handler(commands=['registrate_admin'])
async def registrate_admin_handler(message: types.Message, state: FSMContext):
    if message.chat.type == 'private' and message.from_user.id in new_admins:
        await FsmAdminAnketa.name.set()
        await message.answer('как звать?', reply_markup=cancel_markup)
    else:
        await message.answer('заполнение анкету только в личке', reply_markup=cancel_markup)


@dp.message_handler(state=FsmAdminAnketa.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[id] = message.from_user.id
        data['username'] = f'@{message.from_user.username}'
        data['name'] = message.text
    await FsmAdminAnketa.next()
    await message.answer('сколько лет?', reply_markup=cancel_markup)


@dp.message_handler(state=FsmAdminAnketa.age)
async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('пиши только число')
    elif int(message.text) < 5 or int(message.text) > 50:
        await message.answer('возрастное ограничение')
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FsmAdminAnketa.next()
        await message.answer("Все ли верно? Отправь 'Да' для подтверждения или 'Нет' для отмены.", reply_markup=submit_markup)


@dp.message_handler(state=FsmAdminAnketa.submit)
async def confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() not in ['да', 'нет']:
        await message.answer('выберите из варианта ниже')
    else:
        if message.text.lower() == 'да':

            await message.answer("Ты успешно зарегистрирован!", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer("Регистрация отменена.", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


def register_admin_handler(dp: Dispatcher):
    dp.register_message_handler(cancel_handler_command)
    dp.register_message_handler(cancel_handler_text)
