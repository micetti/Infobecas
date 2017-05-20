import time
import telepot

TOKEN = 'TOKEN'

def echo(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    if content_type == 'text':
        bot.sendMessage(chat_id, message['text'])

if __name__ == '__main__':
    bot = telepot.Bot(TOKEN)
    bot.message_loop(echo)
    # Keep the program running.
    while 1:
        time.sleep(1)