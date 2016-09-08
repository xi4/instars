from peewee import *

sqlite_db = SqliteDatabase("chat.db")

def before_request_handler():
    sqlite_db.connect()

def after_request_handler():
    sqlite_db.close()

class BaseModel(Model):
    class Meta:
        database = sqlite_db

class User(BaseModel):
    id = PrimaryKeyField(primary_key=True)
    t_id = IntegerField()
    karma = IntegerField(default=50)
    gender = IntegerField(null=True)
    age = IntegerField(null=True)
    s_gender = IntegerField(null=True)
    s_age = IntegerField(null=True)
    chat = IntegerField(null=True)

class Gender(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()

class Age(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()


def get_user(id):
    try:
        return User.get(t_id=id)
    except:
        User.create(t_id=id)
        return User.get(t_id=id)
