from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup
import logging
import os
import Parameters
import psutil

cwd = os.getcwd()
folder = os.path.dirname(os.path.abspath(__file__))
assert cwd == folder, "Process has to be started from folder. Pls do it right"

with open("token.txt", "r") as token_file:
    token = token_file.readline()
updater = Updater(token=token) # Insert bot token here
dispatcher = updater.dispatcher

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Emoji codes for intuitive keyboard
up    = u'\U00002B06'
down  = u'\U00002B07'
left  = u'\U00002B05'
right = u'\U000027A1'
lupe  = u'\U0001F50E'
plus  = u'\U00002795'
minus = u'\U00002796'
blitz = u'\U000026A1'
keyboard = ReplyKeyboardMarkup(keyboard=[[lupe+plus , up, lupe+minus], [left, 'Toggle Boost', right], ['Less Detail', down, 'More Detail']],
                               resize_keyboard=True)

keyboard_boost = ReplyKeyboardMarkup(keyboard=[[blitz+lupe+plus+blitz , blitz+up+blitz, blitz+lupe+minus+blitz], [blitz+left+blitz, 'Toggle Boost', blitz+right+blitz], [blitz+'Less Detail'+blitz, blitz+down+blitz, blitz+'More Detail'+blitz]],
                               resize_keyboard=True)


user_parameters = {}


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm the fractal bot! Just send me a command to get started", reply_markup=keyboard)
dispatcher.add_handler(CommandHandler("start", start))


def check_user(user_id):
    if(not user_id in user_parameters):
        user_parameters[user_id] = Parameters.parameters()
        return False
    return True


def calc_fractal(parameters):
    arguments = parameters.to_string()
    os.system("./picture_generator " + arguments)


def get_fractal(bot, update):
    user = update.message.chat_id
    
    check_user(user)
    
    calc_fractal(user_parameters[user])
    try:
        bot.send_document(chat_id=user, document=open('fraktal.png', 'rb'))
        bot.send_photo(chat_id=user, photo=open("fraktal.png", "rb"))
    except FileNotFoundError:
        bot.send_message(chat_id=user, text="Couldn't find generated picture. The dev is probably an idiot")

fractal_handler = CommandHandler("get_fractal", get_fractal)
dispatcher.add_handler(fractal_handler)



def commands(bot, update):
    
    command = update.message.text.split()[0][1:]

    values = [float(i) for i in update.message.text.split()[1:]]
    user = update.message.chat_id
    
    logging.info("Command received from user " + str(user) + ": " + command)

    check_user(user)
    params = user_parameters[user]

    if(not hasattr(user_parameters[user], command)):
        logging.error("Command not found")
        bot.send_message(chat_id=user, text="Command not found")
        return
        
    if(len(values)==0):
        output = getattr(user_parameters[user], command)()
    else:
        output = getattr(user_parameters[user], command)(*values)
    
    return_text = "Generating new picture"
    if(output is not None):
        return_text = output + "\n" + return_text

    if(params.boosted):
        markup = keyboard_boost
    else:
        markup = keyboard
    
    bot.send_message(chat_id=user, text=return_text, reply_markup=markup)
    get_fractal(bot, update)

    
    
commands_handler = MessageHandler(Filters.command, commands)
dispatcher.add_handler(commands_handler)


def message(bot, update):

    message = update.message.text
    user = update.message.chat_id
    check_user(user)
    logging.info("Message received from chat " + str(user) + ": " + message)

    params = user_parameters[user]

    output = None
    create_pic = True
    if(up in message):
        params.move_up()
    elif(down in message):
        params.move_down()
    elif(left in message):
        params.move_left()
    elif(right in message):
        params.move_right()
    elif(plus in message):
        params.zoom_in()
    elif(minus in message):
        params.zoom_out()
    elif('Boost' in message):
        output = params.toggle_boost()
        create_pic = False
    elif('More' in message):
        output = params.more_detail()
    elif('Less' in message):
        params.less_detail()

    if(create_pic):
        return_text = "Generating new picture"
    else:
        return_text = ""
    if(output is not None):
        return_text = output + "\n" + return_text

    if(params.boosted):
        markup = keyboard_boost
    else:
        markup = keyboard
    bot.send_message(chat_id=user, text=return_text, reply_markup=markup)

    if(create_pic):
        get_fractal(bot, update)

dispatcher.add_handler(MessageHandler(Filters.text, message))


# set program priority to low
p = psutil.Process(os.getpid())
if(os.name == 'nt'):
	#Windows
	p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
elif(os.name == "posix"):
	#Unix
	p.nice(19)

print("starting bot")
updater.start_polling()
updater.idle()
