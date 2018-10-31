
from config import USER_IDS
from plugins.access_denied import access_denieded
from plugins.QR_code_decryption import QR_code_decryption, qr_code_registration
from plugins.sale_regist import sale_regist
from plugins.echo import echo
from plugins.info import info, contacts
from plugins.keyboards import main_keyboard
from plugins.check_db import main_user_info, get_session_status, change_session_status
from plugins.profile_editing import profile_editing, change_info
from plugins.db_queries import db_queries, send_request


def message_replier(messages):
    for message in messages:
        chat_id = str(message.from_user.id)
        user_name = str(message.chat.first_name)
        access_level = main_user_info(chat_id)['admitt_level']
        change_session_status(chat_id=chat_id, user_data=message.text)
        session_status = get_session_status(chat_id)

        # Проверка, имеет ли пользователь доступ к боту
        if chat_id not in USER_IDS:
            access_denieded(message)
            return

        # Если пользователь в процессе регистрации покупки или запроса информации из БД ПЕРЕПИСАТЬ ЧЕРЕЗ БД
        # if chat_id in users_in_session:
        #     sale_regist(message)
        #     return

        main_keyboard(message)

        if message.text in ('/start', '/help'):
            info(message)
            return

        # Функции бота при выборе с главной клавиатуры с проверкой уровня доступа
        if message.text == 'Помощь' and access_level in ['demo', 'seller', 'user', 'admin', 'creator']:
            message.text = '/help'
            info(message)
            return

        if message.text == 'Контакты' and access_level in ['demo', 'seller', 'user', 'admin', 'creator']:
            contacts(message)
            return

        if message.text == 'Редактировать профиль' and access_level in ['seller', 'user', 'admin', 'creator']:
            profile_editing(message)
            return

        if message.text == 'Запросы из БД' and access_level in ['user', 'admin', 'creator']:
            db_queries(message)
            return

        if message.text == 'Редактировать БД' and access_level in ['admin', 'creator']:
            pass

        if message.text == 'Секретные возможности создателя' and access_level in ['creator']:
            pass

        # Если пользователь прислал фото
        if message.content_type == 'photo' and access_level in ['seller', 'user', 'admin', 'creator']:
            decrypted_code = QR_code_decryption(message)
            return

        # Если пользователь в процессе получения/изменения хронимых данных
        if session_status[0]:
            if 'PE' in session_status[0]:
                change_info(message, session_status[0], session_status[1])
                return
            elif 'QR' in session_status[0]:
                qr_code_registration(message, action=session_status[1], qr_code=session_status[2])
            elif 'RD' in session_status[0]:
                send_request(message)
        # Когда ни один вариант не подходит отвечаем ЭХО-сообщением
        else:
            echo(message)
            return


def in_session():
    try:
        session_control = open('session_control.txt')
        session_control_content = session_control.read()
        session_control.close()
    except FileNotFoundError:
        session_control = open('session_control.txt', 'w')
        session_control_content = ''
        session_control.close()
    return session_control_content


def add_in_session(user_id, code):
    session_control = open('session_control.txt', 'a')
    session_control.write(f'{user_id}-{code}\n')
    session_control.close()

