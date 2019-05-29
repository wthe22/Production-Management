import datetime
from io import StringIO
import sys
import json

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..lib.functions import display_time
from ..lib.task import TaskManager
from ..models.management import (
    Item, Recipe, RecipeOutput,
    Machine, MachineRecipe,
)
from .base import BaseView


class AnalyzerView(BaseView):
    @view_config(route_name='analyzer_input', renderer='../templates/analyze/input.mako')
    def input(self):
        message = None
        
        if 'submit' in self.request.params:
            order_dict = json.loads(self.request.params.get('orders'))
            machine_dict = json.loads(self.request.params.get('machines'))
            
            input_orders = []
            for order in order_dict.values():
                input_orders += [[int(value) for value in order.values()]]
            
            input_machines = []
            for machine in machine_dict.values():
                input_machines += [[int(value) for value in machine.values()]]
            
            taskman = TaskManager()
            exit_code = taskman.set_tasks(input_orders, input_machines, description="Test")
            if exit_code == TaskManager.SUCCESS:
                self.request.session['analyzer_input_data'] = [input_orders, input_machines]
                url = self.request.route_url('analyzer_result')
                return HTTPFound(url)
            else:
                message = "Set orders failed"
        
        item_machine_list = []
        for item in Item.select():
            try:
                recipe = RecipeOutput.get(RecipeOutput.item_id == item.id).recipe
            except RecipeOutput.DoesNotExist:
                continue
            
            try:
                machine = MachineRecipe.get(MachineRecipe.recipe_id == recipe.id).machine
            except MachineRecipe.DoesNotExist:
                message = "warning: recipe '' cannot be produced with any machines".format(recipe.name)
                continue
            
            item_machine_list += [[item.id, machine.id]]
        
        return {
            'item_list': list(Item.select().order_by(Item.name)),
            'machine_list': list(Machine.select().order_by(Machine.name)),
            'item_machine_list': item_machine_list,
            'message': message,
        }
    
    @view_config(route_name='analyzer_result', renderer='../templates/analyze/result.mako')
    def result(self):
        if not 'analyzer_input_data' in self.request.session:
            url = self.request.route_url('analyzer_input')
            return HTTPFound(url)
        
        input_orders, input_machines = self.request.session['analyzer_input_data']
        taskman = TaskManager()
        exit_code = taskman.set_tasks(input_orders, input_machines, description="Test")
        
        if 'submit' in self.request.params:
            taskman.apply_orders()
        
        task_list = taskman.task_list
        machine_list = taskman.active_machines
        
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        print("Analyze result:")
        print()
        time_required, machine_notifications = taskman.calculate_sequence()
        print()
        
        print("Time required: {}".format(str(datetime.timedelta(seconds=time_required))))
        
        sys.stdout = old_stdout
        
        return {
            'time_required': display_time(time_required),
            'test_output': mystdout.getvalue(),
            'task_list': task_list,
            'machine_list': machine_list,
            'machine_notifications': machine_notifications,
        }
    
    @view_config(route_name='analyzer_test', renderer='../templates/analyze/result.mako')
    def run_test(self):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        readable_input_orders = [
            ['Copper Nail', 300 / 20 * 10],
            ['Copper Wire', 300 / 30 * 5],
            ['Battery', 189],
            ['Lamp', 60],
            ['Circuit', 123],

            ['Gunpowder', 151],
            ['Hydrogen', 10],
            ['Clean Water', 7],
        ]
        readable_input_machines = [
            ['Crafting', 4],
            ['Chemistry', 2],
        ]

        input_orders = []
        for name, qty in readable_input_orders:
            item = Item.get(Item.name == name)
            input_orders += [[item.id, qty]]

        input_machines = []
        for name, qty in readable_input_machines:
            machine = Machine.get(Machine.name == name)
            input_machines += [[machine.id, qty]]

        self.request.session['analyzer_input_data'] = [input_orders, input_machines]
        url = self.request.route_url('analyzer_result')
        return HTTPFound(url)
