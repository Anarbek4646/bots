from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
start_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=3
)


gender_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=3
)

location_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
)

submit_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
).add(KeyboardButton('да'), KeyboardButton('нет'))

cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
)
lenguage_markup = ReplyKeyboardMarkup(
    resize_keyboard=True
).add(KeyboardButton('🇷🇺 русский'))

register_start__markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    row_width=5
).add(KeyboardButton('1.1'),KeyboardButton('2'),KeyboardButton('3'),KeyboardButton('4'),KeyboardButton('🚀 5'))

like_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=4
).add(KeyboardButton('❤️'), KeyboardButton('💌 / 📹'), KeyboardButton('👎'), KeyboardButton('💤'))


start_user_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('start'))


cancel_button = KeyboardButton('cancel')

start_button = KeyboardButton('/start')
info_button = KeyboardButton('/info')
help_button = KeyboardButton('/help')
share_location = KeyboardButton('Share location', request_location=True)
share_contact = KeyboardButton('Share contact', request_contact=True)
register_button = KeyboardButton('/reg')

male_gender = KeyboardButton('я парень')
female_gender = KeyboardButton('я девушка')
none_gender = KeyboardButton('хз')

cancel_markup.add(cancel_button)

location_markup.add(share_location, cancel_button)

gender_markup.add(male_gender, female_gender, none_gender, cancel_button)

start_markup.add(start_button, info_button, help_button, share_location, share_contact, register_button)
