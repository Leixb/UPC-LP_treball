#!/usr/bin/env python3

"""
File: bot.py
Author: Aleix Boné Ribó
Email: aleix.bone@est.fib.upc.edu
"""

import logging
import pickle
import sys
import tempfile

# importing Telegram API
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

import matplotlib.pyplot as plt
import networkx as nx

sys.path.append("../cl")

# Disable interactive plotting
plt.ioff()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

SAVE_OPTS = {"format": "png", "bbox_inches": "tight", "transparent": True}

STATS_FILE = "stats.pckl"
GRAPH_FILE = "../cl/network_graph.pckl"

# loading the access token from token.txt
TOKEN = open("token.txt").read().strip()
AUTHOR = "Aleix Boné Ribó\naleix.bone@est.fib.upc.edu"


def read_pickle(filename: str):
    """Read object from pickle file."""
    with open(filename, "rb") as file:
        return pickle.load(file)


def write_pickle(obj: object, filename: str):
    """Save object in pickle file."""
    with open(filename, "wb") as file:
        return pickle.dump(obj, file)


try:
    RESPOSTES = read_pickle(STATS_FILE)
except FileNotFoundError:
    RESPOSTES = dict()
LOGGER.info(RESPOSTES)

GRAPH = read_pickle(GRAPH_FILE)

PREG_NODES = nx.get_node_attributes(GRAPH, "text")
RESP_NODES = nx.get_node_attributes(GRAPH, "opcions")


def add_resposta(id_pregunta, id_resposta):
    """Afegeix resposta a RESPOSTES."""
    if id_pregunta not in RESPOSTES:
        RESPOSTES[id_pregunta] = dict()
    if id_resposta not in RESPOSTES[id_pregunta]:
        RESPOSTES[id_pregunta][id_resposta] = 0
    RESPOSTES[id_pregunta][id_resposta] += 1


def save_respostes():
    """Guarda RESPOSTES amb pickle."""
    write_pickle(RESPOSTES, STATS_FILE)


# defining callback function for the /start command
def start(update: Update, context: CallbackContext):
    """Envia misstage de benvinguda."""
    update.message.reply_text(
        (
            "Benvingut al quizBot!\n"
            "/quiz <idEnquesta> per contestar una enquesta o /help per veure la llista de commandes"
        )
    )
    LOGGER.info("User start: %s", update.message.from_user.username)


def help_handler(update: Update, context: CallbackContext):
    """Mostra l'ajuda."""
    text = (
        "/start Inicia la conversa amb el Bot\n"
        "/help Mostra llista de possibles commandes\n"
        "/author Nom complet de l’autor del projecte i correu electrònic oficial de la facultat\n"
        "/quiz <idEnquesta> Inicia un intèrpret realitzant una enquesta\n"
        "/bar <idPreg> Retorna una diagrama de barres de les respostes a la pregunta\n"
        "/pie <idPreg> Retorna una gràfica de formatget de les respostes a la pregunta\n"
        "/report Retorna una taula amb el nombre de respostes obtingudes per cada valor\n"
    )
    update.message.reply_text(text)


def author(update: Update, context: CallbackContext):
    """Envia el nom de l'auto i el correu de la facultat."""
    update.message.reply_text(AUTHOR)


def quiz(update: Update, context: CallbackContext):
    """Inicia el quiz."""
    if len(context.args) == 0 or not GRAPH.has_node(context.args[0]):
        update.message.reply_text("Invalid quiz ID")
        return
    enq = context.args[0]
    context.user_data["enquesta"] = enq
    context.user_data["pregunta"] = list(GRAPH.edges(enq))[0][1]
    pregunta(update, context)


def bar_plot(update: Update, context: CallbackContext):
    """Handler de la commanda /bar."""
    if len(context.args) == 0:
        update.message.reply_text("La commanda /bar necesita el id de la pregunta")
        return
    preg = context.args[0]

    try:
        data = RESPOSTES[preg]
    except KeyError:
        update.message.reply_text("ID de pregunta invàlid")
        return

    plt.clf()
    plt.bar(range(len(data)), list(data.values()), align="center")
    plt.xticks(range(len(data)), list(data.keys()))

    send_plot(update)


