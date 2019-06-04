import datetime

from peewee import *


db = SqliteDatabase(None)


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
    duration = IntegerField(null=True)

    def __str__(self):
        return self.name


class RecipeInput(BaseModel):
    recipe = ForeignKeyField(Recipe, on_delete='CASCADE')
    item = ForeignKeyField(Item, on_delete='RESTRICT')
    quantity = IntegerField()
    
    class Meta:
        primary_key = CompositeKey('recipe', 'item')
    
    def __str__(self):
        return "{}: {} {}".format(self.recipe, self.quantity, self.item)


class RecipeOutput(BaseModel):
    recipe = ForeignKeyField(Recipe, on_delete='CASCADE')
    item = ForeignKeyField(Item, on_delete='RESTRICT')
    quantity = IntegerField()
    
    class Meta:
        primary_key = CompositeKey('recipe', 'item')
    
    def __str__(self):
        return "{}: {} {}".format(self.recipe, self.quantity, self.item)


class Stock(BaseModel):
    id = AutoField(primary_key=True)
    item = ForeignKeyField(Item, on_delete='CASCADE')
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
    cycles_remaining = IntegerField()
    description = CharField(null=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cycles_remaining = self.cycles
    
    def activate(self):
        self.time_remaining = self.recipe.duration * self.cycles_remaining
        self.usable_machines = []
        self.allocated = 0
    
    def __str__(self):
        return "{:<24}   x{:<3} | ETA R: {:<5} | Machines: ({}) of {}".format(
            str(self.recipe),
            self.cycles_remaining,
            self.time_remaining,
            self.allocated,
            self.usable_machines,
        )
        return "{} x{}".format(self.recipe, self.cycles)


class MachineTask(BaseModel):
    id = AutoField(primary_key=True)
    machine = ForeignKeyField(Machine, on_delete='CASCADE')
    task = ForeignKeyField(Task, on_delete='CASCADE', null=True)
    start_time = IntegerField(null=True)
    cycles = IntegerField(null=True)
    
    def free(self):
        self.temp_task_id = None
        self.start_time = None
        self.cycles = None
    
    def __str__(self):
        return "{}: {} | Start: {} | Cycles: {}".format(
            self.machine_id,
            self.temp_task_id,
            self.start_time,
            self.cycles,
        )


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


def get_tables():
    return [
        Item, Recipe, RecipeInput, RecipeOutput, Stock, 
        Machine, MachineRecipe,
        MachineTask, Task, Notification,
    ]
