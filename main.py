#################
# LAPOT BOT 2.0 #
#################
# Импортируем библиотеки
import telebot
import os
import sys
import datetime

# Подгружаем плагины, конфиг
from config import TELE_BOT_TOKEN, PROXY_CONNECTION
from plugins.message_replier import message_replier
from plugins.check_db import check_db_exist
from plugins.proxy_setup import proxy_setup

# Начало кода
bot = telebot.TeleBot(TELE_BOT_TOKEN)
time = datetime.datetime.now()

print(f'Bot started: {time}')
# check_db_exist()

if PROXY_CONNECTION:
    print('Подключение через прокси.')
    # proxy_setup()
    telebot.apihelper.proxy = {'https': 'socks5://5.135.20.158:8080'}
    bot.set_update_listener(message_replier)
    bot.polling(none_stop=True, interval=0, timeout=10)
else:
    bot.set_update_listener(message_replier)
    bot.polling(none_stop=True, interval=0, timeout=3)
