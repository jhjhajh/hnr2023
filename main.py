import logging
from os import environ as env
from dotenv import load_dotenv # if you dont have dotenv yet: pip install python-dotenv

import telebot
import openai

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
bot = telebot.TeleBot(env["BOT_API_KEY"])
openai.api_key = env["OPENAI_API_KEY"]

@bot.message_handler(func=lambda message: True)

def get_codex(message):
    # prompt = message.text
    response = openai.Completion.create(
    model="text-davinci-003",
    # prompt="To explain horse in a peculiar but short way, without mentioning the word horse: ",
    prompt='"""\n{}\n"""'.format(message.text),
    # prompt=["explain "+message.text+" in a peculiar but short way without mentioning the word "+message.text+". Do not explicitly mention words related to "+message.text+". "],
    # temperature=0,
    # max_tokens=100,
    # top_p=1,
    # frequency_penalty=0.0,
    # presence_penalty=0.0,
    stop=["\n"]
    )

    # response = openai.Completion.create(
    # model="text-davinci-003",
    # prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: Where is the Valley of Kings?\nA:",
    # temperature=0,
    # max_tokens=100,
    # top_p=1,
    # frequency_penalty=0.0,
    # presence_penalty=0.0,
    # stop=["\n"])
    
    bot.send_message(message.chat.id,
    text=response["choices"][0]["text"],
    parse_mode="Markdown")
    
    # response = openai.Completion.create(
    # # engine="code-davinci-001",
    # engine="text-davinci-003",
    # prompt='"""\n{}\n"""'.format(message.text),
    # temperature=0,
    # max_tokens=1200,
    # top_p=1,
    # frequency_penalty=0,
    # presence_penalty=0,
    # stop=['"""'])

    # bot.send_message(message.chat.id,
    # text=response["choices"][0]["text"],
    # parse_mode="Markdown")

bot.infinity_polling()
