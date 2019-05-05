from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.httpexceptions import (
    HTTPFound,
    exception_response
    )
import colander
import deform.widget
from .models import (
    Item, Recipe, RecipeInput, RecipeOutput, Stock, 
    Machine, MachineRecipe, Task, 
    Notification
    )


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
    editable_fields = None
    
    class EditForm(colander.MappingSchema):
        pass

    def __init__(self, request):
        self.request = request

    @property
    def edit_form(self):
        schema = self.EditForm()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.edit_form.get_widget_resources()

    def get_or_404(self):
        id = self.request.matchdict['id']
        try:
            return self.model.get_by_id(id)
        except self.model.DoesNotExist:
            raise exception_response(404)

    def new(self, success_route=None):
        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.edit_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(form=e.render(), heading="New {}".format(self.model.__name__))

            form_values = {}
            for field in self.editable_fields:
                form_values[field] = appstruct[field]
            self.model.create(**form_values)
            
            url = self.request.route_url(success_route)
            return HTTPFound(url)

        form = self.edit_form.render()
        
        return {
            'heading': "Add new {}".format(self.model.__name__),
            'form': form,
        }

    def edit(self, success_route=None):
        selected = self.get_or_404()
        
        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.edit_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(form=e.render())

            for field in self.editable_fields:
                setattr(selected, field, appstruct[field])
            selected.save()

            url = self.request.route_url(success_route)
            return HTTPFound(url)

        form_values = {}
        for field in self.editable_fields:
            form_values[field] = getattr(selected, field)
        
        form = self.edit_form.render(form_values)
        
        return {
            'heading': "Edit {}".format(self.model.__name__),
            'form': form,
        }
    
    def delete(self, success_route=None):
        selected = self.get_or_404()
        selected.delete_instance()
        url = self.request.route_url(success_route)
        return HTTPFound(url)


class ItemView(ModelView):
    model = Item
    editable_fields = ['name', 'description']
    
    class EditForm(colander.MappingSchema):
        name = colander.SchemaNode(colander.String())
        description = colander.SchemaNode(colander.String(), widget=deform.widget.TextAreaWidget())

    @view_config(route_name='show_item', renderer='templates/show_item.mako')
    def show(self):
        item = self.get_or_404()
        
        return {
            'item': item,
            'recipe_input': RecipeInput.select().where(RecipeInput.item_id == item.id).order_by(RecipeInput.item.name),
            'recipe_output': RecipeOutput.select().where(RecipeOutput.item_id == item.id).order_by(RecipeOutput.item.name),
        }

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

    @view_config(route_name='new_item', renderer='templates/deform_edit.mako')
    def new(self):
        return super(self.__class__, self).new(success_route='list_items')

    @view_config(route_name='edit_item', renderer='templates/deform_edit.mako')
    def edit(self):
        return super(self.__class__, self).edit(success_route='list_items')

    @view_config(route_name='delete_item', renderer='templates/show_item.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_items')


class RecipeView(ModelView):
    model = Recipe
    editable_fields = ['name', 'description', 'duration']
    
    class EditForm(colander.MappingSchema):
        name = colander.SchemaNode(colander.String())
        description = colander.SchemaNode(colander.String(), widget=deform.widget.TextAreaWidget())
        duration = colander.SchemaNode(colander.Time(), widget=deform.widget.TimeInputWidget())

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
    def new(self):
        success_route = 'list_items'
        
        form_values = {
            'name': "",
            'description': "",
            'duration': 0,
        }
        if 'submit' in self.request.params:
            form_values = {}
            for field in self.editable_fields:
                value = self.request.params[field]
                if value:
                    form_values[field] = value
            self.model.create(**form_values)
            url = self.request.route_url(success_route)
            return HTTPFound(url)

        return {
            'heading': "Add new {}".format(self.model.__name__),
            'form_values': form_values,
        }

    @view_config(route_name='edit_recipe', renderer='templates/recipe/edit.mako')
    def edit(self):
        success_route = 'list_items'
        selected = self.get_or_404()
        
        form_values = {}
        if 'submit' in self.request.params:
            selected.name = self.request.params['name']
            selected.description = self.request.params['description']
            selected.duration = int(self.request.params['duration'])
            selected.save()
            url = self.request.route_url(success_route)
            return HTTPFound(url)
        else:
            for field in self.editable_fields:
                form_values[field] = getattr(selected, field)
        
        return {
            'heading': "Edit {}".format(self.model.__name__),
            'form_values': form_values,
        }

    @view_config(route_name='delete_recipe', renderer='templates/recipe/show.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_items')


