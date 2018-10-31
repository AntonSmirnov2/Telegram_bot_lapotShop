import telebot
from config import TELE_BOT_TOKEN
from plugins.keyboards import db_queries_keyboard, main_keyboard
from plugins.check_db import change_session_status, general_product_request, general_user_request

bot = telebot.TeleBot(TELE_BOT_TOKEN)


@bot.message_handler(content_types='text')
def db_queries(message):
    chat_id = str(message.from_user.id)
    change_session_status(chat_id, 'RD')
    bot.send_message(chat_id, 'Выбери запрос (RD)', reply_markup=db_queries_keyboard())
    pass


@bot.message_handler(content_types=['text'])
def send_request(message):
    transaction_dict = {'Общая информация по товарам': general_product_request(),
                        'Общая информация по пользователям': general_user_request()}
    chat_id = str(message.from_user.id)
    message_text = str(message.text)

    if message_text in transaction_dict.keys():
        result = transaction_dict[message_text]
        change_session_status(chat_id, '')
        bot.send_message(chat_id, result, reply_markup=main_keyboard(message))
    else:
        change_session_status(chat_id, 'CANC')
        bot.send_message(chat_id, 'Отмена (RD)', reply_markup=main_keyboard(message))
