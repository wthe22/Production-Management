import math
import datetime
import time
import copy

from ..models.management import (
    Item, Recipe, RecipeOutput,
    Machine, MachineRecipe,
    Task, MachineTask,
    Notification,
)


class TaskManager:
    SUCCESS = 0x0
    FAILED = 0x1

    def print_tasks(self, text="Task list"):
        print(text)
        for t, task in self.task_list.items():
            print("{} | {}".format(t, task))
        print()

    def print_machines(self, text="Machine list"):
        print(text)
        for m, machine in self.active_machines.items():
            eta = None
            if not machine.temp_task_id is None:
                task = self.task_list[machine.temp_task_id]
                eta = machine.cycles * task.recipe.duration - (self.elapsed_time - machine.start_time)
            print("{} | {} | ETA: {}".format(m, machine, eta))
        print()

    def __init__(self):
        self.active_machines = {}
        self.task_list = {}
        self.master_task_list = {}
        self.machine_sequences = {}
        self.elapsed_time = 0

    def update_db_tasks(self):
        self.__init__()
        
        for task in Task.select():
            task.activate()
            task.usable_machines = []
            for machine_recipe in MachineRecipe.select().where(MachineRecipe.recipe_id == task.recipe_id):
                machine = machine_recipe.machine
                task.usable_machines += [machine.id]
            self.task_list[task.id] = task
        
        min_time = None
        for machine_task in MachineTask.select():
            self.active_machines[machine_task.id] = machine_task
            
            task_id = machine_task.task_id
            self.task_list[task_id].allocated += 1
            
            if machine_task.start_time is None:
                continue
            
            if min_time is None:
                min_time = machine_task.start_time
            if machine_task.start_time < min_time:
                min_time = machine_task.start_time
        
        # EDIT
            self.task_list[task_id].cycles_remaining -= (self.elapsed_time - machine.start_time) // self.task_list[temp_task_id].recipe.duration
            #task.cycles_remaining = self.cycles
            #task.time_remaining = self.recipe.duration * self.cycles
            #task.allocated = 0
        
            for machine_recipe in MachineRecipe.select().where(MachineRecipe.recipe_id == task.recipe_id):
                machine = machine_recipe.machine
                task.usable_machines += [machine.id]
            self.task_list[task.id] = task
            
            #task.cycles_remaining = self.cycles
            #task.time_remaining = self.recipe.duration * self.cycles
            #task.allocated = 0
        
        self.elapsed_time = min_time    
        target_time = int(time.time())
        
        while(self.elapsed_time < target_time):
            self.assign_tasks()
            self.update_machine_cycles()
            fast_forward_sec = self.lowest_machine_eta()
            catchup_time = target_time - self.elapsed_time
            if fast_forward_sec > catchup_time:
                fast_forward_sec = catchup_time
            
            self.fast_forward(fast_forward_sec)
            
            self.free_machines()

        return self.SUCCESS

    def set_tasks(self, input_orders, input_machines, description):
        input_machines_id = [id for id, qty in input_machines]

        self.task_list = {}
        for item, qty in input_orders:
            item = Item.get(Item.id == item)
            recipe_output = list(RecipeOutput.select().where(RecipeOutput.item_id == item.id))
            if (len(recipe_output) == 0):
                print("error: No recipe can produce item '{}'".format(item.name))
                return None, None
            recipe_output = recipe_output[0]
            recipe = recipe_output.recipe
            cycles = math.ceil(qty / recipe_output.quantity)

            usable_machines = []
            for machine_recipe in MachineRecipe.select().where(MachineRecipe.recipe_id == recipe.id):
                machine = machine_recipe.machine
                usable_machines += [machine.id]
                if not machine.id in input_machines_id:
                    print("error: Machine '{}' is required to produce item '{}'".format(machine.name, item.name))
                    return self.FAILED
            
            id = len(self.task_list)
            task = Task(
                recipe = recipe,
                cycles = cycles,
                description = description,
                usable_machines = usable_machines,
            )
            task.activate()
            task.usable_machines = usable_machines
            self.task_list[id] = task
        
        self.master_task_list = self.task_list.copy()
        
        self.active_machines = {}
        for machine, qty in input_machines:
            machine = Machine.get(Machine.id == machine)
            for i in range(qty):
                id = len(self.active_machines)
                machine_task = MachineTask(machine=machine)
                machine_task.free()
                self.active_machines[id] = machine_task
                self.machine_sequences[id] = []
        
        return self.SUCCESS

    def get_next_task(self, machine_type):
        selected_task = None
        for t, task in self.task_list.items():
            if task.time_remaining == 0:
                continue
            if not machine_type in task.usable_machines:
                continue
            if task.time_remaining <= task.recipe.duration * task.allocated:
                continue

            if selected_task is None:
                selected_task = t
                continue
            if task.allocated > self.task_list[selected_task].allocated:
                continue
            if task.allocated < self.task_list[selected_task].allocated:
                selected_task = t
                continue
            if task.time_remaining < self.task_list[selected_task].time_remaining:
                selected_task = t

        return selected_task

    def assign_tasks(self):
        idle_machines = []
        for i, machine in self.active_machines.items():
            if machine.temp_task_id is None:
                idle_machines += [i]

        for m in idle_machines:
            machine_type = self.active_machines[m].machine_id
            selected_task = self.get_next_task(machine_type)
            if selected_task is None:
                continue
            self.active_machines[m].temp_task_id = selected_task
            self.active_machines[m].start_time = self.elapsed_time
            self.task_list[selected_task].allocated += 1
    
    def update_machine_cycles(self):
        active_tasks = []
        for machine in self.active_machines.values():
            if machine.temp_task_id is None:
                continue
            if not machine.temp_task_id in active_tasks:
                active_tasks += [machine.temp_task_id]

        print("Active Task: {}".format(active_tasks))

        for t in active_tasks:
            task = self.task_list[t]
            m_list = []
            for m, machine in self.active_machines.items():
                if machine.temp_task_id == t:
                    m_list += [m]

            cycles_left = task.cycles_remaining
            for m in m_list:
                machine = self.active_machines[m]
                cycles_elapsed = math.ceil((self.elapsed_time - machine.start_time) / task.recipe.duration)
                cycles_left -= cycles_elapsed
            
            cycles_min = cycles_left // len(m_list)
            for m in m_list:
                machine = self.active_machines[m]
                cycles_elapsed = math.ceil((self.elapsed_time - machine.start_time) / task.recipe.duration)
                self.active_machines[m].cycles = cycles_min + cycles_elapsed
            
            remainder = cycles_left % len(m_list)
            
            print("{} | CL: {} | M: {} | R: {}".format(t, cycles_left, cycles_min, remainder))

            m_list = sorted(m_list, key = lambda m: 
                self.active_machines[m].cycles - (self.elapsed_time - self.active_machines[m].start_time) / task.recipe.duration
            )
            for m in m_list[:remainder]:
                self.active_machines[m].cycles += 1

    def lowest_machine_eta(self):
        lowest_eta = None
        for machine in self.active_machines.values():
            if machine.temp_task_id is None:
                continue
                
            task = self.task_list[machine.temp_task_id]
            eta = machine.cycles * task.recipe.duration - (self.elapsed_time - machine.start_time)
            
            if lowest_eta is None:
                lowest_eta = eta
            if eta < lowest_eta:
                lowest_eta = eta
        return lowest_eta
    
    def fast_forward(self, seconds):
        for m, machine in self.active_machines.items():
            if machine.temp_task_id is None:
                continue

            temp_task_id = self.active_machines[m].temp_task_id

            self.task_list[temp_task_id].time_remaining -= seconds

        self.elapsed_time += seconds
    
    def free_machines(self):
        for m, machine in self.active_machines.items():
            if machine.temp_task_id is None:
                continue

            temp_task_id = self.active_machines[m].temp_task_id
            task = self.task_list[machine.temp_task_id]
            eta = machine.cycles - (self.elapsed_time - machine.start_time) / task.recipe.duration

            if eta == 0:
                self.machine_sequences[m] += [copy.deepcopy(machine)]
                # ! Move to fast_forward?
                self.task_list[temp_task_id].allocated -= 1
                self.task_list[temp_task_id].cycles_remaining -= (self.elapsed_time - machine.start_time) // self.task_list[temp_task_id].recipe.duration
                self.active_machines[m].free()
        
        # ! Delete task?
        updated_recipe_task = {}
        for t, task in self.task_list.items():
            if not task.time_remaining == 0:
                updated_recipe_task[t] = task
        self.task_list = updated_recipe_task

    def calculate_sequence(self):
        iteration = 0
        while(self.task_list):
            print()
            print("[T+{:0>8}] Iteration #{}".format(str(datetime.timedelta(seconds=self.elapsed_time)), iteration))
            iteration += 1

            self.print_tasks("Task List")
            self.print_machines("Machine List")
            self.assign_tasks()
            self.update_machine_cycles()
            self.print_machines("Assigned machines")

            lowest_eta = self.lowest_machine_eta()
            print("Lowest ETA: {}".format(lowest_eta))
            
            self.fast_forward(lowest_eta)
            self.free_machines()
        
        print(self.machine_sequences)
        return self.elapsed_time, self.machine_sequences
    
    def sequence2notif(self, machine_sequences):
        notif_sequences = {}
        for m in machine_sequences.keys():
            notif_sequences[m] = []
        
        for m, machine_task_sequence in machine_sequences.items():
            for machine_task in machine_task_sequence:
                temp_task_id = machine_task.temp_task_id
                
                notif_sequences[m] += [Notification(
                    time = machine_task.start_time,
                    description = "Start task{}: {} (x{})".format(
                        temp_task_id,
                        self.master_task_list[temp_task_id].recipe,
                        machine_task.cycles,
                    )
                )]
            
            machine_task = machine_task_sequence[-1]
            task = self.master_task_list[machine_task.temp_task_id]
            end_time = machine_task.start_time + task.recipe.duration * machine_task.cycles
            
            notif_sequences[m] += [Notification(
                time = end_time,
                description = "Stop machine"
            )]
        
        return notif_sequences
    
    def sequence2log(self, machine_sequences):
        all_notifs = []
        for m, machine_task_sequence in machine_sequences.items():
            for machine_task in machine_task_sequence:
                machine = machine_task.machine
                temp_task_id = machine_task.temp_task_id
                task = self.master_task_list[temp_task_id]
                end_time = machine_task.start_time + task.recipe.duration * machine_task.cycles
                
                machine_name = "{} (#{})".format(machine_task.machine, m)
                task_name = "task{}: {} (x{})".format(
                    temp_task_id,
                    self.master_task_list[temp_task_id].recipe,
                    machine_task.cycles,
                )
                all_notifs += [Notification(
                    time = machine_task.start_time,
                    description = "{}: Started with {}".format(machine_name, task_name),
                )]
                all_notifs += [Notification(
                    time = end_time,
                    description = "{}: Done with {}".format(machine_name, task_name),
                )]
        
        all_notifs = sorted(all_notifs, key = lambda notif: notif.time)
        
        return all_notifs
    
    def apply_orders(self):
        for t in self.task_list.keys():
            self.task_list[t].save()
        
        '''
        for m, machine_task in self.active_machines.items():
            task = self.task_list[machine_task.temp_task_id].id
            machine_task.task_id = task.id
            machine_task.start_time = 0
            machine_task.save()
        '''
