from models import (
    Item, Recipe, RecipeInput, RecipeOutput, Stock, 
    Machine, MachineRecipe, Task, 
    Notification
    )


class Dataset:
    table_list = [
        Item, Recipe, RecipeInput, RecipeOutput, Stock, 
        Machine, MachineRecipe, Task, 
        Notification
    ]

    @classmethod
    def truncate_db(cls):
        print("Truncate DB")
        for model in cls.table_list:
            model.delete().execute()
            print("Truncate {}".format(model.__name__))
        print("Truncate DB done")

    @classmethod
    def populate_db(cls):
        print("Populate DB")
        
        with db.atomic():
            Item.insert_many([[name] for name in cls.item_list], fields=[Item.name]).execute()
        
            for duration, out_items, in_items in cls.recipe_list:
                recipe_name = ""
                for qty, name in out_items:
                    recipe_name += "{} {} + ".format(qty, name)
                recipe_name = recipe_name[:-3]
                recipe = Recipe(
                    name = recipe_name,
                    duration = duration,
                )
                recipe.save()
                for model_class, item_list in [[RecipeInput, in_items], [RecipeOutput, out_items]]:
                    for qty, name in item_list:
                        model_class.create(
                            recipe = recipe.id,
                            item = Item.get(Item.name == name).id,
                            quantity = qty,
                        )
        
            Machine.insert_many(cls.machine_list, fields=[Machine.quantity, Machine.name]).execute()
            
            for machine, recipe_list in cls.machine_recipe_list:
                machine = Machine.get(Machine.name == machine)
                for name in recipe_list:
                    MachineRecipe.create(
                        machine = machine.id,
                        recipe = Recipe.get(Recipe.name == name).id,
                    )
        
        print("Populate DB done")
        return True

    @classmethod
    def populate_stocks(cls, randomize=True):
        print("Populate stocks")
        print("Randomize: {}".format(randomize))
        
        Stock.delete().execute()
        
        if randomize:
            with db.atomic():
                for item in Item.select().order_by('?')[:20]:
                    Stock.create(
                        item_id = item,
                        description = "Default",
                        quantity = random.randint(300, 27000),
                    )
                return
        
        with db.atomic():
            for qty, name in cls.stock_list:
                Stock.create(
                    item_id = Item.get(Item.name == name).id,
                    comment = "Default",
                    quantity = qty,
                )
        print("Populate stocks done")


