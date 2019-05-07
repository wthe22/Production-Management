from datetime import datetime, timedelta
from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.httpexceptions import (
    HTTPFound,
    exception_response
    )
from .models import (
    Item, Recipe, RecipeInput, RecipeOutput, Stock, 
    Machine, MachineRecipe, Task, 
    Notification
    )
from .forms import PostForm


@view_config(route_name='home', renderer='templates/base.mako')
def home(request):
    return {
        'text': "Welcome to the management site!"
    }


def display_time(seconds, granularity=2):
    result = []

    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
        )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


class AuthView():
    def __init__(self, request):
        self.request = request

    @view_config(route_name='login', renderer='templates/login.mako')
    def login(self):
        return {}

    @view_config(route_name='logout', renderer='templates/home.mako')
    def logout(self):
        
        url = self.request.route_url('home')
        return HTTPFound(url)


class ModelView():
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
                'type': "textarea",
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
            'comment': {
                'label': "Comment",
                'type': "text",
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
            'end_time': {
                'label': "End Time",
                'type': "datetime",
            },
        }
        return {**components[name], 'name': name}
    
    def __init__(self, request):
        self.request = request

    def get_or_404(self):
        id = self.request.matchdict['id']
        try:
            return self.model.get_by_id(id)
        except self.model.DoesNotExist:
            raise exception_response(404)

    def add_new(self, success_route, fields):
        edit_form = PostForm(
            name = 'edit',
            action = 'submit',
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
            action = 'submit',
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
    
    @view_config(route_name='list_items', renderer='templates/list_items.mako')
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

    @view_config(route_name='show_item', renderer='templates/show_item.mako')
    def show(self):
        item = self.get_or_404()
        
        return {
            'item': item,
            'recipe_input': RecipeInput.select().where(RecipeInput.item_id == item.id).order_by(RecipeInput.item.name),
            'recipe_output': RecipeOutput.select().where(RecipeOutput.item_id == item.id).order_by(RecipeOutput.item.name),
        }

    @view_config(route_name='new_item', renderer='templates/generic/edit.mako')
    def add_new(self):
        return super(self.__class__, self).add_new(
            success_route = 'list_items',
            fields = ['name', 'description']
        )

    @view_config(route_name='edit_item', renderer='templates/generic/edit.mako')
    def edit(self):
        return super(self.__class__, self).edit(
            success_route = 'list_items',
            fields = ['name', 'description']
        )

    @view_config(route_name='delete_item', renderer='templates/show_item.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_items')


class RecipeView(ModelView):
    model = Recipe
    
    @view_config(route_name='show_recipe', renderer='templates/recipe/show.mako')
    def show(self):
        recipe = self.get_or_404()
        recipe.duration = display_time(recipe.duration)
        return {
            'recipe': recipe,
            'recipe_input': RecipeInput.select().where(RecipeInput.recipe_id == recipe.id).order_by(RecipeInput.item.name),
            'recipe_output': RecipeOutput.select().where(RecipeOutput.recipe_id == recipe.id).order_by(RecipeOutput.item.name),
            'machine_list': [machine_recipe.machine for machine_recipe in MachineRecipe.select().where(MachineRecipe.recipe_id == recipe.id).order_by(MachineRecipe.machine.name)],
        }

    @view_config(route_name='new_recipe', renderer='templates/recipe/edit.mako')
    def add_new(self):
        return super(self.__class__, self).add_new(
            success_route = 'list_items',
            fields = ['name', 'description', 'duration']
        )

    @view_config(route_name='edit_recipe', renderer='templates/recipe/edit.mako')
    def edit(self):
        return super(self.__class__, self).edit(
            success_route = 'list_items',
            fields = ['name', 'description', 'duration']
        )

    @view_config(route_name='delete_recipe', renderer='templates/recipe/show.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_items')


class StockView(ModelView):
    model = Stock
    
    @view_config(route_name='list_stocks', renderer='templates/stock/list.mako')
    def list(request):
        return {
            'stock_list': Stock.select().order_by(Stock.item.name)
        }

    @view_config(route_name='new_stock', renderer='templates/generic/edit.mako')
    def add_new(self):
        return super(self.__class__, self).add_new(
            success_route = 'list_stocks',
            fields = ['item_id', 'comment', 'description', 'quantity']
        )

    @view_config(route_name='edit_stock', renderer='templates/generic/edit.mako')
    def edit(self):
        return super(self.__class__, self).edit(
            success_route = 'list_stocks',
            fields = ['item_id', 'comment', 'description', 'quantity']
        )

    @view_config(route_name='delete_stock', renderer='templates/list_stocks.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_stocks')


class MachineView(ModelView):
    model = Machine
    
    @view_config(route_name='list_machines', renderer='templates/machine/list.mako')
    def list(request):
        return {
            'machine_list': Machine.select().order_by(Machine.name)
        }

    @view_config(route_name='show_machine', renderer='templates/machine/show.mako')
    def show(self):
        machine = self.get_or_404()
        return {
            'machine': machine,
            'recipe_list': [machine_recipe.recipe for machine_recipe in MachineRecipe.select().where(MachineRecipe.machine_id == machine.id).order_by(MachineRecipe.recipe.name)],
        }

    @view_config(route_name='new_machine', renderer='templates/generic/edit.mako')
    def add_new(self):
        return super(self.__class__, self).add_new(
            success_route = 'list_machines',
            fields = ['name', 'description', 'quantity']
        )

    @view_config(route_name='edit_machine', renderer='templates/generic/edit.mako')
    def edit(self):
        return super(self.__class__, self).edit(
            success_route = 'list_machines',
            fields = ['name', 'description', 'quantity']
        )

    @view_config(route_name='delete_machine', renderer='templates/show_machine.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_machines')


class TaskView(ModelView):
    model = Task
    
    @view_config(route_name='list_tasks', renderer='templates/task/list.mako')
    def list(request):
        task_list = []
        for task in Task.select().order_by(Task.machine.name):
            task.start_time = display_time(task.start_time)
        
        return {
            'task_list': Task.select().order_by(Task.machine.name)
        }

    @view_config(route_name='show_task', renderer='templates/show_task.mako')
    def show(self):
        machine = self.get_or_404()
        
        return {
            'machine': machine,
        }

    @view_config(route_name='new_task', renderer='templates/generic/edit.mako')
    def add_new(self):
        return super(self.__class__, self).add_new(
            success_route = 'list_tasks',
            fields = ['machine_id', 'recipe_id', 'comment', 'start_time', 'end_time']
        )

    @view_config(route_name='edit_task', renderer='templates/generic/edit.mako')
    def edit(self):
        return super(self.__class__, self).edit(
            success_route = 'list_tasks',
            fields = ['comment', 'end_time']
        )
    
    @view_config(route_name='delete_task', renderer='templates/task/list.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_tasks')



class NotificationView(ModelView):
    model = Notification
    editable_fields = None
    
    @view_config(route_name='list_notifications', renderer='templates/list_notifications.mako')
    def list(request):
        return {
            'notification_list': Notification.select().order_by(Notification.time)
        }

    @view_config(route_name='add_notification', renderer='templates/show_notifications.mako')
    def add(sef):
        Notification.create(
            time = 14,
            title = "Smelting for Glass Done",
        )
        
        return {
            'notification_list': Notification.select().order_by(Notification.time)
        }
    
    @view_config(route_name='delete_notification', renderer='templates/list_notifications.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_notifications')


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