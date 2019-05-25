import platform
import os

import peewee

from models import (
    management,
    auth,
)
from .dataset import get_dataset


def clear_console():
    if (platform.system() == "Windows"):
        os.system("cls")
    if (platform.system() == "Linux"):
        os.system("clear")

def input_int():
    try:
        user_input = int(input())
    except ValueError:
        return
    return user_input


class DatabaseTool:
    table_list = [
        management.Item, management.Recipe, management.RecipeInput, management.RecipeOutput, management.Stock, 
        management.Machine, management.MachineRecipe, management.Task, management.Notification
    ]
    
    def menu(self):
        while(True):
            clear_console()
            print("1. Truncate DB")
            print("2. Populate Management")
            print("3. Populate Auth")
            print()
            print("0. Exit")
            print()
            print("What do you want to do?")
            user_input = input_int()
            if user_input == 1: self.truncate_db()
            if user_input == 2: self.populate_management()
            if user_input == 3: self.populate_user()
    
    def __init__(self):
        auth.db.init('databases/auth.sqlite3')
        auth.db.connect()
        auth.db.create_tables([auth.User])
        management.db.init('databases/test.sqlite3')
        management.db.connect()
        management.db.create_tables(self.table_list)

    def truncate_db(self):
        print("Truncate DB")
        for model in self.table_list:
            model.delete().execute()
            print("Truncate {}".format(model.__name__))
        print("Truncate DB done")

    def populate_user(self):
        auth.User.create(
            username = "admin",
            password = "admin",
        )
    
    def populate_management(self):
        dataset = get_dataset('DeepTown')
        with management.db.atomic():
            dataset.populate_db()
            dataset.populate_stocks()

    def print_data(self, index):
        selected_table = self.table_list[index]
        self.data_model = QtGui.QStandardItemModel(self.data_table)
        for i, column in enumerate(list(selected_table._meta.fields.keys())):
            self.data_model.setHorizontalHeaderItem(i, QtGui.QStandardItem(column));
        for item in selected_table.select().tuples():
            self.data_model.appendRow([QtGui.QStandardItem(str(data)) for data in item])
        self.data_table.setModel(self.data_model)

