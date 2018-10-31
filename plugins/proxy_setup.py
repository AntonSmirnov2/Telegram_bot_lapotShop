import telebot
from config import TELE_BOT_TOKEN
# from plugins.message_replier import message_replier

bot = telebot.TeleBot(TELE_BOT_TOKEN)

PROXIES_LST = [
    {'https': 'socks5h://5.135.20.158:8080'},
    {'https': 'socks5h://148.251.238.35:1080'},
    {'https': 'socks5h://188.226.141.127:1080'},
    {'https': 'socks5h://217.23.6.40:1080'}
]


def proxy_setup():
    for proxy in PROXIES_LST:
        telebot.apihelper.proxy = proxy
        bot.set_update_listener(message_replier)
        print(f'Try to connect...{proxy["https"]}', end=' ')
        try:
            bot.polling(none_stop=True, interval=0, timeout=3)
        except:
            print('Отказ.')
            continue
