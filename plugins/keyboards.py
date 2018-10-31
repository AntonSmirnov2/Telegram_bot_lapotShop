import telebot
from telebot import types
from config import TELE_BOT_TOKEN
from plugins.check_db import main_user_info

bot = telebot.TeleBot(TELE_BOT_TOKEN)


def main_keyboard(message):
    chat_id = str(message.from_user.id)
    user_admitt_level = main_user_info(chat_id)['admitt_level']
    # Admitt levels: 0 - demo; 1 - seller; 2 - user; 3 - admin; 4 - creator

    btn1 = types.KeyboardButton('Помощь')
    btn2 = types.KeyboardButton('Контакты')
    btn3 = types.KeyboardButton('Редактировать профиль')
    btn4 = types.KeyboardButton('Запросы из БД')
    btn5 = types.KeyboardButton('Редактировать БД')
    btn6 = types.KeyboardButton('Секретные возможности создателя')

    if user_admitt_level == 'demo':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=1)
        markup.add(btn1, btn2)
    elif user_admitt_level == 'seller':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2)
        markup.add(btn1, btn2, btn3)
    elif user_admitt_level == 'user':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2)
        markup.add(btn1, btn2, btn3, btn4)
    elif user_admitt_level == 'admin':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2)
        markup.add(btn1, btn2, btn3, btn4, btn5)
    elif user_admitt_level == 'creator':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2)
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=1)
        markup.add(btn1, btn2)
    return markup


def profile_editing_keyboard():
    btn1 = types.KeyboardButton('Никнейм')
    btn2 = types.KeyboardButton('Телефон')
    btn3 = types.KeyboardButton('Пароль')
    btn4 = types.KeyboardButton('Отмена')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2)
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def remove_keyboard():
    markup = types.ReplyKeyboardRemove()
    return markup


def qr_code_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Зарегистрировать продажу')
    btn2 = types.KeyboardButton('Показать информацию')
    markup.add(btn1, btn2)
    return markup


def db_queries_keyboard():
    btn1 = types.KeyboardButton('Общая информация по товарам')
    btn2 = types.KeyboardButton('Общая информация по пользователям')
    btn3 = types.KeyboardButton('Отмена')
    btn4 = types.KeyboardButton('(Пусто)')
    btn5 = types.KeyboardButton('(Пусто)')
    btn6 = types.KeyboardButton('(Пусто)')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=1)
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup
