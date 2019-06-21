import json

from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    exception_response
)

from ..lib.forms import PostForm
from ..lib.functions import display_time
from ..lib.task import TaskManager
from ..models.management import (
    Item, Recipe, RecipeInput, RecipeOutput, Stock, 
    Machine, MachineRecipe,
    MachineTask, Task, Notification
)
from .base import BaseView


class ModelView(BaseView):
    model = None
    
    def form_component(self, name):
        components = {
            'name': {
                'label': "Name",
                'type': "text",
                'required': True,
            },
            'description': {
                'label': "Description",
                'type': "text",
            },
            'duration': {
                'label': "Duration",
                'type': "number",
                'required': True,
            },
            'quantity': {
                'label': "Quantity",
                'type': "number",
                'required': True,
            },
            'details': {
                'label': "Details",
                'type': "textarea",
                'required': True,
            },
            'item_id': {
                'label': "Item",
                'type': "select",
                'required': True,
                'options': [[item.id, item.name] for item in Item.select().order_by(Item.name)],
            },
            'recipe_id': {
                'label': "Recipe",
                'type': "select",
                'required': True,
                'options': [[recipe.id, recipe.name] for recipe in Recipe.select().order_by(Recipe.name)],
            },
            'machine_id': {
                'label': "Machine",
                'type': "select",
                'required': True,
                'options': [[machine.id, machine.name] for machine in Machine.select().order_by(Machine.name)],
            },
            'start_time': {
                'label': "Start Time",
                'type': "datetime",
                'required': True,
            },
            'cycles': {
                'label': "Cycles",
                'type': "number",
                'required': True,
            },
        }
        return {**components[name], 'name': name}
    
    def get_or_404(self):
        id = self.request.matchdict['id']
        try:
            return self.model.get_by_id(id)
        except self.model.DoesNotExist:
            raise exception_response(404)

    def add_new(self, success_route, fields):
        edit_form = PostForm(
            name = 'edit',
            components = [self.form_component(field) for field in fields],
        )
        
        if 'submit' in self.request.params:
            form_values = edit_form.extract_values(self.request.params)
            self.model.create(**form_values)
            url = self.request.route_url(success_route)
            return HTTPFound(url)

        return {
            'heading': "Add new {}".format(self.model.__name__),
            'edit_form_schema': edit_form.schema(),
        }

    def edit(self, success_route, fields):
        selected = self.get_or_404()
        
        edit_form = PostForm(
            name = 'edit',
            components = [{**self.form_component(field), 'value': getattr(selected, field)} for field in fields],
        )
        
        if 'submit' in self.request.params:
            form_values = edit_form.extract_values(self.request.params)
            for key, value in form_values.items():
                setattr(selected, key, value)
            selected.save()
            url = self.request.route_url(success_route)
            return HTTPFound(url)

        return {
            'heading': "Edit {}".format(self.model.__name__),
            'edit_form_schema': edit_form.schema(),
        }

    def delete(self, success_route=None):
        selected = self.get_or_404()
        selected.delete_instance()
        url = self.request.route_url(success_route)
        return HTTPFound(url)


class ItemView(ModelView):
    model = Item
    
    @view_config(route_name='item_list', renderer='../templates/management/item_list.mako')
    def list(self):
        recipe_list = Recipe.select().order_by(Recipe.name)
        recipe_count = len(recipe_list)
        recipe_full_list = []
        for recipe in recipe_list:
            recipe_full_list += [[
                recipe,
                [
                    list(RecipeInput.select().where(RecipeInput.recipe == recipe.id)),
                    list(RecipeOutput.select().where(RecipeOutput.recipe == recipe.id)),
                ],
            ]]
        item_list = Item.select().order_by(Item.name)
        item_count = len(item_list)
        return {
            'item_list': item_list,
            'item_count': item_count,
            'recipe_count': recipe_count,
            'recipe_full_list': recipe_full_list,
        }

    @view_config(route_name='item_show', renderer='../templates/management/item_show.mako')
    def show(self):
        item = self.get_or_404()
        
        return {
            'item': item,
            'recipe_input': RecipeInput.select().where(RecipeInput.item_id == item.id).order_by(RecipeInput.item.name),
            'recipe_output': RecipeOutput.select().where(RecipeOutput.item_id == item.id).order_by(RecipeOutput.item.name),
        }

    @view_config(route_name='item_new', renderer='../templates/management/generic_edit.mako')
    def add_new(self):
        return super().add_new(
            success_route = 'item_list',
            fields = ['name', 'details']
        )

    @view_config(route_name='item_edit', renderer='../templates/management/generic_edit.mako')
    def edit(self):
        return super().edit(
            success_route = 'item_list',
            fields = ['name', 'details']
        )

    @view_config(route_name='item_delete', renderer='../templates/show_item.mako')
    def delete(self):
        return super().delete(success_route='item_list')


