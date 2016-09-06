from peewee import *

sqlite_db = SqliteDatabase("my.db")

def before_request_handler():
    sqlite_db.connect()

def after_request_handler():
    sqlite_db.close()

class BaseModel(Model):
    class Meta:
        database = sqlite_db

class User(BaseModel):
    t_id = IntegerField()
    username = CharField(max_length=255)
    money = IntegerField(default=100)

class Work(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    text = CharField()
    go = CharField()

class Type_w(BaseModel ):
    id = IntegerField(primary_key=True)
    type_w = IntegerField()
    time = DateTimeField()
    price = IntegerField()
    r_ret = IntegerField()

class Resours(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    mincount = IntegerField()
    maxcount = IntegerField()
    minprice = IntegerField()

class Tasks(BaseModel):
    t_id = IntegerField()
    type_w = IntegerField()
    dateEnd = DateTimeField()
    id_work = IntegerField()