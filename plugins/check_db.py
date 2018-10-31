import sqlite3
import datetime
# from config import DB_NAME

DB_NAME = 'lapotshop.sqlite'


def check_db_exist():
    print('Проверка базы данных на существование...', end=' ')
    try:
        connect = sqlite3.connect(DB_NAME)
        cursor = connect.cursor()
        cursor.execute("""
        SELECT count(id_product) as num
        FROM product
        """)
        connect.close()
    except sqlite3.OperationalError:
        print('БД не найдена или повреждена. Создание новой...', end=' ')
        create_db()
        print('Выполнено.')
        return False
    print('ОК')
    return True


def create_db():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.executescript('''
    CREATE TABLE product         (id_product TEXT, id_product_group TEXT, name TEXT, 
                                  purchase_price REAL, selling_price REAL, status TEXT, 
                                  info TEXT, pic TEXT);
    CREATE TABLE product_group   (id_product_group INTEGER, group_name TEXT);
    CREATE TABLE product_hist    (id_product INTEGER, status TEXT, date TEXT);
    CREATE TABLE user            (id_user INTEGER, id_telegram TEXT, password TEXT, name TEXT,
                                  contact TEXT, admitt_level TEXT);
    CREATE TABLE session         (id_telegram TEXT, status TEXT, data TEXT, date_time TEXT, qr_code TEXT);
    CREATE TABLE strangers       (id_telegram TEXT, name TEXT, date_time TEXT);
    ''')
    default_users = [
        (1, '401814822', 'toor', 'Anton', '+7-953-799-3236', 'creator'),
        (2, '113391194', 'toor', 'Nikita', 'NULL', 'admin'),
        (3, '541451816', 'toor', 'Валерий', 'NULL', 'demo'),
        (4, '197974521', 'toor', 'Даниил', '+7-961-217-6112', 'user'),
        (5, '481001070', 'toor', 'Yliya', 'NULL', 'seller')
    ]
    cursor.executemany("""
    INSERT INTO user VALUES (?, ?, ?, ?, ?, ?);
    """, default_users)
    connect.commit()
    connect.close()


def main_user_info(chat_id):

    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute("""
    SELECT * FROM user
    WHERE id_telegram = :chat_id;
    """, {'chat_id': chat_id})

    result = cursor.fetchall()
    connect.close()
    result_dict = {'name': result[0][3], 'phone': result[0][4], 'admitt_level': result[0][5],
                   'password': result[0][2]}
    return result_dict


def unauthorized_users(chat_id, name):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute("""
    SELECT id_telegram FROM strangers;""")

    result = cursor.fetchall()
    result = [i[0] for i in result]

    cursor.executemany("""
    INSERT INTO strangers VALUES (?, ?, ?);
    """, [chat_id, name, datetime.datetime.now()])
    connect.commit()
    connect.close()
    return result


def admins_contact():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute("""
    SELECT name, contact 
    FROM user
    WHERE admitt_level = 'admin' 
    OR admitt_level = 'creator';
    """)
    result = cursor.fetchall()
    connect.close()
    return result


def get_user_ids():

    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute("""
    SELECT id_telegram FROM user;
    """)
    result = cursor.fetchall()
    connect.close()
    result = [i[0] for i in result]
    return result


def get_session_status(chat_id: str):
    """
    :param chat_id: ID чата (юзера телеграм) в которое отправляется сообщение
    :return: словарь - 0: код статуса, 1: данные от пользователя или NULL, 2: qr-код или none
    """
    try:
        connect = sqlite3.connect(DB_NAME)
        cursor = connect.cursor()
        cursor.execute("""
        SELECT status, data, qr_code 
        FROM session
        WHERE id_telegram = :id;
        """, {'id': chat_id})
        result = cursor.fetchall()
        connect.close()
    except sqlite3.OperationalError:
        return None
    try:
        result = [i for i in result[0]]
    except IndexError:
        return None
    return result