class StockView(ModelView):
    model = Stock
    editable_fields = ['item', 'description', 'quantity']
    
    class EditForm(colander.MappingSchema):
        name = colander.SchemaNode(colander.String())
        description = colander.SchemaNode(colander.String(), widget=deform.widget.TextAreaWidget())
        quantity = colander.SchemaNode(colander.Integer(), validator=colander.Range(0, 10000))

    @view_config(route_name='list_stocks', renderer='templates/stock/list.mako')
    def list(request):
        return {
            'stock_list': Stock.select().order_by(Stock.item.name)
        }

    @view_config(route_name='new_stock', renderer='templates/stock/edit.mako')
    def new(self):
        success_route = 'list_stocks'
        
        form_values = {
            'item': [[item.id, item.name] for item in Item.select().order_by(Item.name)],
            'comment': "",
            'description': "",
            'quantity': 0,
        }
        if 'submit' in self.request.params:
            form_values = {}
            for field in ['item', 'comment', 'description', 'quantity']:
                value = self.request.params[field]
                if value:
                    form_values[field] = value
            self.model.create(**form_values, check_time=0)
            url = self.request.route_url(success_route)
            return HTTPFound(url)

        return {
            'heading': "Add new {}".format(self.model.__name__),
            'form_values': form_values,
        }

    @view_config(route_name='edit_stock', renderer='templates/stock/edit.mako')
    def edit(self):
        success_route = 'list_stocks'
        selected = self.get_or_404()
        
        form_values = {
            'item': [[item.id, item.name] for item in Item.select().order_by(Item.name)],
            'comment': selected.comment,
            'description': selected.description,
            'quantity': selected.quantity,
        }
        if 'submit' in self.request.params:
            form_values = {}
            for field in ['item', 'comment', 'description', 'quantity']:
                value = self.request.params[field]
                if value:
                    form_values[field] = value
            self.model.create(**form_values, check_time=0)
            url = self.request.route_url(success_route)
            return HTTPFound(url)

        return {
            'heading': "Edit {}".format(self.model.__name__),
            'form_values': form_values,
        }

    
    @view_config(route_name='delete_stock', renderer='templates/list_stocks.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_stocks')


class MachineView(ModelView):
    model = Machine
    editable_fields = ['name', 'description', 'quantity']
    
    class EditForm(colander.MappingSchema):
        name = colander.SchemaNode(colander.String())
        description = colander.SchemaNode(colander.String(), widget=deform.widget.TextAreaWidget())
        quantity = colander.SchemaNode(colander.Integer(), validator=colander.Range(0, 10000))

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

    @view_config(route_name='new_machine', renderer='templates/deform_edit.mako')
    def new(self):
        return super(self.__class__, self).new(success_route='list_machines')

    @view_config(route_name='edit_machine', renderer='templates/deform_edit.mako')
    def edit(self):
        return super(self.__class__, self).edit(success_route='list_machines')

    @view_config(route_name='delete_machine', renderer='templates/show_machine.mako')
    def delete(self):
        return super(self.__class__, self).delete(success_route='list_machines')


class TaskView(ModelView):
    model = Task
    editable_fields = ['name', 'recipe', 'comment', 'start_time', 'end_time']
    
    class EditForm(colander.MappingSchema):
        name = colander.SchemaNode(colander.String())
        recipe = colander.SchemaNode(colander.String())
        comment = colander.SchemaNode(colander.String())
        start_time = colander.SchemaNode(colander.DateTime(), widget=deform.widget.DateTimeInputWidget())
        end_time = colander.SchemaNode(colander.DateTime(), widget=deform.widget.DateTimeInputWidget())

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

    @view_config(route_name='new_task', renderer='templates/task/add.mako')
    def new(self):
        success_route = 'list_tasks'
        
        form_values = {
            'machine': [[machine.id, machine.name] for machine in Machine.select().order_by(Machine.name)],
            'recipe': [[recipe.id, recipe.name] for recipe in Recipe.select().order_by(Recipe.name)],
            'comment': "",
            'start_time': 0,
            'end_time': 0,
        }
        #'recipe': [[machine_recipe.recipe.id, machine_recipe.recipe.name] for machine_recipe in MachineRecipe.select().order_by(MachineRecipe.recipe.name)],
        if 'submit' in self.request.params:
            form_values = {}
            for field in ['machine', 'recipe', 'comment', 'start_time', 'end_time']:
                value = self.request.params[field]
                if value:
                    form_values[field] = value
            self.model.create(**form_values, check_time=0)
            url = self.request.route_url(success_route)
            return HTTPFound(url)

        return {
            'heading': "Add new {}".format(self.model.__name__),
            'form_values': form_values,
        }

    @view_config(route_name='edit_task', renderer='templates/task/edit.mako')
    def edit(self):
        success_route = 'list_tasks'
        machine = self.get_or_404()
        
        form_values = {
            'machine': [[machine.id, machine.name] for machine in Machine.select().order_by(Machine.name)],
            'recipe': [[recipe.id, recipe.name] for recipe in Recipe.select().order_by(Recipe.name)],
            'comment': machine.comment,
            'start_time': machine.start_time,
            'end_time': machine.end_time,
        }
        #'recipe': [[machine_recipe.recipe.id, machine_recipe.recipe.name] for machine_recipe in MachineRecipe.select().order_by(MachineRecipe.recipe.name)],
        if 'submit' in self.request.params:
            form_values = {}
            for field in ['machine', 'recipe', 'comment', 'start_time', 'end_time']:
                value = self.request.params[field]
                if value:
                    form_values[field] = value
            self.model.create(**form_values, check_time=0)
            url = self.request.route_url(success_route)
            return HTTPFound(url)

        return {
            'heading': "Edit {}".format(self.model.__name__),
            'form_values': form_values,
        }

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