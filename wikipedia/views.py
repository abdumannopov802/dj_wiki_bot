from django.shortcuts import render
from django.http import HttpResponse
from .webhook import bot
from .functions import search_wikipedia
from telebot import types
import requests
import logging
import wikipedia

def base(request):
    return HttpResponse('Welcome')


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('help', callback_data='help')
    btn_2 = types.InlineKeyboardButton('Search here', callback_data='search')
    markup.add(btn_1, btn_2)

    if message.from_user.last_name != None:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} {message.from_user.last_name} 😀 \n\nIn this weather bot you can get information existing on wikipedia.org! \nIf you need /help click here.""", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} 😀 \n\nIn this weather bot you can get information existing on wikipedia.org! \nIf you need /help click here.""", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'help':
        bot.reply_to(call.message, f"""The following commands are availabe: \n\n/start -> Welcome message \n/help -> Show Available Commands""")
    if call.data == 'search':
        bot.reply_to(call.message, "Nima haqida malumot qidiryapsiz?")


@bot.message_handler(func=lambda message: True)
def wikipedia_message(message):
    query = message.text
    title, extract, image_url = search_wikipedia(query)
    if title and extract:
        response_text = f"{title}\n\n{extract}"
        if image_url:
            bot.send_photo(message.chat.id, image_url, caption=response_text)
        else:
            bot.reply_to(message, response_text)
    else:
        bot.reply_to(message, "Sorry, no Wikipedia page found for that query.")
