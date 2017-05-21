import time
from redis import Redis
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)

from answers.predefined_answers import predefined_answers
import answers.predefined_answers as phrase

import user
from questions import questions
from token_file import token
from institutions import institutions

redis = Redis(host='127.0.0.1', port=6379, db=0)

TOKEN = token

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=phrase.welcome_message)

def run(bot, update):
    chat_id = update.message.chat_id
    content = update.message.text
    user_profile = get_user(chat_id, bot)

    user_profile.answer_question(content)
    next_question = user_profile.next_question()
    user_profile.last_question = next_question
    if next_question:
        responsive_reply(bot, chat_id, next_question)
    else:
        finalize_conversation(chat_id, bot, user_profile)

    redis.set(chat_id, user_profile.get_as_json())


def build_nice_response(match):
    name = match['name']
    budget = match['budget']
    num_scholarships = match['num_scholarships']
    response = '<b> ' + name + '</b>\n'
    response += 'They are offering this Scholarship to ' + str(num_scholarships) + ' people.\n'
    response += 'In total it has a value of' + str(budget) + ' Euro.\n\n'
    response += 'Talk to them <a href="t.me/fake_uni1bot">here</a>'
    return response

def responsive_reply(bot, chat_id, next_question):
    if next_question in predefined_answers:
        markup = ReplyKeyboardMarkup(predefined_answers[next_question], one_time_keyboard=True)
        bot.send_message(chat_id=chat_id, text=questions[next_question],
                         reply_markup=markup)
    else:
        bot.send_message(chat_id=chat_id, text=questions[next_question])

def get_user(chat_id, bot):
    user_profile = redis.get(chat_id)
    if user_profile:
        return user.create_user_from_json(chat_id, user_profile.decode("utf-8"))
    else:
        bot.send_message(chat_id=chat_id, text=phrase.starting_message)
        time.sleep(2)
        bot.send_message(chat_id=chat_id, text=phrase.start_explanation)
        time.sleep(1)
        return user.User(chat_id)

def finalize_conversation(chat_id, bot, user_profile):
        bot.send_message(chat_id=chat_id, text="Thats all! Here is what I understood from our chat:")
        bot.send_message(chat_id=chat_id, text=user_profile.get_summary_message())
        time.sleep(3)
        bot.send_message(chat_id=chat_id, text="If you find some thing wrong, you can start over by typing /delete")
        time.sleep(1)
        bot.send_message(chat_id=chat_id, text=phrase.search_for_match)
        match = user_profile.get_match()
        time.sleep(2)
        bot.send_message(chat_id=chat_id, text=phrase.hourglass + "\nProtipp: A recomendation letter can make the difference")
        time.sleep(2)
        bot.send_message(chat_id=chat_id, text=phrase.hourglass + "\nDid you know that last year 1.9B dollar in scholaships did not match a candidate")
        time.sleep(2)
        bot.send_message(chat_id=chat_id, text=phrase.hourglass + "\nProtipp: Make sure you know about the institution you are about to apply to")
        time.sleep(2)
        if not match:
            bot.send_message(chat_id=chat_id, text="Sorry no matches found")
        else:
            bot.send_message(chat_id=chat_id, text="\nWe found a match for you\n")
            time.sleep(2)
            nice_match_found_message = build_nice_response(institutions[0])
            bot.send_photo(chat_id=chat_id, photo='http://pm1.narvii.com/6415/ac702663901e3934c297213aabaec4204ae6a106_128.jpg')
            bot.send_message(chat_id=chat_id, text=nice_match_found_message, parse_mode=ParseMode.HTML)


def delete(bot, update):
    chat_id = update.message.chat_id
    redis.delete(chat_id)
    bot.send_message(chat_id=chat_id, text="Starting over")


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    run_handler = MessageHandler(Filters.text, run)
    dispatcher.add_handler(run_handler)

    delete_handler = CommandHandler('delete', delete)
    dispatcher.add_handler(delete_handler)

    updater.start_polling()
    updater.idle()
