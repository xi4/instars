# coding=utf-8
from telebot import *
import conf
import db

bot = TeleBot(conf.apikey)

def menu():
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text="Поиск",callback_data="search"))
    key.add(types.InlineKeyboardButton(text="Настройки",callback_data="setting"))
    return key
def get_setting():
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text="Выбрать пол",callback_data="select_gender"))
    key.add(types.InlineKeyboardButton(text="Выбрать возраст",callback_data="select_age"))
    key.add(types.InlineKeyboardButton(text="Выбрать пол собеседника",callback_data="select_gender_chat"))
    key.add(types.InlineKeyboardButton(text="Выбрать возраст собеседника",callback_data="select_age_chat"))
    key.add(types.InlineKeyboardButton(text="Меню",callback_data="menu"))
    return key
@bot.message_handler(commands=["start","help"])
def start_help(message):
    bot.send_message(message.chat.id,"Сделайте выбор",reply_markup=menu())


@bot.message_handler(content_types=["text"])
def chat(message):
    one = db.get_user(message.chat.id)
    if one.chat is not None:
        two = db.get_user(one.chat)
        if two.chat is one.id:
            bot.send_message(two.t_id,str(one.id)+":"+message.text)
        else:
            one.chat = None
            one.save()

@bot.callback_query_handler(func=lambda call: True)
def logik(call):
    user = db.get_user(call.message.chat.id)
    key = types.InlineKeyboardMarkup()
    if call.message:

        params = call.data.split("_")

        if call.data=="setting":
            bot.edit_message_text(text="Настройки",chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=get_setting())
        if call.data=="menu":
            bot.edit_message_text(text="Сделайте выбор",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=menu())
        if call.data=="select_gender":
            for g in db.Gender.select():
                key.add(types.InlineKeyboardButton(text=g.name,callback_data="setgender_"+g.id))
            bot.edit_message_text(text="Сделайте выбор",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)
        if call.data=="select_age":
            for g in db.Age.select():
                key.add(types.InlineKeyboardButton(text=g.name,callback_data="setage_"+g.id))
            bot.edit_message_text(text="Сделайте выбор",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)
        if call.data=="select_gender_chat":
            for g in db.Gender.select():
                key.add(types.InlineKeyboardButton(text=g.name,callback_data="setgenderchat_"+g.id))
            bot.edit_message_text(text="Сделайте выбор",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)
        if call.data=="select_age_chat":
            for g in db.Age.select():
                key.add(types.InlineKeyboardButton(text=g.name,callback_data="setagechat_"+g.id))
            bot.edit_message_text(text="Сделайте выбор",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)

        if params[0]=="setgender":
            user.gender = params[1]
            user.save()
            bot.edit_message_text(text="Изменения успешно. \n Настройки",chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=get_setting())
        if params[0]=="setage":
            user.age=params[1]
            user.save()
            bot.edit_message_text(text="Изменения успешно. \n Настройки",chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=get_setting())
        if params[0]=="setgenderchat":
            user.s_gender=params[1]
            user.save()
            bot.edit_message_text(text="Изменения успешно. \n Настройки",chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=get_setting())
        if params[0]=="setagechat":
            user.s_age=params[1]
            user.save()
            bot.edit_message_text(text="Изменения успешно",chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=get_setting())


if __name__ == '__main__':
    bot.polling(none_stop=True)