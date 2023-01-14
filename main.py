import logging
from os import environ as env
from dotenv import load_dotenv

import telebot
import openai

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
state = "default"

load_dotenv()
bot = telebot.TeleBot(token=env["BOT_API_KEY"])
openai.api_key=env["OPENAI_API_KEY"]

@bot.message_handler(commands=['start', 'hello'])
def handle_command(message):
    bot.reply_to(message, "Hello, welcome to McDermott Group's Bot!")

@bot.message_handler(commands=['define'])
def handle_command(message):
    global state
    if (state == "default"):
        bot.reply_to(message, "You are already in definition state!")
    else:
        bot.reply_to(message, "Send a word to receive its definition!")
        state = "default"

@bot.message_handler(commands=['play'])
def handle_command(message):
    global state
    if (state == "play"):
        bot.reply_to(message, "You are already in play state!")
    else:
        bot.reply_to(message, "Guess the word given its definition!")
        state = "play"

@bot.message_handler(func=lambda message: True)
def get_definition(message):
    if (state == "default"):
        prompt_message = "explain fun " + message.text + " in a fun and weird but short way without mentioning the word" + message.text + " Do not explicitly mention words related to " + message.text

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='"""\n{}\n"""'.format(prompt_message),
            temperature=0,
            max_tokens=1200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['"""'])

        bot.send_message(message.chat.id,
        f'```python\n{response["choices"][0]["text"]}\n```',
        parse_mode="Markdown")
    else:
        bot.reply_to(message, "not default mode")

bot.infinity_polling()