from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.session import SignedCookieSessionFactory
from .models import db


class MyRequest(Request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db.init('manufacture/test.sqlite3')
        db.connect()
        self.add_finished_callback(self.finish)

    def finish(self, request):
        if not db.is_closed():
            db.close()


def main(global_config, **settings):
    my_session_factory = SignedCookieSessionFactory('secret_key_here')
    config = Configurator(
        settings = settings,
        session_factory = my_session_factory
        )
    config.include('pyramid_mako')
    
    config.add_route('default', '/')
    config.add_route('home', '/home/')
    config.add_route('login', '/login/')
    config.add_route('logout', '/logout/')
    
    config.add_route('list_items', '/items/')
    config.add_route('show_item', '/item/{id}/')
    config.add_route('new_item', '/new/item/')
    config.add_route('edit_item', '/edit/item/{id}/')
    config.add_route('delete_item', '/delete/item/{id}/')
    
    config.add_route('show_recipe', '/recipe/{id}/')
    config.add_route('new_recipe', '/new/recipe/')
    config.add_route('edit_recipe', '/edit/recipe/{id}/')
    config.add_route('delete_recipe', '/delete/recipe/{id}/')
    
    config.add_route('list_stocks', '/inventory/')
    config.add_route('new_stock', '/new/stock/')
    config.add_route('edit_stock', '/edit/stock/{id}/')
    config.add_route('delete_stock', '/delete/stock/{id}/')
    
    config.add_route('list_machines', '/machines/')
    config.add_route('show_machine', '/machine/{id}/')
    config.add_route('new_machine', '/new/machine/')
    config.add_route('edit_machine', '/edit/machine/{id}/')
    config.add_route('delete_machine', '/delete/machine/{id}/')
    
    config.add_route('list_tasks', '/tasks/')
    config.add_route('show_task', '/task/{id}/')
    config.add_route('new_task', '/new/task/')
    config.add_route('edit_task', '/edit/task/{id}/')
    config.add_route('delete_task', '/delete/task/{id}/')
    
    config.add_route('show_analyzer', '/analyzer/')
    
    config.add_static_view(name='static', path='static')
    config.add_static_view('deform_static', 'deform:static/')
    config.set_request_factory(MyRequest)
    config.scan('.views')
    return config.make_wsgi_app()
