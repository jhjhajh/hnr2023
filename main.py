import logging

import telebot
import openai

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot("5953540475:AAGLYArxfKAURJlkhYBEhTiQxCszToKRA4g")
openai.api_key = "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"

@bot.message_handler(func=lambda message: True)

# bot.send_message(message.chat.id, text = "Welcome!")

def get_response(message):

    prompt = message.text
    
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt)

    print(response["choices"][0]["text"])

    bot.send_message(message.chat.id, text = response["choices"][0]["text"])
    # bot.send_message(message.chat.id, text = response["choices"][0]["text"])

bot.infinity_polling()

# # from teleBot import CommandHandler, Updater
# # from logging import basicConfig, getLogger, INFO

# # basicConfig(level=INFO)
# # log = getLogger()

# # def start(update, context):
# #     update.message.reply_text(
# #         "start this bot",
# #         parse_mode="markdown")

# # def help(update, context):
# #     update.message.reply_text(
# #         "help for this bot",
# #         parse_mode="markdown")

# # def main():
# #     updater = Updater(token=BOT_TOKEN, use_context=True)
# #     dispatcher = updater.dispatcher

# #     start_handler = CommandHandler("start", start)
# #     help_handler = CommandHandler("help", help)

# #     dispatcher.add_handler(start_handler)
# #     dispatcher.add_handler(help_handler)
# #     updater.start_polling()

# # if __name__ == '__main__':
# #     main()

# import os
import openai
# openai.organization = "org-mKz403VBDaLqeEP7mJB80GEa"
openai.api_key = "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"
openai.Model.list()