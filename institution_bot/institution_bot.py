import time
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)

from answers.predefined_answers import institution_answers

from token_file import token

TOKEN = token


def institution_start_handler(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=institution_answers['welcome'])
    bot.send_message(chat_id=chat_id, text=institution_answers['check_docs'])
    bot.send_message(chat_id=chat_id, text=institution_answers['doc_link'])
    bot.send_message(chat_id=chat_id, text=institution_answers['in_touch'])


if __name__ == '__main__':


    institution_updater = Updater(TOKEN)
    institution_dispatcher = institution_updater.dispatcher

    start_handler = CommandHandler('start', institution_start_handler)
    institution_dispatcher.add_handler(start_handler)

    institution_updater.start_polling()
    institution_updater.idle()