class DeepTown(Dataset):
    item_list = [
        # Mining Station
        "Coal", "Copper", "Iron", "Amber", "Aluminum", "Silver", "Gold", "Emerald", "Platinum",
        "Topaz", "Ruby", "Sapphire", "Amethyst", "Diamond", "Alexandrite", "Obsidian",
        "Titanium Ore", "Uranium",
        
        # Chemistry Mining
        "Silicon", "Sulfur", "Sodium", "Nitrogen",
        
        # Water Collector
        "Water",
        
        # Oil Mining
        "Oil",
        
        # Smelting
        "Copper Bar", "Iron Bar", "Glass", "Aluminum Bar", "Steel Bar", "Silver Bar", "Gold Bar",
        "Steel Plate", "Steel Pipe", "Titanium Bar", "Magnetite Bar",
         
        # Crafting
        "Graphite", "Copper Nail", "Copper Wire", "Battery", "Circuit", "Lamp", "Lab Flask",
        "Amber Charger", "Aluminum Bottle", "Amber Insulation", "Insulated Wire", "Aluminum Tank",
        "Mirror", "Mirror Laser", "Green Laser", "Diamond Cutter", "Motherboard", "Solid Propellant",
        "Accumulator", "Solar Panel", "Gear", "Gas Cylinder", "Bomb", "Compressor", "Optic Fiber",
        "Dry Ice", "Oxygen Cylinder", "Magnet", "Electrical Engine", "LCD Monitor",
        
        # Chemistry
        "Clean Water", "Hydrogen", "Oxygen", "Rubber", "Sulfuric Acid", "Ethanol", "Refined Oil",
        "Plastic Plate", "Titanium", "Diethyl Ether", "Gunpowder", "Liquid Nitrogen", "Magnetite Ore",
        "Enhanced Helium 3", "Toxic Bomb",
        
        # Uranium Enrichment
        "Uranium Rod", 
        
        # Jewel Crafting
        "Polished Amber", "Polished Emerald", "Polished Topaz", "Polished Ruby", "Polished Diamond",
        "Polished Sapphire", "Polished Amethyst", "Polished Alexandrite", "Polished Obsidian",
        "Emerald Ring", "Amber Bracelet", "Maya Calendar", "Haircomb", "Obsidian Knife",
        "Sapphire Crystal Glass",
        
        # Greenhouse
        "Tree Seed", "Liana Seed", "Grape Seed",
        "Tree", "Liana", "Grape",
    ]
    recipe_list = [
        # Smelting
        [10, [[1, "Copper Bar"]], [[5, "Copper"]]],
        [15, [[1, "Iron Bar"]], [[5, "Iron"]]],
        [60, [[1, "Glass"]], [[2, "Silicon"]]],
        [15, [[1, "Aluminum Bar"]], [[5, "Aluminum"]]],
        [45, [[1, "Steel Bar"]], [[1, "Graphite"], [1, "Iron Bar"]]],
        [60, [[1, "Silver Bar"]], [[5, "Silver"]]],
        [60, [[1, "Coal"]], [[1, "Tree"]]],
        [60, [[1, "Gold Bar"]], [[5, "Gold"]]],
        [120, [[1, "Steel Plate"]], [[5, "Steel Bar"]]],
        [60, [[1, "Steel Pipe"]], [[1, "Steel Plate"]]],
        [60, [[1, "Titanium Bar"]], [[5, "Titanium"]]],
        #[60, [[1, "Magnetite Bar"]], [[5, "Unknown"]]],
        
        # Crafting
        [5, [[1, "Graphite"]], [[5, "Coal"]]],
        [20, [[10, "Copper Nail"]], [[1, "Copper Bar"]]],
        [30, [[5, "Copper Wire"]], [[1, "Copper Bar"]]],
        [120, [[1, "Battery"]], [[1, "Amber"], [1, "Iron Bar"], [5, "Copper Bar"]]],
        [180, [[1, "Circuit"]], [[10, "Iron Bar"], [50, "Graphite"], [20, "Copper Bar"]]],
        [140, [[1, "Lamp"]], [[5, "Copper Bar"], [10, "Copper Wire"], [20, "Graphite"]]],
        [60, [[1, "Lab Flask"]], [[1, "Glass"]]],
        [5, [[1, "Amber Charger"]], [[1, "Amber"]]],
        [30, [[1, "Aluminum Bottle"]], [[1, "Aluminum Bar"]]],
        [20, [[1, "Amber Insulation"]], [[10, "Amber"], [1, "Aluminum Bottle"]]],
        [200, [[1, "Insulated Wire"]], [[1, "Copper Wire"], [1, "Amber Insulation"]]],
        [120, [[5, "Aluminum Tank"]], [[3, "Aluminum Bar"]]],
        [120, [[2, "Mirror"]], [[1, "Glass"], [1, "Aluminum Bar"]]],
        [120, [[2, "Mirror Laser"]], [[1, "Battery"], [1, "Lamp"], [3, "Mirror"]]],
        [20, [[5, "Green Laser"]], [[1, "Emerald"], [1, "Insulated Wire"], [1, "Lamp"]]],
        [30, [[1, "Diamond Cutter"]], [[1, "Steel Plate"], [5, "Polished Diamond"]]],
        [30, [[1, "Motherboard"]], [[1, "Gold Bar"], [3, "Circuit"], [3, "Silicon"]]],
        [20, [[1, "Solid Propellant"]], [[1, "Aluminum Bar"], [3, "Rubber"]]],
        [180, [[1, "Accumulator"]], [[20, "Sulfur"], [20, "Sodium"]]],
        [60, [[1, "Solar Panel"]], [[1, "Rubber"], [10, "Silicon"], [50, "Glass"]]],
        [80, [[1, "Gear"]], [[1, "Diamond Cutter"], [1, "Titanium"]]],
        [180, [[3, "Gas Cylinder"]], [[1, "Steel Plate"], [1, "Plastic Plate"], [1, "Aluminum Tank"]]],
        [180, [[1, "Bomb"]], [[5, "Steel Bar"], [10, "Gunpowder"]]],
        [180, [[1, "Compressor"]], [[2, "Refined Oil"], [1, "Rubber"], [5, "Iron Bar"]]],
        [120, [[10, "Optic Fiber"]], [[10, "Silicon"], [10, "Oxygen"], [1, "Plastic Plate"]]],
        [120, [[4, "Dry Ice"]], [[1, "Compressor"], [10, "Green Laser"], [1000, "Graphite"]]],
        [120, [[1, "Oxygen Cylinder"]], [[1, "Compressor"], [1, "Gas Cylinder"], [5, "Oxygen"]]],
        #"Magnet", "Electrical Engine", "LCD Monitor",
        
        # Chemistry
        [10*60, [[1, "Clean Water"]], [[1, "Lab Flask"], [1, "Water"]]],
        [15*60, [[2, "Hydrogen"], [1, "Oxygen"]], [[1, "Water"]]],
        [30*60, [[2, "Rubber"]], [[1, "Liana"]]],
        [30*60, [[1, "Sulfuric Acid"]], [[2, "Sulfur"], [1, "Clean Water"]]],
        [30*60, [[1, "Ethanol"]], [[1, "Aluminum Bottle"], [2, "Grape"]]],
        [30*60, [[1, "Refined Oil"]], [[10, "Oil"], [10, "Hydrogen"], [1, "Lab Flask"]]],
        [10*60, [[1, "Plastic Plate"]], [[1, "Green Laser"], [50, "Coal"], [1, "Refined Oil"]]],
        [20, [[50, "Titanium"]], [[1, "Sulfuric Acid"], [100, "Titanium Ore"]]],
        [60, [[1, "Diethyl Ether"]], [[1, "Sulfuric Acid"], [1, "Ethanol"]]],
        [120, [[20, "Gunpowder"]], [[1, "Diethyl Ether"], [2, "Sulfuric Acid"], [2, "Tree"]]],
        [120, [[4, "Liquid Nitrogen"]], [[1, "Aluminum Bottle"], [10, "Nitrogen"], [1, "Compressor"]]],
        
        # Greenhouse
        [30*60, [[10, "Tree"]], [[1, "Tree Seed"], [10, "Water"]]],
        [30*60, [[1, "Liana"]], [[1, "Liana Seed"], [20, "Water"]]],
        [30*60, [[2, "Grape"]], [[1, "Grape Seed"], [15, "Water"]]],
        
        # Jewel Crafting
        [30, [[1, "Polished Amber"]], [[5, "Amber"]]],
        [30, [[1, "Polished Emerald"]], [[5, "Emerald"]]],
        [60, [[1, "Polished Topaz"]], [[5, "Topaz"]]],
        [60, [[1, "Polished Ruby"]], [[5, "Ruby"]]],
        [60, [[1, "Polished Diamond"]], [[5, "Diamond"]]],
        [60, [[1, "Polished Sapphire"]], [[5, "Sapphire"]]],
        [60, [[1, "Polished Amethyst"]], [[5, "Amethyst"]]],
        [60, [[1, "Polished Alexandrite"]], [[5, "Alexandrite"]]],
        [60, [[1, "Polished Obsidian"]], [[5, "Obsidian"]]],
        [5*60, [[1, "Emerald Ring"]], [[1, "Gold"], [1, "Polished Emerald"]]],
        [2*60, [[1, "Amber Bracelet"]], [[1, "Silver"], [1, "Polished Amber"]]],
        [2*60, [[1, "Maya Calendar"]], [[2, "Silver"], [10, "Gold"]]],
        [2*60, [[1, "Haircomb"]], [[1, "Silver"], [15, "Polished Amethyst"], [10, "Polished Alexandrite"]]],
        [2*60, [[1, "Obsidian Knife"]], [[1, "Silver"], [2, "Tree"], [50, "Obsidian"]]],
        [120, [[1, "Sapphire Crystal Glass"]], [[10, "Sapphire"]]],
        
        # Uranium Enrichment
        [120, [[1, "Uranium Rod"]], [[20, "Uranium"], [10, "Sodium"]]],
    ]
    machine_list = [
        [8, "Smelting"],
        [8, "Crafting"],
        [5, "Chemistry"],
        [3, "Greenhouse"],
        [8, "Jewel Crafting"],
        [2, "Uranium Enrichment"],
    ]
    stock_list = [
        # Mining Station
        [9500, "Coal"], [10800, "Copper"], [30000, "Iron"], [54700, "Amber"], [16400, "Aluminum"],
        [25500, "Silver"], [18300, "Gold"], [65400, "Emerald"], [35200, "Platinum"], [34800, "Topaz"],
        [7500, "Sapphire"], [13100, "Amethyst"], [1500, "Diamond"], [7500, "Alexandrite"],
        [48600, "Obsidian"], [31000, "Titanium Ore"], [110, "Uranium"],
        
        # Chemistry Mining
        [100, "Silicon"], [19000, "Sulfur"], [39400, "Sodium"], [64, "Nitrogen"],
        
        # Water Collector
        [2000, "Water"],
        
        # Oil Mining
        [225, "Oil"], 
    ]
    machine_recipe_list = [
        ["Smelting", [
            "1 Copper Bar",
            "1 Iron Bar",
            "1 Glass",
            "1 Aluminum Bar",
            "1 Steel Bar",
            "1 Silver Bar",
            "1 Coal",
            "1 Gold Bar",
            "1 Steel Plate",
            "1 Steel Pipe",
            "1 Titanium Bar",
        ]],
        ["Crafting", [
            "1 Graphite",
            "10 Copper Nail",
            "5 Copper Wire",
            "1 Battery",
            "1 Circuit",
            "1 Lamp",
            "1 Lab Flask",
            "1 Amber Charger",
            "1 Aluminum Bottle",
            "1 Amber Insulation",
            "1 Insulated Wire",
            "5 Aluminum Tank",
            "2 Mirror",
            "2 Mirror Laser",
            "5 Green Laser",
            "1 Diamond Cutter",
            "1 Motherboard",
            "1 Solid Propellant",
            "1 Accumulator",
            "1 Solar Panel",
            "1 Gear",
            "3 Gas Cylinder",
            "1 Bomb",
            "1 Compressor",
            "10 Optic Fiber",
            "4 Dry Ice",
            "1 Oxygen Cylinder",
        ]],
        ["Chemistry", [
            "1 Clean Water",
            "2 Hydrogen + 1 Oxygen",
            "2 Rubber",
            "1 Sulfuric Acid",
            "1 Ethanol",
            "1 Refined Oil",
            "1 Plastic Plate",
            "50 Titanium",
            "1 Diethyl Ether",
            "20 Gunpowder",
            "4 Liquid Nitrogen",
        ]],
        ["Greenhouse", [
            "10 Tree",
            "1 Liana",
            "2 Grape",
        ]],
        ["Jewel Crafting", [
            "1 Polished Amber",
            "1 Polished Emerald",
            "1 Polished Topaz",
            "1 Polished Ruby",
            "1 Polished Diamond",
            "1 Polished Sapphire",
            "1 Polished Amethyst",
            "1 Polished Alexandrite",
            "1 Polished Obsidian",
            "1 Emerald Ring",
            "1 Amber Bracelet",
            "1 Maya Calendar",
            "1 Haircomb",
            "1 Obsidian Knife",
            "1 Sapphire Crystal Glass",
        ]],
        ["Uranium Enrichment", [
            "1 Uranium Rod",
        ]],
    ]
    
    @classmethod
    def add_collector(cls):
        # Collector Buildings
        for item_name in [
            "Coal", "Copper", "Iron", "Amber", "Aluminum", "Silver", "Gold", "Emerald", "Platinum",
            "Topaz", "Ruby", "Sapphire", "Amethyst", "Diamond", "Alexandrite", "Obsidian",
            "Titanium Ore", "Uranium",
        ]:
            recipe = Recipe(
                name = "{} Mining Station - Level 9".format(item_name),
                description = "Highest level Mining Station. Consumes 2 electricity",
                duration = timedelta(seconds=3),
            )
            recipe.save()
            RecipeOutput.objects.create(
                recipe_id = recipe,
                item_id = Item.objects.get(name=item_name),
                quantity = 1,
            )
        
        for qty, name in [
            [20, "Silicon"], 
            [20, "Sulfur"],
            [20, "Sodium"],
            [12, "Nitrogen"],
        ]:
            recipe = Recipe(
                name = "{} Chemistry Mining - Level 4".format(name),
                description = "Highest level Chemistry Mining",
                duration = timedelta(minutes=10),
            )
            recipe.save()
            RecipeOutput.objects.create(
                recipe_id = recipe,
                item_id = Item.objects.get(name=name),
                quantity = qty,
            )
        [
            ["Water Collector", "Water"],
            ["Oil Mining", "Oil"],
        ]

