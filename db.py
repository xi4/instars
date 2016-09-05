from peewee import *

sqlite_db = SqliteDatabase("my.db")

class BaseModel(Model):
    class Meta:
        database = sqlite_db

class User(BaseModel):
    id = IntegerField(primary_key=True)
    t_id = IntegerField()
    username = CharField(max_length=255)

class Work(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()

class Resours(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    mincount = IntegerField()
    maxcount = IntegerField()

class Item(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    strength = IntegerField()