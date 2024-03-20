from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import dp, bot


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('answer_'))
async def answer_callback_query(callback_query: types.CallbackQuery):
    # Здесь мы отправляем сообщение непосредственно после выбора ответа пользователем
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == 'answer_1':
        await bot.send_message(callback_query.message.chat.id, f'бооже {callback_query.from_user.first_name} не уважает себя')
    else:
        await bot.send_message(callback_query.message.chat.id, f'бооже {callback_query.from_user.first_name}  не уверен(а) в себе')

    # question = "процент твоей любви к Тиме"
    # answers = [
    #     '100%',
    #     '100%',
    # ]
    #
    # if message.chat.id == 5257782766:
    #
    #         chat_id=-1002042123398,
    #         # chat_id=message.from_user.id,
    #         question=question,
    #         options=answers,
    #         is_anonymous=False,
    #         # type = 'quiz',
    #         # correct_option_id=0,
    #         # explanation='стыдно за такую любовь',
    #         # open_period=10,
    #         reply_markup=murkup2,
    #     )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('channel_'))
async def send_quiz_to_channel(callback_query: types.CallbackQuery):

    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton('NEXT', callback_data='button_call_1')
    markup.add(button_call_1)

    await bot.answer_callback_query(callback_query.id)
    channel_id = None

    # Определяем ID канала в зависимости от выбора пользователя
    if callback_query.data == 'channel_legends_of_python':
        channel_id = -1002042123398  # Пример ID канала "Легенды Питона"
        response_text = 'Тест отправлен в Легенды Питона.'
    elif callback_query.data == 'channel_bots_channel':
        channel_id = -1002056807462  # Пример ID другого канала
        response_text = 'Тест отправлен в Bots Channel.'

    # Отправляем сообщение пользователю об успешном выборе
    await bot.send_message(callback_query.message.chat.id, response_text)

    # Теперь можно отправить опрос в выбранный канал
    if channel_id:
        question = "Процент твоей любви к Тиме"
        answers = ['100%', '100%']
        await bot.send_poll(
            chat_id=channel_id,
            question=question,
            options=answers,
            is_anonymous=False,

            reply_markup=markup
        )


allowed_user_id = 5257782766


@dp.callback_query_handler(text='button_call_1')
async def quiz_2(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != allowed_user_id:
        await bot.answer_callback_query(callback_query.id, text="У вас нет доступа к этой кнопке", show_alert=True)
        return
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton('NEXT', callback_data='button_call_2')
    markup.add(button_call_1)

    question = "что такое доброта?"
    answers = [
        'Anarbek',
        'Bolot',
        'Адольф Гитлер'
    ]

    await bot.send_poll(
        chat_id=callback_query.message.chat.id,
        # chat_id=-1002042123398,
        # chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type = 'quiz',
        correct_option_id=0,
        explanation='боооже чел как можно не знать',
        open_period=10,
        reply_markup=markup
    )


@dp.callback_query_handler(text='button_call_2')
async def quiz_3(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != allowed_user_id:
        await bot.answer_callback_query(callback_query.id, text="У вас нет доступа к этой кнопке", show_alert=True)
        return
    question = "когда открыли Америку?"
    answers = [
        '1492',
        '1439',
        '1380',
        '1389',
    ]
    photo = open('/home/anarbek/Desktop/oop/git_project/bots/media/cat.jpg', 'rb')
    await bot.send_photo(callback_query.message.chat.id, photo)
    await bot.send_poll(
        chat_id=callback_query.message.chat.id,
        # chat_id=-1002042123398,
        # chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation='боже чел ты такой не умный',
        open_period=10,
    )


def register_handler_callback(dp: Dispatcher):
    dp.register_message_handler(answer_callback_query)
    dp.register_message_handler(send_quiz_to_channel)
    dp.register_message_handler(quiz_2)
    dp.register_message_handler(quiz_3)

