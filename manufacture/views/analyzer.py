import math
import datetime
from io import StringIO
import sys
import json

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..models.management import (
    Item, Recipe, RecipeInput, RecipeOutput, Stock, 
    Machine, MachineRecipe, Task, Notification
)
from .base import BaseView


class ActiveTask:
    def __init__(self, recipe, cycles_remaining, time_remaining, usable_machines, allocated):
        self.recipe = recipe
        self.cycles_remaining = cycles_remaining
        self.time_remaining = time_remaining
        self.usable_machines = usable_machines
        self.allocated = allocated

    def __str__(self):
        return "{:<24}   x{:<3} | ETA R: {:<5} | Machines: ({}) of {}".format(
            str(self.recipe),
            self.cycles_remaining,
            self.time_remaining,
            self.allocated,
            self.usable_machines,
        )


class ActiveMachine:
    def __init__(self, machine_id, task_id, start_time, eta):
        self.machine_id = machine_id
        self.task_id = task_id
        self.start_time = start_time
        self.eta = eta

    def __str__(self):
        return "{}: {} | Start: {} | ETA: {}".format(
            self.machine_id,
            self.task_id,
            self.start_time,
            self.eta,
        )


class TaskManager:
    SUCCESS = 0x0
    FAILED = 0x1

    def print_tasks(self, text="Task list"):
        print(text)
        for t, task in self.recipe_tasks.items():
            print("{} | {}".format(t, task))
        print()

    def print_machines(self, text="Machine list"):
        print(text)
        for m, machine in self.active_machines.items():
            print("{} | {}".format(m, machine))
        print()

    def __init__(self):
        self.active_machines = {}
        self.recipe_tasks = {}
        self.all_notifications = []
        self.machine_notifications = {}
        self.elapsed_time = 0

    def set_orders(self, input_orders, input_machines):
        input_machines_id = [id for id, qty in input_machines]

        self.recipe_tasks = {}
        for item, qty in input_orders:
            item = Item.get(Item.id == item)
            recipe_output = list(RecipeOutput.select().where(RecipeOutput.item_id == item.id))
            if (len(recipe_output) == 0):
                print("error: No recipe can produce item '{}'".format(item.name))
                return None, None
            recipe_output = recipe_output[0]
            recipe = recipe_output.recipe
            cycles_remaining = math.ceil(qty / recipe_output.quantity)
            time_remaining = recipe.duration * cycles_remaining

            usable_machines = []
            for machine_recipe in MachineRecipe.select().where(MachineRecipe.recipe_id == recipe.id):
                machine = machine_recipe.machine
                usable_machines += [machine.id]
                if not machine.id in input_machines_id:
                    print("error: Machine '{}' is required to produce item '{}'".format(machine.name, item.name))
                    return self.FAILED

            self.recipe_tasks[len(self.recipe_tasks)] = ActiveTask(
                recipe = recipe,
                cycles_remaining = cycles_remaining,
                time_remaining = time_remaining,
                usable_machines = usable_machines,
                allocated = 0,
            )

        self.active_machines = {}
        for machine, qty in input_machines:
            machine = Machine.get(Machine.id == machine)
            for i in range(qty):
                id = len(self.active_machines)
                self.active_machines[id] = ActiveMachine(
                    machine_id = machine.id,
                    task_id = None,
                    start_time = None,
                    eta = None,
                )
                self.machine_notifications[id] = []

        return self.SUCCESS

    def next_task(self, machine_type):
        selected_task = None
        for t, task in self.recipe_tasks.items():
            if task.time_remaining == 0:
                continue
            if not machine_type in task.usable_machines:
                continue
            if task.time_remaining <= task.recipe.duration * task.allocated:
                continue

            if selected_task is None:
                selected_task = t
                continue
            if task.allocated > self.recipe_tasks[selected_task].allocated:
                continue
            if task.allocated < self.recipe_tasks[selected_task].allocated:
                selected_task = t
                continue
            if task.time_remaining < self.recipe_tasks[selected_task].time_remaining:
                selected_task = t

        return selected_task

    def assign_task(self):
        idle_machines = []
        for i, machine in self.active_machines.items():
            if machine.task_id is None:
                idle_machines += [i]

        for m in idle_machines:
            machine_type = self.active_machines[m].machine_id
            selected_task = self.next_task(machine_type)
            if selected_task is None:
                continue
            self.active_machines[m].task_id = selected_task
            self.active_machines[m].start_time = self.elapsed_time
            self.recipe_tasks[selected_task].allocated += 1
            
            self.all_notifications += [Notification(
                time = self.elapsed_time,
                description = "Started machine{} with task{}: {}".format(m, selected_task, self.recipe_tasks[selected_task].recipe)
            )]
            self.machine_notifications[m] += [Notification(
                time = self.elapsed_time,
                description = "Started  task{}: {}".format(selected_task, self.recipe_tasks[selected_task].recipe)
            )]

    def lowest_machine_eta(self):
        lowest_eta = None
        for machine in self.active_machines.values():
            if machine.task_id is None:
                continue
            if lowest_eta is None:
                lowest_eta = machine.eta
            if machine.eta < lowest_eta:
                lowest_eta = machine.eta
        return lowest_eta

    def fast_forward(self, seconds):
        for m, machine in self.active_machines.items():
            if machine.task_id is None:
                continue

            task_id = self.active_machines[m].task_id

            self.active_machines[m].eta -= seconds
            self.recipe_tasks[task_id].time_remaining -= seconds

        self.elapsed_time += seconds

    def free_machines(self):
        for m, machine in self.active_machines.items():
            if machine.task_id is None:
                continue

            task_id = self.active_machines[m].task_id

            if machine.eta == 0:
                self.all_notifications += [Notification(
                    time = self.elapsed_time,
                    description = "machine{} done with task{}: {}".format(m, task_id, self.recipe_tasks[task_id].recipe)
                )]
                self.machine_notifications[m] += [Notification(
                    time = self.elapsed_time,
                    description = "Done with task{}: {}".format(task_id, self.recipe_tasks[task_id].recipe)
                )]
                self.active_machines[m].task_id = None
                self.recipe_tasks[task_id].allocated -= 1
                self.recipe_tasks[task_id].cycles_remaining -= (self.elapsed_time - machine.start_time) // self.recipe_tasks[task_id].recipe.duration
            if self.recipe_tasks[task_id].time_remaining == 0:
                del self.recipe_tasks[task_id]

    def calculate_eta(self):
        active_tasks = []
        for machine in self.active_machines.values():
            if machine.task_id is None:
                continue
            if not machine.task_id in active_tasks:
                active_tasks += [machine.task_id]

        print("Active Task: {}".format(active_tasks))

        for t in active_tasks:
            task = self.recipe_tasks[t]
            m_list = []
            for m, machine in self.active_machines.items():
                if machine.task_id == t:
                    m_list += [m]

            cycles_left = task.cycles_remaining
            for m in m_list:
                machine = self.active_machines[m]
                cycles_left -= math.ceil((self.elapsed_time - machine.start_time) / task.recipe.duration)
            eta_min = task.recipe.duration * (cycles_left // len(m_list))
            for m in m_list:
                machine = self.active_machines[m]
                cycle_remaining = task.recipe.duration - (self.elapsed_time - machine.start_time) % task.recipe.duration
                if cycle_remaining == task.recipe.duration:
                    cycle_remaining = 0
                self.active_machines[m].eta = eta_min + cycle_remaining
            remainder = cycles_left % len(m_list)
            #print("ETA: M: {} + R: {}".format(eta_min, cycle_remaining))
            print("{} | CL: {} | M: {} | R: {}".format(t, cycles_left, eta_min, remainder))

            m_list = sorted(m_list, key = lambda m: self.active_machines[m].eta)
            for m in m_list[:remainder]:
                self.active_machines[m].eta += task.recipe.duration

    def calculate_sequence(self):
        iteration = 0
        while(self.recipe_tasks):
            print()
            print("[T+{:0>8}] Iteration #{}".format(str(datetime.timedelta(seconds=self.elapsed_time)), iteration))
            iteration += 1

            self.print_tasks("Task List")
            self.print_machines("Machine List")
            self.assign_task()
            self.calculate_eta()
            self.print_machines("Assigned machines")

            lowest_eta = self.lowest_machine_eta()
            print("Lowest ETA: {}".format(lowest_eta))
            if lowest_eta is None:
                break

            self.fast_forward(lowest_eta)
            self.free_machines()

        return self.elapsed_time, self.machine_notifications


class AnalyzerView(BaseView):
    @view_config(route_name='analyzer_input', renderer='../templates/analyze/input.mako')
    def show(self):
    
        item_machines = {}
        for item in Item.select():
            recipe = [recipe_item.recipe for recipe_item in RecipeOutput.select().where(RecipeOutput.item_id == item.id)]
        
        return {
            'item_list': Item.select().order_by(Item.name),
            'item_machines': item_machines,
            'recipe_list': Recipe.select().order_by(Recipe.name),
            'machine_list': Machine.select().order_by(Machine.name)
        }
    
    @view_config(route_name='analyzer_result', renderer='../templates/analyze/result.mako')
    def result(self):
        if not 'submit' in self.request.params:
            url = self.request.route_url('analyzer_input')
            return HTTPFound(url)
        
        order_dict = json.loads(self.request.params.get('orders'))
        machine_dict = json.loads(self.request.params.get('machines'))
        
        input_orders = []
        for order in order_dict.values():
            input_orders += [[int(value) for value in order.values()]]
        
        input_machines = []
        for machine in machine_dict.values():
            input_machines += [[int(value) for value in machine.values()]]
        
        print("Input orders:")
        print(input_orders)
        print()
        
        print("Input machines:")
        print(input_machines)
        print()
        
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        taskman = TaskManager()
        exit_code = taskman.set_orders(input_orders, input_machines)
        if exit_code == TaskManager.FAILED:
            print("Set orders failed")
            return

        print("Analyze result:")
        time_required, machine_notifications = taskman.calculate_sequence()
        print()
        print("Time required: {}".format(str(datetime.timedelta(seconds=time_required))))
        
        sys.stdout = old_stdout
        
        return {
            'time_required': time_required,
            'test_output': mystdout.getvalue(),
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

        taskman = TaskManager()
        exit_code = taskman.set_orders(input_orders, input_machines)
        if exit_code == TaskManager.FAILED:
            print("Set orders failed")
            return

        print("Analyze result:")
        time_required, machine_notifications = taskman.calculate_sequence()
        print()
        print("Time required: {}".format(str(datetime.timedelta(seconds=time_required))))

        return {
            'time_required': time_required,
            'test_output': mystdout.getvalue(),
            'machine_notifications': machine_notifications,
        }

