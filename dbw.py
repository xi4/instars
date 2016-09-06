import db

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