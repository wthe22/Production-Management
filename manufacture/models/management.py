from peewee import *
import datetime


db = SqliteDatabase(None)
#db.init('test.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Item(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    details = TextField(null=True)

    def __str__(self):
        return self.name


class Recipe(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    details = TextField(null=True)
    duration = IntegerField(default=0, null=True)

    def __str__(self):
        return self.name


class RecipeInput(BaseModel):
    recipe = ForeignKeyField(Recipe, on_delete='CASCADE')
    item = ForeignKeyField(Item, on_delete='RESTRICT')
    quantity = IntegerField(default=0)
    
    class Meta:
        primary_key = CompositeKey('recipe', 'item')
    
    def __str__(self):
        return "{}: {} {}".format(self.recipe, self.quantity, self.item)


class RecipeOutput(BaseModel):
    recipe = ForeignKeyField(Recipe, on_delete='CASCADE')
    item = ForeignKeyField(Item, on_delete='RESTRICT')
    quantity = IntegerField(default=0)
    
    class Meta:
        primary_key = CompositeKey('recipe', 'item')
    
    def __str__(self):
        return "{}: {} {}".format(self.recipe, self.quantity, self.item)


class Stock(BaseModel):
    id = AutoField(primary_key=True)
    item = ForeignKeyField(Item, on_delete='RESTRICT')
    description = CharField()
    quantity = IntegerField(default=0)
    
    def __str__(self):
        return "{} {}".format(self.quantity, self.item)


class Machine(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    details = TextField(null=True)
    quantity = IntegerField(default=0)
    
    def __str__(self):
        return "{}".format(self.name, self.quantity)


class MachineRecipe(BaseModel):
    machine = ForeignKeyField(Machine, on_delete='CASCADE')
    recipe = ForeignKeyField(Recipe, on_delete='CASCADE')
    
    class Meta:
        primary_key = CompositeKey('machine', 'recipe')
    
    def __str__(self):
        return "{}: {}".format(self.machine, self.recipe)


class Task(BaseModel):
    id = AutoField(primary_key=True)
    recipe = ForeignKeyField(Recipe, on_delete='CASCADE')
    cycles = IntegerField()
    description = TextField()
    
    def __str__(self):
        return "{} x{}".format(self.recipe, self.cycles)


class Notification(BaseModel):
    id = AutoField(primary_key=True)
    time = IntegerField()
    description = CharField()
    details = TextField(null=True)

    def __str__(self):
        time = ""
        if not self.time is None:
            time = str(datetime.timedelta(seconds=self.time))
        return "[T+{:0>8}] {}".format(time, self.description)
