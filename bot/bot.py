import time
from redis import Redis
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

from answers.predefined_answers import PredefinedAnswers

import user

redis = Redis(host='database', port=6379, db=0)

TOKEN = ''


def echo(bot, update):
    content = update.message.text
    chat_id = update.message.chat_id
    user_profile = redis.get(chat_id)
    if user_profile:
        bot.send_message(chat_id=update.message.chat_id, text="Hi back, {}".format(chat_id))
        returning_user = user.create_user_from_json(chat_id, user_profile.decode("utf-8"))
    else:
        bot.sendMessage(chat_id, "Whats your name?", )
        first_time_user = user.User(chat_id)
        redis.set(chat_id, first_time_user.get_as_json())
        bot.send_message(chat_id=update.message.chat_id, text=content)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=PredefinedAnswers.welcome_message)


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()
