import time
from redis import Redis
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)

from answers.predefined_answers import predefined_answers

import user
from questions import questions
from token_file import token
from institutions import institutions

redis = Redis(host='127.0.0.1', port=6379, db=0)

TOKEN = token


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=predefined_answers.welcome_message)

def build_nice_response(match):
    name = match['name']
    budget = match['budget']
    num_scholarships = match['num_scholarships']
    response = '<b> ' + name + '</b>\n'
    response += 'Number of Scholarships: ' + str(num_scholarships) + '\n'
    response += 'Voulume of the Scholarship' + str(budget) + '\n'
    response += 'Talk to theme here: <a href="http://google.com">link</a>'
    return response

def echo(bot, update):
    chat_id = update.message.chat_id

    user_profile = redis.get(chat_id)

    if user_profile:
        content = update.message.text
        returning_user = user.create_user_from_json(chat_id, user_profile.decode("utf-8"))
        if returning_user.last_question:
            returning_user.answer_question(content)
            next_question = returning_user.next_question()
            returning_user.last_question = next_question
            if next_question:
                responsive_reply(bot, chat_id, next_question)
            else:
                bot.send_message(chat_id=chat_id, text="Thats all! Here is the summay of our nice conversation:")
                bot.send_message(chat_id=chat_id, text=returning_user.get_summary_message())
                match = returning_user.get_match()
                time.sleep(3)
                if not match:
                    bot.send_message(chat_id=chat_id, text="Sorry no matches found")
                else:
                    bot.send_message(chat_id=chat_id, text="We found a match for you")
                    nice_match_found_message = build_nice_response(institutions[0])
                    bot.send_photo(chat_id=chat_id, photo='http://pm1.narvii.com/6415/ac702663901e3934c297213aabaec4204ae6a106_128.jpg')
                    bot.send_message(chat_id=chat_id, text=nice_match_found_message, parse_mode=ParseMode.HTML)
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


def delete(bot, update):
    chat_id = update.message.chat_id
    redis.delete(chat_id)
    bot.send_message(chat_id=chat_id, text="Starting over")


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    delete_handler = CommandHandler('delete', delete)
    dispatcher.add_handler(delete_handler)

    updater.start_polling()
    updater.idle()
