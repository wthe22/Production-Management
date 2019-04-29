from pyramid.view import (
    view_config,
    view_defaults
    )
import pyramid.httpexceptions as exc
from .models import *


@view_config(route_name='home', renderer='templates/base.mako')
def home(request):
    return {
        'text': "Hello world"
    }


@view_config(route_name='list_items', renderer='templates/list_items.mako')
def list_items(request):
    recipe_full_list = []
    for recipe in Recipe.select().order_by(Recipe.name):
        recipe_full_list += [[
            recipe,
            [
                list(RecipeInput.select().where(RecipeInput.recipe == recipe.id)),
                list(RecipeOutput.select().where(RecipeOutput.recipe == recipe.id)),
            ],
        ]]
    return {
        'item_list': Item.select().order_by(Item.name),
        'recipe_full_list': recipe_full_list,
    }

@view_config(route_name='list_stocks', renderer='templates/list_stocks.mako')
def list_stocks(request):
    return {
        'stock_list': Stock.select().order_by(Stock.item.name)
    }

@view_config(route_name='list_machines', renderer='templates/list_machines.mako')
def list_machines(request):
    return {
        'machine_list': Machine.select().order_by(Machine.name)
    }

@view_config(route_name='list_tasks', renderer='templates/list_tasks.mako')
def list_tasks(request):
    return {
        'task_list': Task.select().order_by(Task.machine.name)
    }

@view_config(route_name='list_notifications', renderer='templates/list_notifications.mako')
def list_notifications(request):
    return {
        'notification_list': Notification.select().order_by(Notification.time)
    }

@view_config(route_name='list_db', renderer='templates/list_db.mako')
def list_db(request):
    return {}

@view_config(route_name='show_item', renderer='templates/show_item.mako')
def show_item(request):
    id = request.matchdict['id']
    item = Item.select().where(Item.id == id).limit(1)
    if len(item) > 0:
        item = item[0] 
    else:
        raise exc.exception_response(404)
    
    return {
        'item': item,
        'recipe_input': RecipeInput.select().where(RecipeInput.item_id == id).order_by(RecipeInput.item.name),
        'recipe_output': RecipeOutput.select().where(RecipeOutput.item_id == id).order_by(RecipeOutput.item.name),
    }

@view_config(route_name='show_recipe', renderer='templates/show_recipe.mako')
def show_recipe(request):
    id = request.matchdict['id']
    recipe = Recipe.select().where(Recipe.id == id).limit(1)
    if len(recipe) > 0:
        recipe = recipe[0] 
    else:
        raise exc.exception_response(404)
    
    return {
        'recipe': recipe,
        'recipe_input': RecipeInput.select().where(RecipeInput.recipe_id == id).order_by(RecipeInput.item.name),
        'recipe_output': RecipeOutput.select().where(RecipeOutput.recipe_id == id).order_by(RecipeInput.item.name),
    }

@view_config(route_name='edit_object', renderer='templates/edit_object.mako')
def edit_object(request):
    return {
        'notification_list': Notification.select().order_by(Notification.time)
    }

"""

\{\{ (((?! \}\}).)+) \}\}
\$\{$1\}

"""