from peewee import *


db = SqliteDatabase(None)
#db.init('test.sqlite3')


class User(Model):
    id = AutoField(primary_key=True)
    username = CharField(unique=True)
    password = CharField()
    
    class Meta:
        database = db
