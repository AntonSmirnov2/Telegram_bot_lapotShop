import telebot
from config import TELE_BOT_TOKEN
import requests
from plugins.proxy_setup import PROXIES_LST
from telebot import types
from pyzbar.pyzbar import decode
from PIL import Image
from plugins.keyboards import qr_code_keyboard, main_keyboard
from plugins.check_db import change_session_status, qr_code_check, sale_registration

bot = telebot.TeleBot(TELE_BOT_TOKEN)


def decrypt(path):
    im = Image.open(path)
    qr_content = decode(im)
    if qr_content != []:
        qr_content = qr_content[0][0].decode('utf-8')
    else:
        qr_content = 'Код не распознан.'
    return qr_content


def download_photo(message):
    fileID = message.photo[-1].file_id
    file = bot.get_file(fileID)
    photo_URL = rf'https://api.telegram.org/file/bot{TELE_BOT_TOKEN}/{file.file_path}'

    photo = requests.get(photo_URL, proxies={'https': 'socks5://5.135.20.158:8080'})

    f = open(rf'users_files\photo_chatID{message.chat.id}_from_{message.chat.first_name}.jpg', 'wb')
    f.write(photo.content)
    f.close()
    path_to_photo = rf'users_files\photo_chatID{message.chat.id}_from_{message.chat.first_name}.jpg'
    return path_to_photo


@bot.message_handler(content_types='photo')
def QR_code_decryption(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Получил фото.')
    qr_code_pic = download_photo(message)
    answer = decrypt(qr_code_pic)

    if answer == 'Код не распознан.':
        bot.send_message(chat_id, answer)
        return False
    else:
        answer = answer.split()[0]
        if qr_code_check(answer):
            bot.send_message(chat_id, 'Код распознан, выбери действие:', reply_markup=qr_code_keyboard())
            change_session_status(chat_id, 'QR', user_data='', qr_code=answer)
        else:
            bot.send_message(chat_id, f'В базе данных отсутствует информация по этому коду:\n'
                                      f'{answer}',
                             reply_markup=main_keyboard(message))
            change_session_status(chat_id, 'CANC')
        return answer


@bot.message_handler(content_types='text')
def qr_code_registration(message, qr_code, action):
    chat_id = message.chat.id
    if action == 'Зарегистрировать продажу':
        sale_registration(qr_code)
        bot.send_message(chat_id, 'Продажа зарегистрирована, спасибо, секси:)', reply_markup=main_keyboard(message))
    elif action == 'Показать информацию':
        product_info = qr_code_check(qr_code)
        product_info = [i for i in product_info[0]]
        bot.send_message(chat_id, f'ID: {product_info[0]}\n'
                                  f'Name: {product_info[2]}\n'
                                  f'PPrice: {product_info[3]}\n'
                                  f'SPrice: {product_info[4]}\n'
                                  f'Status: {product_info[5]}',
                         reply_markup=main_keyboard(message))
    change_session_status(chat_id, 'CANC')
    pass
