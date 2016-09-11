# coding=utf-8
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
    xp = IntegerField(default=0)
    money = IntegerField(default=100)
    select_herb = IntegerField(null=True)

class Herb(BaseModel):
    id = IntegerField(primary_key=True)
    lvl = IntegerField()
    item_id = IntegerField()
    price = IntegerField()
    g_time = IntegerField()
    min=IntegerField()
    max=IntegerField()

class Herb_plant(BaseModel):
    id = PrimaryKeyField(primary_key=True)
    t_id = IntegerField()
    herb_id = IntegerField(null=True)
    end_time = DateTimeField(null=True)

class Inventory(BaseModel):
    id = IntegerField(primary_key=True)
    t_id = IntegerField()
    count = IntegerField()
    item_id = IntegerField()

class Animals(BaseModel):
    id = IntegerField(primary_key=True)
    item_id = IntegerField()
    price = CharField()
    g_time = IntegerField()

class Animal_product(BaseModel):
    id = IntegerField(primary_key=True)
    animal_id = IntegerField()
    product_id = IntegerField()
    min = IntegerField()
    max = IntegerField()

class Item(BaseModel):
    id = IntegerField(primary_key=True)
    txt = CharField()


User.create_table(True)
Herb.create_table(True)
Herb_plant.create_table(True)
Inventory.create_table(True)
Item.create_table(True)

if Herb.select().count()==0:
    Herb.create(txt="Укроп",lvl=0,price=10,g_time=1,min=1,max=10)
    Herb.create(txt="Петрушка",lvl=1,price=12,g_time=2,min=1,max=9)
    Herb.create(txt="Лук",lvl=2,price=15,g_time=3,min=1,max=8)
    Herb.create(txt="Хрен",lvl=2,price=15,g_time=3,min=1,max=8)
    Herb.create(txt="Мята",lvl=3,price=20,g_time=4,min=1,max=7)
    Herb.create(txt="Редис",lvl=3,price=20,g_time=4,min=1,max=7)
    Herb.create(txt="Капуста",lvl=4,price=25,g_time=5,min=1,max=6)
    Herb.create(txt="Базилик",lvl=4,price=25,g_time=5,min=1,max=6)
    Herb.create(txt="Морковь",lvl=5,price=30,g_time=6,min=1,max=5)
    Herb.create(txt="Свекла",lvl=5,price=30,g_time=6,min=1,max=5)
    Herb.create(txt="Щавель",lvl=6,price=35,g_time=7,min=1,max=4)
    Herb.create(txt="Картофель",lvl=6,price=35,g_time=7,min=1,max=4)
    Herb.create(txt="Горох",lvl=7,price=40,g_time=8,min=1,max=3)
    Herb.create(txt="Перец",lvl=7,price=40,g_time=8,min=1,max=3)
    Herb.create(txt="Томат",lvl=8,price=50,g_time=9,min=1,max=2)
    Herb.create(txt="Сельдерей",lvl=8,price=50,g_time=9,min=1,max=2)
    Herb.create(txt="Брокколи",lvl=9,price=10,g_time=1,min=1,max=1)
    Herb.create(txt="Огурец",lvl=9,price=10,g_time=1,min=1,max=1)
    Herb.create(txt="Кабачок",lvl=10,price=10,g_time=1,min=1,max=1)
    Herb.create(txt="Клубника",lvl=10,price=10,g_time=1,min=1,max=1)