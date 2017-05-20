import time
import telepot
from redis import Redis

import user
from questions import questions

redis = Redis(host='database', port=6379, db=0)

TOKEN = ''

def echo(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    if content_type == 'text':
        user_profile = redis.get(chat_id)
        if user_profile:
            answer = message['text']
            returning_user = user.create_user_from_json(chat_id, user_profile.decode("utf-8"))
            returning_user.answer_question(answer)
            next_question = returning_user.next_question()
            returning_user.last_question = next_question
            if next_question:
                bot.sendMessage(chat_id, questions[next_question])
            else:
                bot.sendMessage(chat_id, "Thats all!")
            redis.set(chat_id, returning_user.get_as_json())
        else:
            bot.sendMessage(chat_id, "Hello first_time_user")
            first_time_user = user.User(chat_id)
            next_question = first_time_user.next_question()
            first_time_user.last_question = next_question
            bot.sendMessage(chat_id, questions[next_question])
            redis.set(chat_id, first_time_user.get_as_json())


if __name__ == '__main__':
    bot = telepot.Bot(TOKEN)
    bot.message_loop(echo)
    # Keep the program running.
    while 1:
        time.sleep(1)