class RecipeView(ModelView):
    model = Recipe
    
    @view_config(route_name='recipe_show', renderer='../templates/management/recipe_show.mako')
    def show(self):
        recipe = self.get_or_404()
        recipe.duration = display_time(recipe.duration)
        return {
            'recipe': recipe,
            'recipe_input': RecipeInput.select().where(RecipeInput.recipe_id == recipe.id).order_by(RecipeInput.item.name),
            'recipe_output': RecipeOutput.select().where(RecipeOutput.recipe_id == recipe.id).order_by(RecipeOutput.item.name),
            'machine_list': [machine_recipe.machine for machine_recipe in MachineRecipe.select().where(MachineRecipe.recipe_id == recipe.id).order_by(MachineRecipe.machine.name)],
        }

    @view_config(route_name='recipe_new', renderer='../templates/management/recipe_edit.mako')
    def add_new(self):
        return {
            **super().add_new(
                success_route = 'item_list',
                fields = ['name', 'details', 'duration']
            ),
            'item_options': json.dumps([[item.id, item.name] for item in Item.select().order_by(Item.name)], ensure_ascii=False),
            'recipe_input': [],
            'recipe_output': [],
        }
            

    @view_config(route_name='recipe_edit', renderer='../templates/management/recipe_edit.mako')
    def edit(self):
        success_route = 'item_list'
        fields = ['name', 'details', 'duration']
        
        recipe = self.get_or_404()
        
        edit_form = PostForm(
            name = 'edit',
            components = [{**self.form_component(field), 'value': getattr(recipe, field)} for field in fields],
        )
        
        if 'submit' in self.request.params:
            form_values = edit_form.extract_values(self.request.params)
            for key, value in form_values.items():
                setattr(recipe, key, value)
            recipe.save()

            recipe_input_list = json.loads(self.request.params.get('recipe_inputs')).values()
            recipe_output_list = json.loads(self.request.params.get('recipe_outputs')).values()
            
            recipe_inputs = []
            for item in recipe_input_list:
                item_id, qty = item.values()
                if item_id == '':
                    continue
                qty = int(qty)
                if qty == 0:
                    continue
                recipe_inputs += [[int(value) for value in item.values()]]
            
            recipe_outputs = []
            for item in recipe_output_list:
                item_id, qty = item.values()
                if item_id == '':
                    continue
                qty = int(qty)
                if qty == 0:
                    continue
                recipe_outputs += [[int(value) for value in item.values()]]
            
            print("Processed List")
            print(recipe_inputs)
            print(recipe_outputs)
            
            RecipeInput.delete().where(RecipeInput.recipe_id == recipe.id).execute()
            for item_id, qty in recipe_inputs:
                RecipeInput.create(
                    item_id = item_id,
                    recipe_id = recipe.id,
                    quantity = qty,
                )
            
            RecipeOutput.delete().where(RecipeOutput.recipe_id == recipe.id).execute()
            for item_id, qty in recipe_outputs:
                RecipeOutput.create(
                    item_id = item_id,
                    recipe_id = recipe.id,
                    quantity = qty,
                )
            
            #url = self.request.route_url(success_route)
            #return HTTPFound(url)
        
        return {
            'heading': "Edit {}".format(self.model.__name__),
            'edit_form_schema': edit_form.schema(),
            'item_options': json.dumps([[item.id, item.name] for item in Item.select().order_by(Item.name)], ensure_ascii=False),
            'recipe_input': RecipeInput.select().where(RecipeInput.recipe_id == recipe.id).order_by(RecipeInput.item.name),
            'recipe_output': RecipeOutput.select().where(RecipeOutput.recipe_id == recipe.id).order_by(RecipeOutput.item.name),
        }

    @view_config(route_name='recipe_delete', renderer='../templates/management/recipe_show.mako')
    def delete(self):
        return super().delete(success_route='item_list')


