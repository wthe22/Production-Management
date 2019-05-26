from peewee import *


db = SqliteDatabase(None)


class User(Model):
    id = AutoField(primary_key=True)
    username = CharField(unique=True)
    password = CharField()
    
    class Meta:
        database = db


def get_tables():
    return [
        User,
    ]
