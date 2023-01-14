import telegram
import telegram.ext
# import queue
import re
import openai

from os import environ as env
from dotenv import load_dotenv

# The API Key we received for our bot
API_KEY = "5634663497:AAF4Xih_61qN1KxsdhrtrgqOZOquETBy8mE"
openai.api_key = "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"
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

# The entry function
def start(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    update_obj.message.reply_text("Hello, welcome to McDermott Group's Bot! Choose a mode to start (Define/Play)",
        reply_markup=telegram.ReplyKeyboardMarkup([['Define', 'Play']], one_time_keyboard=True)
    )
    # go to the WELCOME state
    return WELCOME

# helper function, generates new numbers and sends the question
def randomize_word(update_obj, context):
    prompt_message = "generate a commonly-used non-article word, do not give me a code or a sentence"
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt='"""\n{}\n"""'.format(prompt_message),
    temperature=0,
    max_tokens=1200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=['"""'])
    
    # store the answer in the context
    context.user_data['answer'] = response["choices"][0]["text"].strip()
    # context.user_data['answer'] = context.user_data['answer'].translate()
    context.user_data['answer'] = context.user_data['answer'].lower()
    update_obj.message.reply_text(f'''Answer: {response["choices"][0]["text"]} \n''')
    print(f'''Answer: {response["choices"][0]["text"]} \n''')
    print(context.user_data['answer'])
    
    prompt_message2 = "explain " + context.user_data['answer'] + " in a fun and weird but short way without mentioning the word" + context.user_data['answer'] + " Do not explicitly mention words related to " + context.user_data['answer']

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
    update_obj.message.reply_text(f'''{response2["choices"][0]["text"]} \n Recorded answer: {context.user_data['answer']}''')

# in the WELCOME state, check if the user wants to answer a question
def welcome(update_obj, context):
    if update_obj.message.text.lower() == 'play':
        # send question, and go to the PLAY state
        update_obj.message.reply_text("Going to PLAY state")
        randomize_word(update_obj, context)
        update_obj.message.reply_text("Random word generated")
        return PLAY
    else:
        update_obj.message.reply_text("Going to DEFINE state")
        # go to the PLAY state
        return DEFINE

# in the QUESTION state
def play(update_obj, context):
    # expected solution
    # check if the solution was correct
    if (context.user_data['answer'] == update_obj.message.text.lower()):
        # correct answer, ask the user if he found tutorial helpful, and go to the CORRECT state
        update_obj.message.reply_text("Correct answer!")
        update_obj.message.reply_text("Play another game?", reply_markup=telegram.ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True))
        return CORRECT
    else:
        # wrong answer, reply, try again
        update_obj.message.reply_text("Wrong answer... Try again!")
        return PLAY

# in the CORRECT state
def correct(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        return WELCOME
    else:
        # get the user's first name
        first_name = update_obj.message.from_user['first_name']
        update_obj.message.reply_text(f"See you {first_name}!, bye")
        return telegram.ext.ConversationHandler.END

def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}!", reply_markup=telegram.ReplyKeyboardRemove()
    )
    return telegram.ext.ConversationHandler.END

# a regular expression that matches yes or no
define_play_regex = re.compile(r'^(Define|Play)$', re.IGNORECASE)
yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)
# Create our ConversationHandler, with only one state
handler = telegram.ext.ConversationHandler(
      entry_points=[telegram.ext.CommandHandler('start', start)],
      states={
            WELCOME: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(define_play_regex), welcome)],
            # DEFINE: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), define)],
            PLAY: [telegram.ext.MessageHandler(telegram.ext.Filters.text, play)],
            CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), cancel)],
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