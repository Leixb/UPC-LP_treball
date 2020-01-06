#!/usr/bin/env python3

# importing Telegram API
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

import pickle
import logging

import networkx as nx

import sys

sys.path.append("../cl")


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

STATS_FILE = "stats.pckl"
GRAPH_FILE = "../cl/network_graph.pckl"

# loading the access token from token.txt
TOKEN = open("token.txt").read().strip()
AUTHOR = "Aleix Boné Ribó\naleix.bone@est.fib.upc.edu"


def read_pickle(filename: str):
    with open(filename, "rb") as file:
        return pickle.load(file)


def write_pickle(obj: object, filename: str):
    with open(filename, "wb") as file:
        return pickle.dump(obj, file)


class Respostes:
    @staticmethod
    def add_resposta(id_pregunta, id_resposta):
        if id_pregunta not in Respostes.data:
            Respostes.data[id_pregunta] = dict()
        if id_resposta not in Respostes.data[id_pregunta]:
            Respostes.data[id_pregunta][id_resposta] = 0
        Respostes.data[id_pregunta][id_resposta] += 1

    @staticmethod
    def load_stats():
        try:
            Respostes.data = read_pickle(STATS_FILE)
        except FileNotFoundError:
            Respostes.data = dict()

    @staticmethod
    def save_stats():
        write_pickle(Respostes.data, STATS_FILE)


class Graph:

    G = read_pickle(GRAPH_FILE)


# defining callback function for the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Benvingut al quizBot!\n /quiz <idEnquesta> per contestar una enquesta o /help per veure la llista de commandes"
    )


def help_handler(update: Update, context: CallbackContext):
    text = """/start Inicia la conversa amb el Bot
/help Mostra llista de possibles commandes
/author Nom complet de l’autor del projecte i correu electrònic oficial de la facultat
/quiz <idEnquesta> Inicia un intèrpret realitzant una enquesta
/bar <idPregunta> Retorna una gràfica de barres mostrant un diagrama de barres de les respostes a la pregunta donada
/pie <idPregunta> Retorna una gràfica de formatget amb el percentatge de les respostes a la pregunta donada
/report Retorna una taula amb el nombre de respostes obtingudes per cada valor de cada pregunta
"""
    update.message.reply_text(text)


def author(update: Update, context: CallbackContext):
    update.message.reply_text(AUTHOR)


def quiz(update: Update, context: CallbackContext):
    update.message.reply_text("WIP")
    Respostes.add_resposta('P1', 12)
    Respostes.add_resposta('P1', 12)
    Respostes.add_resposta('P1', 2)
    Respostes.add_resposta('P1', 2)
    Respostes.add_resposta('P2', 3)
    Respostes.add_resposta('P3', 1)


def bar(update: Update, context: CallbackContext):
    update.message.reply_text("WIP")


def pie(update: Update, context: CallbackContext):
    update.message.reply_text("WIP")


def report(update: Update, context: CallbackContext):
    update.message.reply_text("WIP")
    for pregunta, respostes in Respostes.data.items():
        for resposta, count in respostes.items():
            print(pregunta, resposta, count)


def main():

    Respostes.load_stats()
    LOGGER.info(Respostes.data)

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
    try:
        main()
    finally:
        Respostes.save_stats()