class HayDay(Dataset):
    item_list = [
        "Wheat", "Carrot", "Sugarcane", "Soybean", "Corn",
        "Chili Pepper", "Cotton", "Indigo", "Pumpkin",
        "Chicken Feed", "Cow Feed", "Pig Feed", "Sheep Feed",
        "Brown Sugar", "White Sugar", "Syrup",
        "Egg", "Milk", "Bacon", "Wool",
        "Bread", "Corn Bread", "Cookie",
        "Popcorn", "Buttered Popcorn", "Chili Popcorn",
        "Cream", "Butter", "Cheese",
    ]
    recipe_list = [
        [4*60, [[3, "Chicken Feed"]], [[2, "Wheat"], [1, "Corn"]]],
        [9*60, [[3, "Cow Feed"]], [[2, "Soybean"], [1, "Corn"]]],
        [19*60, [[3, "Pig Feed"]], [[2, "Carrot"], [1, "Soybean"]]],
        [28*60, [[3, "Sheep Feed"]], [[3, "Wheat"], [1, "Soybean"]]],
        [20*60, [[1, "Brown Sugar"]], [[1, "Sugarcane"]]],
        [40*60, [[1, "White Sugar"]], [[2, "Sugarcane"]]],
        [90*60, [[1, "Syrup"]], [[3, "Sugarcane"]]],
        [20*60, [[1, "Egg"]], [[1, "Chicken Feed"]]],
        [60*60, [[1, "Milk"]], [[1, "Cow Feed"]]],
        [4*60*60, [[1, "Bacon"]], [[1, "Pig Feed"]]],
        [6*60*60, [[1, "Wool"]], [[1, "Sheep Feed"]]],
        [5*60, [[1, "Bread"]], [[3, "Wheat"]]],
        [30*60, [[1, "Corn Bread"]], [[2, "Corn"], [2, "Egg"]]],
        [60*60, [[1, "Cookie"]], [[2, "Wheat"], [1, "Brown Sugar"], [2, "Egg"]]],
        [30*60, [[1, "Popcorn"]], [[2, "Corn"]]],
        [60*60, [[1, "Buttered Popcorn"]], [[2, "Corn"], [1, "Butter"]]],
        [2*60*60, [[1, "Chili Popcorn"]], [[1, "Corn"], [2, "Chili Pepper"]]],
        [20*60, [[1, "Cream"]], [[1, "Milk"]]],
        [30*60, [[1, "Butter"]], [[2, "Milk"]]],
        [60*60, [[1, "Cheese"]], [[3, "Milk"]]],
    ]
    machine_list = []
    stock_list = []