def pie_plot(update: Update, context: CallbackContext):
    """Handler de la commanda /pie."""
    if len(context.args) == 0:
        update.message.reply_text("La commanda /pie necesita el id de la pregunta")
        return

    preg = context.args[0]

    try:
        data = RESPOSTES[preg]
    except KeyError:
        update.message.reply_text("ID de pregunta invàlid")
        return

    plt.clf()
    explode = [0.05] * len(data)
    plt.pie(
        list(data.values()),
        explode=explode,
        labels=list(data.keys()),
        autopct="%1.1f%%",
        shadow=True,
    )

    send_plot(update)


def report(update: Update, context: CallbackContext):
    """Handler de la commanda /report."""
    text = "*pregunta valor respostes*\n"
    for preg, respostes in RESPOSTES.items():
        for resposta, count in respostes.items():
            text += f"{preg} {resposta} {count}\n"

    update.message.reply_markdown(text)


def pregunta(update: Update, context: CallbackContext):
    """Mostra missatge de la pregunta actual."""
    enq = context.user_data["enquesta"]
    preg = context.user_data["pregunta"]

    if preg == "END":
        del context.user_data["enquesta"]
        del context.user_data["pregunta"]
        LOGGER.info(
            "Enquesta %s finalitzada (usuari:%s)",
            enq,
            update.message.from_user.username,
        )
        update.message.reply_text(f"{enq}> Gràcies pel teu temps!")
        return

    text_preg = PREG_NODES[preg]

    text = f"{enq}> {text_preg}\n"

    for _, r_id, data in GRAPH.edges(preg, data=True):
        try:
            if data["tipus"] == "item":
                context.user_data["resposta"] = r_id
                for opcio in RESP_NODES[r_id]:
                    text += f"{opcio['id']}: {opcio['text']}\n"
                update.message.reply_text(text)
                return
        except KeyError:
            pass


def seguent_pregunta(update: Update, context: CallbackContext, opcio):
    """Decicdeix quina es la seguent pregunta."""
    preg = context.user_data["pregunta"]
    enq = context.user_data["enquesta"]

    alternativa = None
    default = None

    for _, nxt_id, data in GRAPH.edges(preg, data=True):
        print(nxt_id, data)
        if data["tipus"] == "default" and enq in data["id_enq"]:
            default = nxt_id
        elif data["tipus"] == "alternativa" and data["id_opcio"] == opcio:
            alternativa = nxt_id

    LOGGER.info("default: %s", default)
    LOGGER.info("alternativa: %s", alternativa)

    if alternativa is None:
        if default is None:
            context.user_data["pregunta"] = context.user_data["fallback"]
            pregunta(update, context)
            return
        context.user_data["pregunta"] = default
        pregunta(update, context)
        return
    context.user_data["pregunta"] = alternativa
    context.user_data["fallback"] = default

    pregunta(update, context)


def send_plot(update: Update):
    """Guarda i envia la gràfica."""
    with tempfile.TemporaryFile(suffix=".png") as tmpfile:
        plt.savefig(tmpfile, **SAVE_OPTS)
        tmpfile.seek(0)
        update.message.reply_photo(tmpfile)


def message_handler(update: Update, context: CallbackContext):
    """Handler de missatges."""
    if "resposta" not in context.user_data:
        update.message.reply_text("Si us plau inicia l'enquesta amb /quiz <idEnquesta>")
        return
    r_id = context.user_data["resposta"]

    text = update.message.text.strip()

    for opcio in RESP_NODES[r_id]:
        if str(opcio["id"]) == text:
            add_resposta(context.user_data["pregunta"], opcio["id"])
            seguent_pregunta(update, context, opcio["id"])
            return

    update.message.reply_text("Resposta invàlida")


def error_handler(update: Update, context: CallbackContext):
    """Error handler."""
    logging.error(context.error)
    update.message.reply_text("S'ha produit un error")


def main():
    """Funcio principal."""

    # call main Telegram objects
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # handling callbacks functions to the commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_handler))
    dispatcher.add_handler(CommandHandler("author", author))
    dispatcher.add_handler(CommandHandler("quiz", quiz))
    dispatcher.add_handler(CommandHandler("bar", bar_plot))
    dispatcher.add_handler(CommandHandler("pie", pie_plot))
    dispatcher.add_handler(CommandHandler("report", report))

    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

    dispatcher.add_error_handler(error_handler)

    # starting the bot
    LOGGER.info("STARTED")

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    try:
        main()
    finally:
        save_respostes()
