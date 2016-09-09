import db
import datetime

def user(u):
    try:
        user = db.User.get(t_id=u.id)
        if user.username!=u.username:
            user.username = u.username
            user.save()
        return user
    except db.User.DoesNotExist:
        return db.User.create(t_id=u.id,username=u.username)

def work():
    try:
        return db.Work.select()
    except db.Work.DoesNotExist:
        return False

def type_w(type):
    try:
        return db.Type_w.select().where(db.Type_w.type_w==type).order_by(db.Type_w.price)
    except db.Type_w.DoesNotExist:
        return False

def resours_get(id):
    return db.Resours.get(db.Resours.id == id)

def task(id,type):
    try:
        db.Tasks.select().where(db.Tasks.t_id==id,db.Tasks.id_work==type).order_by(db.Tasks.dateEnd)
    except db.Tasks.DoesNotExist:
        return False


def work_get(params):
    return db.Work.get(db.Work.id==params)


def type_w_get_name(type_w):
    resoursId = db.Type_w.select().where(db.Type_w.id==type_w).get()
    return db.Resours.get(db.Resours.id==resoursId).name

def ref_task(id,params):
    tasks = db.Tasks.select().where(db.Tasks.t_id==id,db.Tasks.id_work==params,db.Tasks.dateEnd!=None)
    for task in tasks:
        nowtime = datetime.datetime.now()
        endtime = task.dateEnd
        if nowtime>endtime:
            task.dateEnd = None
            task.save()

def getLastTime(newtime):
    nowtime = datetime.datetime.now()
    return newtime-nowtime


def get_plants_user(user):
    return db.Herb_plant.select().where(db.Herb_plant.t_id==user.t_id)


def ref_farm(user):
    for p in get_plants_user(user):
        t_now = datetime.datetime.now()
        if t_now>p.end_time:
            p.end_time=None
            p.save()


def get_plants_count_user(user):
    return db.Herb_plant.select().where(db.Herb_plant.t_id==user.t_id).count()


def get_herb_name(herb_id):
    return db.Herb.get(db.Herb.id==herb_id).txt


def buy_herb_plant(user):
    db.Herb_plant.create(t_id = user.t_id)


def get_plant(param):
    return db.Herb_plant.get(id=param)


def get_herb(herb_id):
    return db.Herb.get(id=herb_id)