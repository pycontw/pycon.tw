from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from django.conf import settings
from django.db.models import Q
from proposals.models import TalkProposal, TutorialProposal

import logging
logger = logging.getLogger(__name__)

def get(bot, update):
    talk = TalkProposal.objects.all()
    tutorial = TutorialProposal.objects.all()
    bot.sendMessage(update.message.chat_id,
        text='talk: {}\ntutorial: {}'.format(len(talk),len(tutorial))
        )

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")
    dp = DjangoTelegramBot.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("get", get))
    dp.add_handler(MessageHandler([Filters.text], echo))
    dp.add_error_handler(error)
