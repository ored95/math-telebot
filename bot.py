import telebot as tb
from config import *
from handler import *

bot = tb.TeleBot(BOT_TOKEN)
cmds = ["eq", "integ", "app", "help"]
def send_msg(uid, txt):
    bot.send_message(uid, txt)

@bot.message_handler(commands=["start"])
def start(msg):
    user = User(msg)
    txt = f'Hello {user.uname}! Write something..'
    send_msg(user.uid, txt)

@bot.message_handler(commands=cmds)
def handle_cmd(msg):
    uid = User.get_uid(msg)
    try:
        req = Request(msg.json['text'])
        txt = req.body
        send_msg(uid, txt)
        print(msg.json['text'])
    except:
        send_msg(uid, 'Error code: 400. Bad request: invalid command instruction')

@bot.message_handler(content_types=["text"])
def handle_text(msg):
    user = User(msg)
    txt = f'{user.uname} wrote: ' + msg.json['text']
    bot.send_message(user.uid, txt)
    print(msg.json['text'])

# Run bot
bot.polling(none_stop=True, interval=0)