import time
from redis import Redis
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

from answers.predefined_answers import predefined_answers

import user
from questions import questions
from token_file import token

redis = Redis(host='127.0.0.1', port=6379, db=0)

TOKEN = token


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=predefined_answers.welcome_message)


def echo(bot, update):
    chat_id = update.message.chat_id

    user_profile = redis.get(chat_id)

    if user_profile:

        content = update.message.text
        returning_user = user.create_user_from_json(chat_id, user_profile.decode("utf-8"))
        returning_user.answer_question(content)
        next_question = returning_user.next_question()
        returning_user.last_question = next_question
        if next_question:
             responsive_reply(bot, chat_id, next_question)
        else:
            bot.send_message(chat_id=chat_id, text="Thats all!")
        redis.set(chat_id, returning_user.get_as_json())
    else:
        bot.send_message(chat_id=chat_id, text="Hello first_time_user")
        first_time_user = user.User(chat_id)
        next_question = first_time_user.next_question()
        first_time_user.last_question = next_question
        responsive_reply(bot, chat_id, next_question)
        redis.set(chat_id, first_time_user.get_as_json())


def responsive_reply(bot, chat_id, next_question):
    if next_question in predefined_answers:
        bot.send_message(chat_id=chat_id, text=questions[next_question],
                         reply_markup=ReplyKeyboardMarkup(predefined_answers[next_question], one_time_keyboard=True))
    else:
        bot.send_message(chat_id=chat_id, text=questions[next_question])


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()
