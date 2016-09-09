# coding=utf-8
import json
import random

from telebot import *
import conf
import dbw
import util

bot = TeleBot(conf.apitoken)


def menu():
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text="Работа", callback_data="work"))
    return key


def get_type_work():
    key = types.InlineKeyboardMarkup()
    works = dbw.work()
    if works:
        for w in works:
            key.add(types.InlineKeyboardButton(text=w.name, callback_data="work_" + str(w.id)))
    key.add(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    return key


def get_w_list(id, params):
    dbw.ref_task(id, params)
    w = dbw.work_get(params)
    key = types.InlineKeyboardMarkup()
    tasks = dbw.task(id, params)
    if len(tasks) > 0:
        for t in tasks:
            if t.type_w == 0:
                key.add(
                    types.InlineKeyboardButton(text=w.go, callback_data="work_add_" + str(params) + "_" + str(t.id)))
            else:
                name = dbw.type_w_get_name(t.type_w)
                if t.dateEnd is None:
                    key.add(types.InlineKeyboardButton(text="Собрать " + name, callback_data="pick_" + str(t.id)))
                else:
                    time = dbw.getLastTime(t.dateEnd)
                    key.add(types.InlineKeyboardButton(text=name + " " + str(time), callback_data=""))
    key.add(types.InlineKeyboardButton(text="Купить " + w.text + " Цена:" + str(100 * (len(tasks) + 1)),
                                       callback_data="buy_t_" + str(params) + "_" + str(100 * (len(tasks) + 1))))


@bot.message_handler(commands=["start", "help"])
def start_help(message):
    user = dbw.user(message.chat)
    lvl = util.get_lvl(user.xp)
    proc = util.get_procent(lvl, user.xp)

    bot.send_message(text="Ваш уровень: " + str(lvl) + " (" + str(proc) + "%) " + "Ваш баланс:" + str(user.money),
                     chat_id=message.chat.id, reply_markup=menu())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = dbw.user(call.message.chat)
    key = types.InlineKeyboardMarkup()
    lvl = util.get_lvl(user.xp)
    proc = util.get_procent(lvl, user.xp)
    if call.message:
        params = call.data.split("_")

        if params[0] == "menu":
            bot.edit_message_text(text="Ваш баланс:" + str(user.money), chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=menu())

        if params[0] == "work":
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton(text="Ферма", callback_data="farm"))
            bot.edit_message_text(
                text="Ваш уровень: " + str(lvl) + " (" + str(proc) + "%) " + "Ваш баланс:" + str(user.money),
                chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)

        if params[0] == "farm":
            pl_count = dbw.get_plants_count_user(user)
            if len(params) == 1:
                if pl_count > 0:
                    dbw.ref_farm(user)
                    plants = dbw.get_plants_user(user)
                    for plant in plants:
                        if plant.herb_id is not None:
                            name = dbw.get_herb_name(plant.herb_id)
                            if plant.end_time is not None:
                                left_time = dbw.getLastTime(plant.end_time)
                                key.add(types.InlineKeyboardButton(text=name + " Осталось: " + str(left_time),
                                                                   callback_data="farm"))
                            else:
                                key.add(types.InlineKeyboardButton(text="Собрать " + name,
                                                                   callback_data="farm_get_" + str(plant.id)))
                        else:
                            if user.select_herb:
                                name = dbw.get_herb_name(user.select_herb)
                                key.add(types.InlineKeyboardButton(text="Посадить " + name,
                                                                   callback_data="farm_set_" + str(
                                                                       plant.id) + "_" + str(user.select_herb)))
                            else:
                                key.add(types.InlineKeyboardButton(text="Посадить",
                                                                   callback_data="farm_set_" + str(plant.id)))
                if pl_count < 10:
                    key.add(types.InlineKeyboardButton(text="Купить грядку за" + str(100 * pl_count),
                                                       callback_data="farm_buy"))
                bot.edit_message_text(
                    text="Ваш уровень: " + str(lvl) + " (" + str(proc) + "%) " + "Ваш баланс:" + str(user.money),
                    chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)
            if len(params) > 2:
                # покупка грядок
                if params[1] == "buy":
                    if pl_count <= 10:
                        if user.money >= (100 * pl_count):
                            user.money -= 100 * pl_count
                            user.save()
                            newplant = dbw.buy_herb_plant(user)
                            text = "Грядка успешно куплена \n"
                            if user.select_herb:
                                name = dbw.get_herb_name(user.select_herb)
                                key.add(types.InlineKeyboardButton(text="Посадить " + name,
                                                                   callback_data="farm_set_" + str(
                                                                       newplant.id) + "_" + str(user.select_herb)))
                            else:
                                key.add(types.InlineKeyboardButton(text="Посадить",
                                                                   callback_data="farm_set_" + str(newplant.id)))
                        else:
                            text = "Не достаточно денег для покупки \n"
                        bot.edit_message_text(
                            text=text + "Ваш уровень: " + str(lvl) + " (" + str(proc) + "%) " + "Ваш баланс:" + str(
                                user.money), chat_id=call.message.chat.id, message_id=call.message.message_id,
                            reply_markup=key)
                if params[1] =="get":
                    if params[2] is not None:
                        plant = dbw.get_plant(params[2])
                        herb = dbw.get_herb(plant.herb_id)
                        xp = util.get_xp(lvl,herb.lvl)
                        user.xp = user.xp + xp
                        count_herb = random.randint(herb.min,herb.max)
                        user.money += count_herb*10
                        user.save()
                        plant.herb_id = None
                        plant.save()


if __name__ == '__main__':
    bot.polling(none_stop=True)
