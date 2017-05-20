import time
from redis import Redis
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters

from answers.predefined_answers import PredefinedAnswers

import user
from questions import questions
from token_file import token

redis = Redis(host='127.0.0.1', port=6379, db=0)

TOKEN = token



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=PredefinedAnswers.welcome_message)


def echo(bot, update):
    redis.delete(update.message.chat_id)

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()
