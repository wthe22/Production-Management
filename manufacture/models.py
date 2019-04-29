from peewee import *


db = SqliteDatabase(None)
#db.init('test.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Item(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    description = TextField(null=True)

    def __str__(self):
        return self.name


class Recipe(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    description = TextField(null=True)
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
    comment = CharField()
    description = TextField(null=True)
    quantity = IntegerField(default=0)
    
    def __str__(self):
        return "{} {}".format(self.quantity, self.item)


class Machine(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    description = TextField(null=True)
    quantity = IntegerField(default=0)
    
    def __str__(self):
        return "{} {}".format(self.quantity, self.item)


class MachineRecipe(BaseModel):
    machine = ForeignKeyField(Machine, on_delete='CASCADE')
    recipe = ForeignKeyField(Recipe, on_delete='CASCADE')
    
    class Meta:
        primary_key = CompositeKey('machine', 'recipe')
    
    def __str__(self):
        return "{}: {}".format(self.machine, self.recipe)


class Task(BaseModel):
    id = AutoField(primary_key=True)
    machine = ForeignKeyField(Machine, on_delete='CASCADE')
    recipe = ForeignKeyField(Recipe, on_delete='CASCADE')
    description = TextField(null=True)
    start_time = IntegerField()
    end_time = IntegerField(null=True)
    
    def __str__(self):
        return "{} {}".format(self.machine, self.recipe)


class Notification(BaseModel):
    id = AutoField(primary_key=True)
    time = IntegerField(default=0)
    text = TextField()

