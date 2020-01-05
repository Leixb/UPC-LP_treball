#!/usr/bin/env python3

# importing Telegram API
from telegram.ext import Updater, CommandHandler

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# loading the access token from token.txt
TOKEN = open("token.txt").read().strip()
AUTHOR = "***REMOVED***\n***REMOVED***"

# defining callback function for the /start command
def start(update, context):
    update.message.reply_text("Benvingut al quizBot!\n /quiz <idEnquesta> per contestar una enquesta o /help per veure la llista de commandes")


def help_handler(update, context):
    text = '''/start Inicia la conversa amb el Bot
/help Mostra llista de possibles commandes
/author Nom complet de l’autor del projecte i correu electrònic oficial de la facultat
/quiz <idEnquesta> Inicia un intèrpret realitzant una enquesta
/bar <idPregunta> Retorna una gràfica de barres mostrant un diagrama de barres de les respostes a la pregunta donada
/pie <idPregunta> Retorna una gràfica de formatget amb el percentatge de les respostes a la pregunta donada
/report Retorna una taula amb el nombre de respostes obtingudes per cada valor de cada pregunta
'''
    update.message.reply_text(text)


def author(update, context):
    update.message.reply_text(AUTHOR)


def quiz(update, context):
    update.message.reply_text("WIP")


def bar(update, context):
    update.message.reply_text("WIP")


def pie(update, context):
    update.message.reply_text("WIP")


def report(update, context):
    update.message.reply_text("WIP")


def main():
    # call main Telegram objects
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # handling callbacks functions to the commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_handler))
    dp.add_handler(CommandHandler("author", author))
    dp.add_handler(CommandHandler("quiz", quiz))
    dp.add_handler(CommandHandler("bar", bar))
    dp.add_handler(CommandHandler("pie", pie))
    dp.add_handler(CommandHandler("report", report))

    # starting the bot
    LOGGER.info("STARTED")

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()


# /start inicia la conversa amb el Bot.
# /help el Bot ha de contestar amb una llista de totes les possibles comandes i una breu documentació sobre el seu propòsit i ús.
# /author el Bot ha d’escriure el nom complet de l’autor del projecte i seu correu electrònic oficial de la facultat.
# /quiz <idEnquesta> el Bot ha de iniciar un intèrpret similar al de la secció anterior realitzant l’enquesta. A la secció següent s’amplia la informació.
# /bar <idPregunta> el Bot ha de tornar una gràfica de barres mostrant un diagrama de barres de les respostes a la pregunta donada. A les seccions següents s’amplia la informació.
# /pie <idPregunta> el Bot ha de tornar una gràfica de formatget amb el percentatge de les respostes a la pregunta donada. A les seccions següents s’amplia la informació.
# /report el Bot ha de tornar quelcom tipus taula amb el nombre de respostes obtingudes per cada valor de cada pregunta. A les seccions següents s’amplia la informació.
