import telebot
from config import TELE_BOT_TOKEN
from plugins.check_db import main_user_info, admins_contact
from plugins.keyboards import main_keyboard

bot = telebot.TeleBot(TELE_BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def info(message):

    chat_id = str(message.from_user.id)
    user_name = str(message.chat.first_name)
    user_data = main_user_info(chat_id)
    markup = main_keyboard(message)

    if message.text == '/start':
        if user_data['admitt_level'] == 'creator':
            bot.send_message(chat_id, "Привет Создатель!;)))\n"
                                      f"\n"
                                      f"Никнэйм - {user_data['name']}\n"
                                      f"Контакт - {user_data['phone']}\n"
                                      f"Пароль  - {user_data['password']}\n"
                                      f"Допуск  - {user_data['admitt_level']}\n",
                             reply_markup=markup)
        else:
            bot.send_message(chat_id, f"Привет, {user_name}!\n"
                                      f"Хорошо, что ты с нами:) Твои данные:\n"
                                      f"\n"
                                      f"Никнэйм - {user_data['name']}\n"
                                      f"Контакт - {user_data['phone']}\n"
                                      f"Пароль  - {user_data['password']}\n"
                                      f"Допуск  - {user_data['admitt_level']}\n"
                                      f"\n"
                                      f"Чтобы узнать о моих возможностях отправь команду /help.",
                             reply_markup=markup)
    elif message.text == '/help':
        bot.send_message(chat_id, f"Как пользоваться:\n"
                                  f"Чтобы зарегистрировать продажу или получить информацию о товаре"
                                  f" отправь мне фото QR-кода с упаковки. Я его расшифрую и предложу"
                                  f" действия на выбор.\n"
                                  f"Так же тебе доступны действия на клавиатуре.",
                         reply_markup=markup)


@bot.message_handler(content_types=['text'])
def contacts(message):
    chat_id = str(message.from_user.id)

    reply_message = 'По любым вопросам обращайтесь по номерам:\n'
    for item in admins_contact():
        reply_message += f'{str(item[1])} {str(item[0])}\n'

    bot.send_message(chat_id, reply_message)