def change_session_status(chat_id: str, new_session_status='', user_data='', qr_code=''):
    """
    :param chat_id: ID чата (юзера телеграм) в которое отправляется сообщение
    :param new_session_status: новый код статуса (список кодов ниже)
    :param user_data: данные, которые передал пользователь
    :param qr_code: содержание qr-кода
    :return: Ничего не возвращает, для извлечения данных исп. get_session_status()
    ПРЕФИКСЫ:
    * PE - меняем информацию о профиле (profile_editing)
    * CR - меню создателя
    * RD - запрос информации из БД
    * ED - редактирование БД
    * QR - расшифровка QR-кода
    * CANC - отмена изменения
    ПОСТФИКСЫ:
    * PE-name - меняем ник; PE-contact - меняем телефон; PE-password - меняем пароль
    """
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    if new_session_status == 'CANC':
        cursor.execute("""
        DELETE FROM session
        WHERE id_telegram = :id;
        """, {"id": chat_id})
        connect.commit()
        connect.close()
        return

    cursor.execute("""
    SELECT * FROM session
    WHERE id_telegram = ?;
    """, (chat_id, ))
    result = cursor.fetchall()

    if result and qr_code:
        new_session_status = result[0][1] + new_session_status
        cursor.execute("""
        UPDATE session
        SET status = :status, data = :data, qr_code = :qr_code
        WHERE id_telegram = :id;
        """, {"status": new_session_status, "data": user_data, "id": chat_id, "qr_code": qr_code})
    elif result:
        new_session_status = result[0][1] + new_session_status
        cursor.execute("""
        UPDATE session
        SET status = :status, data = :data
        WHERE id_telegram = :id;
        """, {"status": new_session_status, "data": user_data, "id": chat_id})
    else:
        cursor.execute("""
        INSERT INTO session VALUES (?, ?, ?, ?, ?);
        """, [chat_id, new_session_status, user_data, datetime.datetime.now(), qr_code])

    connect.commit()
    connect.close()


def change_user_inf(chat_id: str, column, new_data):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute(f"""
    UPDATE user
    SET {column} = :data
    WHERE id_telegram = :id;
    """, {'data': new_data, 'id': chat_id})
    connect.commit()
    connect.close()


def qr_code_check(id_product):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute("""
        SELECT * 
        FROM product
        WHERE id_product = :id_product;
        """, {'id_product': id_product})
    result = cursor.fetchall()
    connect.close()
    if result:
        return result
    else:
        return False


def sale_registration(qr_code):
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute("""
        UPDATE product
        SET status = 'sold'
        WHERE id_product = :id;
        """, {'id': qr_code})
    connect.commit()
    connect.close()


def general_product_request():
    r = {}
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute("""SELECT count(id_product), sum(purchase_price), sum(selling_price) FROM product;""")
    a = cursor.fetchall()
    r['total_number'] = a[0][0]
    r['total_purchase'] = a[0][1]
    r['total_selling'] = a[0][2]

    cursor.execute("""SELECT count(id_product), sum(purchase_price), sum(selling_price) 
    FROM product WHERE status = 'stock';""")
    a = cursor.fetchall()
    r['in_stock'] = a[0][0]
    r['in_stock_purchase'] = a[0][1]
    r['in_stock_selling'] = a[0][2]

    cursor.execute("""SELECT count(id_product), sum(purchase_price), sum(selling_price) 
    FROM product WHERE status = 'store';""")
    a = cursor.fetchall()
    r['in_store'] = a[0][0]
    r['in_store_purchase'] = a[0][1]
    r['in_store_selling'] = a[0][2]

    cursor.execute("""SELECT count(id_product), sum(purchase_price), sum(selling_price) 
    FROM product WHERE status = 'sold';""")
    a = cursor.fetchall()
    r['sold'] = a[0][0]
    r['sold_purchase'] = a[0][1]
    r['sold_selling'] = a[0][2]

    connect.close()

    output = f"""
    Общее:
    шт------ {r['total_number']} шт
    СебСт--- {r['total_purchase']} р.
    Доход--- {r['total_selling']} р.
    Прибыль- {r['total_selling'] - r['total_purchase']} р.
    --------
    На складе {r['in_stock']} шт.
    На точках {r['in_store']} шт.
    Продано {r['sold']} шт (+{r['sold_selling'] - r['sold_purchase']} р.)
    """
    return output


def general_user_request():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()
    cursor.execute("""SELECT count(id_telegram) FROM user;""")
    output = str(cursor.fetchall()[0][0])
    output += ' чел имеют доступ к боту:\n'
    cursor.execute("""SELECT id_telegram, name, admitt_level FROM user ORDER BY admitt_level;""")
    a = cursor.fetchall()
    for string in a:
        for cell in string:
            if cell == 'creator':
                cell = 'admin'
            output += cell + ' '
        output += '\n'
    connect.close()
    return output
