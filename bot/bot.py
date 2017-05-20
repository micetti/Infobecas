import time
import telepot
from redis import Redis

redis = Redis(host='database', port=6379)

TOKEN = ''

def echo(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    if content_type == 'text':
        redis.set(chat_id, message['text'])
        message_from_db = redis.get(chat_id)
        bot.sendMessage(chat_id, message_from_db)

if __name__ == '__main__':
    bot = telepot.Bot(TOKEN)
    bot.message_loop(echo)
    # Keep the program running.
    while 1:
        time.sleep(1)