import telebot
from config import TELE_BOT_TOKEN

bot = telebot.TeleBot(TELE_BOT_TOKEN)


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)
