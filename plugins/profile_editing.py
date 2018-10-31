import telebot
from config import TELE_BOT_TOKEN
from plugins.keyboards import profile_editing_keyboard, remove_keyboard, main_keyboard
from plugins.check_db import change_session_status, change_user_inf

bot = telebot.TeleBot(TELE_BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def profile_editing(message):
    chat_id = str(message.from_user.id)
    change_session_status(chat_id, 'PE')
    bot.send_message(chat_id, 'Что меняем? (PE)', reply_markup=profile_editing_keyboard())


@bot.message_handler(content_types=['text'])
def change_info(message, code, data):
    transaction_dict = {'Никнейм': 'name',
                        'Телефон': 'contact',
                        'Пароль': 'password'}
    chat_id = str(message.from_user.id)
    message_text = str(message.text)

    if message_text in transaction_dict.keys():
        change_session_status(chat_id, '-' + transaction_dict[message_text])
        bot.send_message(chat_id, f'Введите новый {message_text.lower()}', reply_markup=remove_keyboard())
    elif 'PE-' in code and ('name' or 'contact' or 'password' in code):
        code = code.split('-')[1]

        change_session_status(chat_id, 'CANC')
        change_user_inf(chat_id, code, data)
        bot.send_message(chat_id, 'Изменения внесены', reply_markup=main_keyboard(message))

    else:
        change_session_status(chat_id, 'CANC')
        bot.send_message(chat_id, 'Отмена изменений', reply_markup=main_keyboard(message))

    pass