class StockView(ModelView):
    model = Stock
    
    @view_config(route_name='stock_list', renderer='../templates/management/stock_list.mako')
    def list(request):
        return {
            'stock_list': Stock.select().order_by(Stock.item.name)
        }

    @view_config(route_name='stock_new', renderer='../templates/management/generic_edit.mako')
    def add_new(self):
        return super().add_new(
            success_route = 'stock_list',
            fields = ['item_id', 'quantity'],
        )

    @view_config(route_name='stock_edit', renderer='../templates/management/generic_edit.mako')
    def edit(self):
        return super().edit(
            success_route = 'stock_list',
            fields = ['item_id', 'quantity'],
        )

    @view_config(route_name='stock_delete', renderer='../templates/management/stock_list.mako')
    def delete(self):
        return super().delete(success_route='stock_list')


class MachineView(ModelView):
    model = Machine
    
    @view_config(route_name='machine_list', renderer='../templates/management/machine_list.mako')
    def list(request):
        return {
            'machine_list': Machine.select().order_by(Machine.name),
        }

    @view_config(route_name='machine_show', renderer='../templates/management/machine_show.mako')
    def show(self):
        machine = self.get_or_404()
        return {
            'machine': machine,
            'recipe_list': [machine_recipe.recipe for machine_recipe in MachineRecipe.select().where(MachineRecipe.machine_id == machine.id).order_by(MachineRecipe.recipe.name)],
        }

    @view_config(route_name='machine_new', renderer='../templates/management/generic_edit.mako')
    def add_new(self):
        return super().add_new(
            success_route = 'machine_list',
            fields = ['name', 'details', 'quantity'],
        )

    @view_config(route_name='machine_edit', renderer='../templates/management/generic_edit.mako')
    def edit(self):
        return super().edit(
            success_route = 'machine_list',
            fields = ['name', 'details', 'quantity'],
        )

    @view_config(route_name='machine_delete', renderer='../templates/show_machine.mako')
    def delete(self):
        return super().delete(success_route='machine_list')


class TaskView(ModelView):
    model = Task
    
    @view_config(route_name='task_list', renderer='../templates/management/task_list.mako')
    def list(request):
        taskman = TaskManager()
        machine_sequences = taskman.update_db_tasks()
        
        for notif in taskman.sequence2log(machine_sequences):
            notif.save()
        
        return {
            'task_list': Task.select().order_by(Task.recipe.name),
            'machine_task_list': MachineTask.select().order_by(MachineTask.start_time),
        }

    @view_config(route_name='task_new', renderer='../templates/management/generic_edit.mako')
    def add_new(self):
        return super().add_new(
            success_route = 'task_list',
            fields = ['recipe_id', 'cycles', 'description'],
        )

    @view_config(route_name='task_edit', renderer='../templates/management/generic_edit.mako')
    def edit(self):
        return super().edit(
            success_route = 'task_list',
            fields = ['description', 'end_time'],
        )
    
    @view_config(route_name='task_delete', renderer='../templates/management/task_list.mako')
    def delete(self):
        return super().delete(success_route='task_list')

    @view_config(route_name='machine_task_delete', renderer='../templates/management/task_list.mako')
    def delete_mt(self):
        id = self.request.matchdict['id']
        try:
            selected = MachineTask.get_by_id(id)
            selected.delete_instance()
        except MachineTask.DoesNotExist:
            raise exception_response(404)
        
        url = self.request.route_url('task_list')
        return HTTPFound(url)


"""

# Get epoch
import time; time.time()

# Get epoch
import calendar, time; calendar.timegm(time.strptime('2000-01-01 12:34:00', '%Y-%m-%d %H:%M:%S'))
import time; time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(epoch))

\{\{ (((?! \}\}).)+) \}\}
\$\{$1\}

datetime.datetime.now().timestamp()

"""