def get_sample(name):
    for dataset in [DeepTown, HayDay]:
        if dataset.__name__.lower() == name.lower():
            return dataset
    return None


if __name__ == '__main__':
    import sys
    import random
    from PyQt5 import QtCore, QtGui, QtWidgets, uic
    import peewee
    from models import db


    class TableExplorer(QtWidgets.QWidget):
        def __init__(self):
            super(TableExplorer, self).__init__()
            uic.loadUi('TableExplorer.ui', self)

            self.dataset = DeepTown

            db.init('test.sqlite3')
            #db.init(':memory:')
            db.connect()
            db.create_tables(Dataset.table_list)
            self.table_selector.addItems([table.__name__ for table in Dataset.table_list])
            self.table_selector.currentIndexChanged.connect(self.update_data)

            self.data_model = QtGui.QStandardItemModel(self.data_table)
            self.update_data(0)
            self.truncate_button.clicked.connect(self.dataset.truncate_db)
            self.populate_button.clicked.connect(self.dataset.populate_db)
            self.random_stock_button.clicked.connect(self.dataset.populate_stocks)

        def update_data(self, index):
            selected_table = Dataset.table_list[index]
            self.data_model = QtGui.QStandardItemModel(self.data_table)
            for i, column in enumerate(list(selected_table._meta.fields.keys())):
                self.data_model.setHorizontalHeaderItem(i, QtGui.QStandardItem(column));
            for item in selected_table.select().tuples():
                self.data_model.appendRow([QtGui.QStandardItem(str(data)) for data in item])
            self.data_table.setModel(self.data_model)

    app = QtWidgets.QApplication(sys.argv)
    table_explorer = TableExplorer()
    table_explorer.show()
    sys.exit(app.exec_())

