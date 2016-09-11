# coding=utf-8
import json
import random

from telebot import *
import conf
import dbw
import util
import game_conf

bot = TeleBot(conf.apitoken)


def menu():
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text="Работа", callback_data="work"))
    key.add(types.InlineKeyboardButton(text="Инвентарь", callback_data="inventory"))
    return key


def get_farm(user, pl_count):
    key = types.InlineKeyboardMarkup()
    if pl_count > 0:
        dbw.ref_farm(user)
        if dbw.get_complet_plant_count(user) > 0:
            key.add(types.InlineKeyboardButton(text="Собрать всё", callback_data="farm_get_all"))
        plants = dbw.get_plants_user(user)
        for plant in plants:
            if plant.herb_id is not None:
                name = dbw.get_herb_name(plant.herb_id)
                if plant.end_time is not None:
                    left_time = dbw.getLastTime(plant.end_time)
                    key.add(types.InlineKeyboardButton(text=name.encode("utf-8") + " осталось: " + str(left_time),
                                                       callback_data="farm"))
                else:
                    key.add(types.InlineKeyboardButton(text="Собрать " + name.encode("utf-8"),
                                                       callback_data="farm_get_one_" + str(plant.id)))
            else:
                if user.select_herb:
                    name = dbw.get_herb_name(user.select_herb)
                    key.add(types.InlineKeyboardButton(text="Посадить " + name.encode("utf-8"),
                                                       callback_data="farm_set_" + str(
                                                           plant.id) + "_" + str(user.select_herb)))
                else:
                    key.add(types.InlineKeyboardButton(text="Посадить",
                                                       callback_data="farm_set_" + str(plant.id)))
    if pl_count < game_conf.max_plant:
        key.add(types.InlineKeyboardButton(text="Купить грядку за " + str(100 * pl_count),
                                           callback_data="farm_buy"))
    key.add(types.InlineKeyboardButton(text="Работы",callback_data="work"))
    return key


def get_inventory(user):
    key = types.InlineKeyboardMarkup()
    inv_count = dbw.get_inventory_count(user.t_id)
    if inv_count > 0:
        for item in dbw.get_inventory_user(user.t_id):
            if item.type == 1:
                name = dbw.get_herb_name(item.item_id)
                key.add(types.InlineKeyboardButton(text=name + u" " + str(item.count),
                                                   callback_data="inventory_action_" + str(item.id)))
    key.add(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    return key


@bot.message_handler(commands=["start", "help"])
def start_help(message):
    user = dbw.user(message.chat)

    bot.send_message(text=u"Ваш уровень: " + str(util.get_lvl(user.xp)) + u" (" + str(
        util.get_procent(util.get_lvl(user.xp), user.xp)) + u"%) Ваш баланс:" + str(user.money),
                     chat_id=message.chat.id, reply_markup=menu())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = dbw.user(call.message.chat)
    key = types.InlineKeyboardMarkup()
    if call.message:
        params = call.data.split("_")

        if params[0] == "menu":
            bot.edit_message_text(text=u"Ваш уровень: " + str(util.get_lvl(user.xp)) + u" (" + str(
                util.get_procent(util.get_lvl(user.xp), user.xp)) + u"%) Ваш баланс:" + str(user.money),
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=menu())

        if params[0] == "work":
            key.add(types.InlineKeyboardButton(text="Ферма", callback_data="farm"))
            key.add(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
            bot.edit_message_text(
                text=u"Ваш уровень: " + str(util.get_lvl(user.xp)) + u" (" + str(
                    util.get_procent(util.get_lvl(user.xp), user.xp)) + u"%) Ваш баланс:" + str(user.money),
                chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)
        # работа с инвентарем
        if params[0] == "inventory":
            text = ""
            if len(params)>2:
                # выбор предмета
                if params[1]=="action":
                    key.add(types.InlineKeyboardButton(text="Быстрая продажа",callback_data="inventory_fastsell_"+str(params[2])))
                key.add(types.InlineKeyboardButton(text="Инвентарь",
                                                   callback_data="inventory"))

                # простая продажа предмета
                if params[1]=="fastsell":
                    old_money = user.money
                    item = dbw.get_item_from_inventory(params[2])
                    dbw.fastsell(item)
                    user = dbw.get_user_from_id(item.t_id)
                    new_money = user.money
                    text= u"Продано на "+str(new_money-old_money)+u"\n"
                    key = get_inventory(user)
            else:
                key = get_inventory(user)
            bot.edit_message_text(
                text=text+u"Ваш уровень: " + str(util.get_lvl(user.xp)) + u" (" + str(
                    util.get_procent(util.get_lvl(user.xp), user.xp)) + u"%) Ваш баланс:" + str(user.money),
                chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)

        if params[0] == "farm":
            text = ""
            pl_count = dbw.get_plants_count_user(user)
            if len(params) >= 2:
                # покупка грядок
                if params[1] == "buy":
                    if pl_count <= game_conf.max_plant:
                        if user.money >= (100 * pl_count):
                            user.money -= 100 * pl_count
                            user.save()
                            dbw.buy_herb_plant(user)
                            text = u"Грядка успешно куплена \n"
                            key = get_farm(user, dbw.get_plants_count_user(user))
                        else:
                            text = u"Не достаточно денег для покупки \n"
                if params[1] == "get":
                    # сбор с грядки собрать один
                    if params[2] == "one":
                        if params[3] is not None:
                            plant = dbw.get_plant(params[3])
                            name = dbw.get_herb_name(plant.herb_id)
                            count = dbw.farm_plant(plant)
                            text = u"Получено:\n " + str(count) + u" " + name + u"\n"

                    # собрать все
                    if params[2] == "all":
                        all_c = u""
                        for plant in dbw.get_complet_plant(user):
                            if plant.herb_id != None:
                                name = dbw.get_herb_name(plant.herb_id)
                                c = dbw.farm_plant(plant)
                                all_c += str(c) + u" " + name + u"\n"
                        text = u"Получено:\n" + all_c
                    user = dbw.user(call.message.chat)
                    key = get_farm(user, pl_count)
                # посадка
                if params[1] == "set":
                    if len(params) == 4:
                        herb = dbw.get_herb(params[3])
                        if user.money >= herb.price:
                            text = herb.txt + u" посажен \n"
                            user.money -= herb.price
                            user.save()
                            dbw.set_herb_to_plant(dbw.get_plant(params[2]), herb)
                            key = get_farm(user, pl_count)
                        else:
                            text = u"Для посадки " + herb.txt + u" не хватает денег \n"
                            key = get_farm(user, pl_count)
                    else:
                        for herb in dbw.get_herbs_from_user_lvl(util.get_lvl(user.xp)):
                            key.add(types.InlineKeyboardButton(text=herb.txt+u" Цена: "+str(herb.price),
                                                               callback_data="farm_set_" + str(params[2]) + "_" + str(
                                                                   herb.id)))
            else:
                key = get_farm(user, pl_count)
            bot.edit_message_text(
                text=text + u"Ваш уровень: " + str(util.get_lvl(user.xp)) + u" (" + str(
                    util.get_procent(util.get_lvl(user.xp), user.xp)) + u"%) Ваш баланс: " + str(user.money),
                chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=key)


if __name__ == '__main__':
    bot.polling(none_stop=True)
