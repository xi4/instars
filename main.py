# coding=utf-8
import json

from telebot import *
import conf
import dbw

bot = TeleBot(conf.apitoken)

def menu():
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text="Работа",callback_data="work"))
    return key
def get_type_work():
    key = types.InlineKeyboardMarkup()
    works = dbw.work()
    if works:
        for w in works:
            key.add(types.InlineKeyboardButton(text=w.name,callback_data="work_"+str(w.id)))
    key.add(types.InlineKeyboardButton(text="Меню",callback_data="menu"))
    return key
def get_w_list(id,params):
    user = dbw.user(id)
    w = dbw.work_get(params)
    key = types.InlineKeyboardMarkup()
    tasks = dbw.task(id,params)
    if len(tasks)>0:
        for t in tasks:
            if t.type_w==0:
                key.add(types.InlineKeyboardButton(text=w.go,callback_data=""))
            else:
                name = dbw.type_w_get_name(t.type_w)
                key.add(types.InlineKeyboardButton(text=name+" "+))
    key.add(types.InlineKeyboardButton(text="Купить "+w.text+" Цена:"+str(100*(len(tasks)+1)),callback_data="buy_t_"+str(params)))


@bot.message_handler(commands=["start","help"])
def start_help(message):
    user = dbw.user(message.chat)
    bot.send_message(text="Ваш баланс:"+str(user.money),chat_id=message.chat.id,reply_markup=menu())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = dbw.user(call.message.chat)
    if call.message:
        params = call.data.split("_")

        if params[0]=="menu":
            bot.edit_message_text(text="Ваш баланс:"+str(user.money),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=menu())

        if params[0]=="work":
            key=[]
            if len(params)>1:
                key = get_w_list(params[1])
            else:
                key = get_type_work()
            bot.edit_message_text(text="Ваш баланс:"+str(user.money),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=key)
















if __name__ == '__main__':
    bot.polling(none_stop=True)