import telegram
import telegram.ext
import string
import re
import openai
import os 
import config
import random

from os import environ as env
from dotenv import load_dotenv

load_dotenv()
# The API Key we received for our bot
API_KEY =env["BOT_API_KEY"]
openai.api_key=env["OPENAI_API_KEY"]
# update_queue = queue.Queue()
# Create an updater object with our API Key
updater = telegram.ext.Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher
# Our states, as integers
WELCOME = 0
DEFINE = 1
PLAY = 2
CANCEL = 3
CORRECT = 4
RESTART = 5

# The entry function
def start(update_obj, context):

            # send the question, and show the keyboard markup (suggested answers)
    update_obj.message.reply_text("Hello, welcome to McDermott Group's Bot! Choose a mode to start (Define/Play)",
    reply_markup=telegram.ReplyKeyboardMarkup([['Define', 'Play']], one_time_keyboard=True)
    )

    # # populate words array from config file
    # try:
    #     if os.path.isfile('data.txt'):
    #         with open('data.txt', 'r') as f:
    #             tempFile = f.read()
    #             tempFile = tempFile.splitlines()
    #             x = 0
    #             while x < len(tempFile):
    #                 config.words += [tempFile[x]]
    #                 x+=1
    #     for word in config.words:
    #         print(word)
    # except Exception as e:
    #     first_name = update_obj.message.from_user['first_name']
    #     print("unable to read file. check the format of data file")
    #     print (e.msg)
    #     update_obj.message.reply_text(f"Unable to load bot. See you {first_name}!, bye")

    # go to the WELCOME state
    return WELCOME

# helper function, generates new numbers and sends the question
def randomize_word(update_obj, context):
    print(config.index)
    print(" " + config.words[config.index])
    prompt_message2 = "explain " + config.words[config.index] + " in a fun and weird but short way without mentioning the word" + config.words[config.index] + " Do not explicitly mention words related to " + config.words[config.index]

    response2 = openai.Completion.create(
    engine="text-davinci-003",
    prompt='"""\n{}\n"""'.format(prompt_message2),
    temperature=0,
    max_tokens=1200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=['"""'])
    
    # send the question
    update_obj.message.reply_text(f'''{response2["choices"][0]["text"]} \n''')    

# helper function, generates new numbers and sends the question
def define(update_obj, context):
    context.user_data['word'] = update_obj.message.text.translate(str.maketrans('','', string.punctuation)).lower()
    prompt_message2 = "explain " + context.user_data['word'] + " in a fun and weird but short way without mentioning the word" + context.user_data['word'] + " Do not explicitly mention words related to " + context.user_data['word']

    response2 = openai.Completion.create(
    engine="text-davinci-003",
    prompt='"""\n{}\n"""'.format(prompt_message2),
    temperature=0,
    max_tokens=1200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=['"""'])
    
    # send the definition
    update_obj.message.reply_text(f'''{response2["choices"][0]["text"]}''')
    update_obj.message.reply_text("Play another game?", reply_markup=telegram.ReplyKeyboardMarkup([['yes', 'no']], one_time_keyboard=True))
    return CORRECT

# in the WELCOME state, check if the user wants to answer a question
def welcome(update_obj, context):
    if update_obj.message.text.lower() == 'play':
        # send question, and go to the PLAY state
        update_obj.message.reply_text("Going to PLAY state")
        randomize_word(update_obj, context)
        update_obj.message.reply_text("Random word generated")
        return PLAY
    else:
        update_obj.message.reply_text("Send me a word!")
        # go to the DEFINE state
        return DEFINE

# in the PLAY state
def play(update_obj, context):
    # expected solution
    # check if the solution was correct
    if (config.words[config.index] == update_obj.message.text.lower()):
        # correct answer, ask the user if he found tutorial helpful, and go to the CORRECT state
        update_obj.message.reply_text("Correct answer!")
        update_obj.message.reply_text("Play another game?", reply_markup=telegram.ReplyKeyboardMarkup([['yes', 'no']], one_time_keyboard=True))
        print("4")
        return CORRECT
    else:
        # wrong answer, reply, try again
        update_obj.message.reply_text("Wrong answer... Try again!")
        return PLAY

# # in the DEFINE state
# def define(update_obj, context):
#     get_definition(update_obj, context)
#     return CORRECT
    
# in the CORRECT state
def correct(update_obj, context):
    print("3")
    if update_obj.message.text.lower() in ['yes', 'y']:
        update_obj.message.reply_text("Send /start to play again.")
        print("1")
        return telegram.ext.ConversationHandler.END
    else:
        print("2")
        return CANCEL

def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(f"See you {first_name}, bye!")
    return telegram.ext.ConversationHandler.END

# def restart(update_obj, context):
#     update_obj.message.reply_text("Entered restart stage.")
#     update_obj.message.reply_text("Send /start to play again.")
#     return telegram.ext.ConversationHandler.END

# a regular expression that matches yes or no
define_play_regex = re.compile(r'^(Define|Play)$', re.IGNORECASE)
yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)
# Create our ConversationHandler, with only one state
handler = telegram.ext.ConversationHandler(
      entry_points=[telegram.ext.CommandHandler('start', start)],
      states={
            WELCOME: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(define_play_regex), welcome)],
            DEFINE: [telegram.ext.MessageHandler(telegram.ext.Filters.text, define)],
            PLAY: [telegram.ext.MessageHandler(telegram.ext.Filters.text, play)],
            CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), cancel)],
            # RESTART: [telegram.ext.MessageHandler(telegram.ext.Filters.all, restart)],
            # CORRECT: [telegram.ext.MessageHandler(telegram.ext.Filters.all, correct)],
            CORRECT: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), correct)],
      },
      fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
      )
# add the handler to the dispatcher
dispatcher.add_handler(handler)
# start polling for updates from Telegram
updater.start_polling()
# block until a signal (like one sent by CTRL+C) is sent
updater.idle()