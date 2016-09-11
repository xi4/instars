import random

import db
import datetime
import game_conf
import util


def user(u):
    try:
        user = db.User.get(t_id=u.id)
        if user.username != u.username:
            user.username = u.username
            user.save()
        return user
    except db.User.DoesNotExist:
        return db.User.create(t_id=u.id, username=u.username)


def getLastTime(newtime):
    nowtime = datetime.datetime.now()
    h,m,s = convert_timedelta(newtime - nowtime)
    return (str(h)+":"+str(m)+":"+str(s))

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

def get_plants_user(user):
    return db.Herb_plant.select().where(db.Herb_plant.t_id == user.t_id)


def ref_farm(user):
    for p in get_plants_user(user):
        t_now = datetime.datetime.now()
        if p.end_time:
            if t_now > p.end_time:
                p.end_time = None
                p.save()


def get_plants_count_user(user):
    return db.Herb_plant.select().where(db.Herb_plant.t_id == user.t_id).count()


def get_herb_name(herb_id):
    return db.Herb.get(db.Herb.id == herb_id).txt


def buy_herb_plant(user):
    db.Herb_plant.create(t_id=user.t_id)


def get_plant(param):
    return db.Herb_plant.get(id=param)


def get_herb(herb_id):
    return db.Herb.get(id=herb_id)


def get_complet_plant(user):
    return db.Herb_plant.select().where(db.Herb_plant.t_id == user.t_id, db.Herb_plant.end_time == None, db.Herb_plant.herb_id!=None)


def get_complet_plant_count(user):
    return db.Herb_plant.select().where(db.Herb_plant.t_id == user.t_id, db.Herb_plant.end_time == None, db.Herb_plant.herb_id!=None).count()


def get_user_from_id(t_id):
    return db.User.get(t_id=t_id)


def to_inventory(t_id, type, count, item_id):
    try:
        inv_item = db.Inventory.get(t_id=t_id,item_id=item_id)
        inv_item.count += count
        inv_item.save()
    except:
        db.Inventory.create(t_id=t_id,count=count,item_id=item_id)

def farm_plant(plant):
    user = get_user_from_id(plant.t_id)
    herb = get_herb(plant.herb_id)
    xp = util.get_xp(util.get_lvl(user.xp), herb.lvl)
    user.xp = user.xp + xp
    user.save()
    count_herb = random.randint(herb.min, herb.max)
    to_inventory(plant.t_id,1,count_herb,herb.id)
    plant.herb_id = None
    plant.save()
    return count_herb


def set_herb_to_plant(plant, herb):
    plant.herb_id = herb.id
    plant.end_time = datetime.datetime.now()+datetime.timedelta(minutes=herb.g_time)
    plant.save()


def get_herbs_from_user_lvl(lvl):
    return db.Herb.select().where(db.Herb.lvl<=lvl)


def get_inventory_count(t_id):
    return db.Inventory.select().where(db.Inventory.t_id==t_id).count()


def get_inventory_user(t_id):
    return db.Inventory.select().where(db.Inventory.t_id==t_id)


def get_item_from_inventory(inv_id):
    return db.Inventory.get(id=inv_id)


def fastsell(item):
    if item.type==1:
        herb = get_herb(item.item_id)
        user = get_user_from_id(item.t_id)
        user.money +=(herb.lvl*item.count)
        item.delete_instance()
        user.save()