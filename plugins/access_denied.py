import telebot
import datetime
from config import TELE_BOT_TOKEN, ADMIN_IDS
from plugins.check_db import unauthorized_users

bot = telebot.TeleBot(TELE_BOT_TOKEN)


@bot.message_handler(func=lambda message: True)
def access_denieded(message):
    chat_id = str(message.from_user.id)
    user_name = str(message.chat.first_name)
    unauthorized_users_content = unauthorized_users(chat_id, user_name)

    if chat_id not in unauthorized_users_content:
        reply = (f'Привет, {user_name}!:) Я БОТ-помошник ребят из Lapot_Shop.\n\n'
                 f' Вижу ты не авторизованый пользователь, так что у тебя не получится поль'
                 f'зоваться моими функциями:(\n Напиши моему создателю по любым вопросам!')
    else:
        reply = (f'Привет еще раз, {user_name}!:)\n\n'
                 f'Кто-то, когда-то написал:\n'
                 f'"Никогда не стучитесь в закрытые двери, никогда не бегите за уходящими поездами..."\n'
                 f'Но серьезно, раз тебе так интересно, напиши моему создателю :D')

    bot.send_message(chat_id, reply)


