from requests import request
import telebot as tb
from config import *
from handler import *
import matplotlib.pyplot as plt

bot = tb.TeleBot(BOT_TOKEN)
app = None

@bot.message_handler(commands=['start'])
def start(msg):
    user = User(msg)
    txt = f'Hello {user.uname}! Write something..'
    bot.send_message(user.uid, txt)

@bot.message_handler(commands=['help'])
def help(msg):
    user = User(msg)
    req = Request(msg.json['text'])
    ftxt = f'Hi {user.uname}!\nLet me introduce how to use our commands\n\n'
    etxt = '/eq - Solve equation\n'
    etxt += '/eqb - Solve equation by Binary searching algo\n'
    etxt += '/eqs - Solve equaiton by Secant algo\n'
    etxt += '/eqt - Solve equation by Brent algo\n\n'
    itxt = '/integ - Calculate integral of function in given ranges\n'
    itxt += '/integs - Calculate integral by Simpson rule\n'
    itxt += '/integt - Calculate integral by Trapezoid rule\n'
    itxt += '/integl - Calculate integral by Left Rectangle rule\n'
    itxt += '/integr - Calculate integral by Right Rectangle rule\n\n'
    atxt = '/app - Find approximated value for 2D functions\n'
    atxt += '/appx - Set X-coordinate values\n'
    atxt += '/appy - Set Y-coordinate values\n'
    atxt += '/appv - Get interpolated value at given X-point\n\n'
    ltxt = '$$$ Have fun with us!' # last help text
    txt = ftxt  # first help text
    if req.body.find('eq') == 1:
        txt += etxt
    if req.body.find('integ') == 1:
        txt += itxt
    if req.body.find('app') == 1:
        txt += atxt
    if len(txt) == len(ftxt):
        txt += etxt + itxt + atxt
    txt += ltxt
    bot.send_message(user.uid, txt)

@bot.message_handler(commands=['eq', 'eqb', 'eqs', 'eqt'])
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
        txt = 'Error code: 400. Bad request: can not recognize that function'
        if solution is not None:
            roots, runtimes = solution[0], solution[1]
            def roots_to_str(roots):
                if len(roots) > 0:
                    return '\n'.join([f'X{j} = {roots[j]}' for j in range(len(roots))])
                return 'No roots.'
            txt = '\n\n'.join([
                f'{i+1} {msg[i]} ({runtimes[i]*1e3:.2f} ms):\n{roots_to_str(roots[i])}' 
                for i in range(len(methods))
            ])
            a, b = -1e2, 1e2
            if Equation.fType(equation):
                a, b = -pi, pi
            plt1 = Graphic.plotFunc(plt, Equation.func(equation), a, b, title='Equation')
            plt1.savefig('temp/equation.png', dpi=300)
            bot.send_photo(uid, photo=open('temp/equation.png', 'rb'))
        bot.send_message(uid, txt)
    except Exception as e:
        bot.send_message(uid, f'Error code: 400. {e.args}')

@bot.message_handler(commands=['integ', 'integs', 'integt', 'integl', 'integr'])
def handle_integ_cmds(msg):
    uid = User.get_uid(msg)
    try:
        req = Request(msg.json['text'])
        tmp = Integral(req.body)
        methods = [Integral.simpson, Integral.trapezoid, Integral.lrectangle, Integral.rrectangle]
        if req.cmd[-1] == 's':
            methods = [Integral.simpson]
        elif req.cmd[-1] == 't':
            methods = [Integral.trapezoid]
        elif req.cmd[-1] == 'l':
            methods = [Integral.lrectangle]
        elif req.cmd[-1] == 'r':
            methods = [Integral.rrectangle]
        results = integ(tmp.func, tmp.a, tmp.b, methods)
        txt = '\n\n'.join([
            f'{i+1} {results[i]["rule"]} ({results[i]["runtime"]*1e3:.2f} ms):\n{results[i]["value"]}' 
            for i in range(len(results))
        ])
        if Equation.fType(req.body.split(',')[0]):
            tmp.a, tmp.b = -pi, pi
        plt1 = Graphic.plotFunc(plt, tmp.func, tmp.a, tmp.b, title='Integral')
        plt1.savefig('temp/integral.png', dpi=300)
        bot.send_photo(uid, photo=open('temp/integral.png', 'rb'))
        bot.send_message(uid, txt)
    except Exception as e:
        bot.send_message(uid, f'Error code: 400. {e.args}')

@bot.message_handler(commands=['app'])
def handle_app_cmd(msg):
    uid = User.get_uid(msg)
    global app
    try:
        req = Request(msg.json['text'])
        app = Approximation(req.body)
        show_options(msg)
    except Exception as e:
        bot.send_message(uid, f'Error code: 400. {e.args}')

def show_options(msg, value=None):
    uid = User.get_uid(msg)
    itembtne = tb.types.KeyboardButton('Newton')
    itembtcs = tb.types.KeyboardButton('Cubic Spline')
    itembtls = tb.types.KeyboardButton('LSM')
    itembtal = tb.types.KeyboardButton('All')
    markup = tb.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row(itembtne, itembtcs, itembtls)
    markup.row(itembtal)
    reply = bot.send_message(uid, 'Choose algorithms below', reply_markup=markup)
    bot.register_next_step_handler(reply, lambda m: run_app(m, value))

def run_app(msg, value=None):
    uid = User.get_uid(msg)
    algos = ['ne', 'cs', 'lsm']
    if msg.json['text'] == 'Newton':
        algos = ['ne']
    elif msg.json['text'] == 'Cubic Spline':
        algos = ['cs']
    elif msg.json['text'] == 'LSM':
        algos = ['lsm']
    if value is None:
        reply = bot.send_message(uid, 'Now use /appv command to calculate interpolation')
        bot.register_next_step_handler(reply, lambda m: run_appv(m, algos))
    else:
        run_appv(msg, algos, value)

@bot.message_handler(commands=['appv'])
def ini_appv(msg):
    uid = User.get_uid(msg)
    try:
        if app is not None:
            tmp = Request(msg.json['text'])
            show_options(msg, value=tmp.body)
        else:
            bot.send_message(uid, 'Use /app, /appx or /appy first to set values')
    except:
        bot.send_message(uid, 'Error code: 400. Bad request: invalid command instruction')

def run_appv(msg, algos, value=None):
    uid = User.get_uid(msg)
    if value is None:
        tmp = Request(msg.json['text'])
        value = tmp.body
    txt = ''
    for item in app.interp(value, algos=algos):
        txt += f'{item["algo"]}: {item["value"]}\n'
    plt1 = Graphic.plotApp(plt, app.X, app.Y, legends=algos)
    plt1.savefig('temp/interpolation.png', dpi=300)
    bot.send_photo(uid, photo=open('temp/interpolation.png', 'rb'))
    bot.send_message(uid, txt)

@bot.message_handler(commands=['appx', 'appy'])
def run_appxy(msg):
    uid = User.get_uid(msg)
    global app
    try:
        if app is None:
            app = Approximation()
        tmp = Request(msg.json['text'])
        if tmp.cmd[-1] == 'x':
            app.setX(tmp.body)
        else:
            app.setY(tmp.body)
        bot.send_message(uid, f'{tmp.cmd[-1].upper()} is set successfully')
    except Exception as e:
        bot.send_message(uid, f'Error code: 400. {e.args}')

@bot.message_handler(content_types=['text'])
def handle_text(msg):
    user = User(msg)
    bot.send_message(user.uid, f'Hi, {user.uname}.\nType /help to know what i can help you')

# Run bot
bot.infinity_polling(timeout=10, long_polling_timeout=5)