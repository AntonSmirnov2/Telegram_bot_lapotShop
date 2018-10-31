import telebot
from telebot import types
from config import TELE_BOT_TOKEN
from config import USER_IDS

bot = telebot.TeleBot(TELE_BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def sale_regist(message):
    # Извлекаем информацию о запросе (QR-код)
    code = extract_info(message.chat.id)

    # Регистрация продажи
    if message.text == 'Зарегистрировать продажу':
        answer = f'Продажа зарегистрирована.\nКод {code}\n\n(функционал не реализован, БД не создана)'

        # Уведомление прочих юзеров о регистрации продажи
        notify_list = notify_users(message.chat.id, USER_IDS)
        for user in notify_list:
            bot.send_message(user, f'Регистрация продажи от {message.chat.first_name}')

    # Запрос информации о товаре
    elif message.text == 'Показать информацию':
        answer = f'Информация о товаре.\nКод {code}\n\n(функционал не реализован, БД не создана)'

    # Если в процессе запроса возникла ошибка
    else:
        answer = 'Ошибка. sale_regist'

    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, answer, reply_markup=markup)


def extract_info(user_id):
    session_control = open('session_control.txt')
    session_control_content = session_control.read()
    session_control_content = session_control_content.split()
    session_control.close()

    product_code = 'Ошибка. sale_regist.extract_info'
    for ind, position in enumerate(session_control_content):
        if str(user_id) in position:
            product_code = position.split('-')[1]
            session_control_content.pop(ind)
            break

    session_control = open('session_control.txt', 'w')
    for position in session_control_content:
        session_control.write(position)
    session_control.close()
    return product_code


def notify_users(executor, user_ids):
    new_ids = []
    for user in user_ids:
        if user != executor:
            new_ids.append(user)
    return new_ids