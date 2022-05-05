import telebot as tb
from config import *
from handler import *

bot = tb.TeleBot(BOT_TOKEN)
eq_cmds = ['eq', 'eqb', 'eqs', 'eqt']
def send_msg(uid, txt):
    bot.send_message(uid, txt)

@bot.message_handler(commands=['start'])
def start(msg):
    user = User(msg)
    txt = f'Hello {user.uname}! Write something..'
    send_msg(user.uid, txt)

@bot.message_handler(commands=['help'])
def help(msg):
    user = User(msg)
    txt = f'Hi {user.uname}!\nLet me introduce how to use our commands\n\n'
    txt += '/eq - Solve equation\n'
    txt += '/eqb - Solve equation by Binary searching algo\n'
    txt += '/eqs - Solve equaiton by Secant algo\n'
    txt += '/eqt - Solve equation by Brent algo\n\n'
    txt += '/integ - Calculate integral of function in given ranges\n'
    txt += '/app - Find approximated value for 2D functions\n\n'
    txt += '$$$ Have fun with us!'
    send_msg(user.uid, txt)

@bot.message_handler(commands=eq_cmds)
def handle_eq_cmds(msg):
    uid = User.get_uid(msg)
    try:
        req = Request(msg.json['text'])
        equation = req.body
        methods = [binary_searching, secant, brentq]
        msg = ['Binary searching algo', 'Secant algo', 'Brent algo']
        if req.cmd[-1] == 'b':
            methods = [binary_searching]
            msg = ['Binary searching algo']
        elif req.cmd[-1] == 's':
            methods = [secant]
            msg = ['Secant algo']
        elif req.cmd[-1] == 't':
            methods = [brentq]
            msg = ['Brent algo']
        solution = eq(equation, methods)
        txt = 'Error code: 401. Bad request: can not recognize that function'
        if solution is not None:
            roots, runtimes = solution[0], solution[1]
            def roots_to_str(roots):
                if len(roots) > 0:
                    return '\n'.join([f'X{j} = {roots[j]}' for j in range(len(roots))])
                return 'No roots.'
            txt = '\n\n'.join([
                f'{i+1} {msg[i]} ({runtimes[i]*1000:.2f} ms):\n{roots_to_str(roots[i])}' 
                for i in range(len(methods))
            ])
        send_msg(uid, txt)
    except:
        send_msg(uid, 'Error code: 400. Bad request: invalid command instruction')

@bot.message_handler(content_types=['text'])
def handle_text(msg):
    user = User(msg)
    txt = f'{user.uname} wrote: ' + msg.json['text']
    bot.send_message(user.uid, txt)

# Run bot
bot.polling(none_stop=True, interval=0)