import time
import telepot
from redis import Redis

import user

redis = Redis(host='database', port=6379, db=0)

TOKEN = ''

def echo(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    if content_type == 'text':
        user_profile = redis.get(chat_id)
        if user_profile:
            bot.sendMessage(chat_id, "Hi, back")
            returning_user = user.create_user_from_json(chat_id, user_profile.decode("utf-8"))
        else:
            bot.sendMessage(chat_id, "Whats your name?")
            first_time_user = user.User(chat_id)
            redis.set(chat_id, first_time_user.get_as_json())


if __name__ == '__main__':
    bot = telepot.Bot(TOKEN)
    bot.message_loop(echo)
    # Keep the program running.
    while 1:
        time.sleep(1)