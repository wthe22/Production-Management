from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.session import SignedCookieSessionFactory

from .models import (
    auth,
    management,
)


class MyRequest(Request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        auth.db.init('manufacture/databases/auth.sqlite3')
        auth.db.connect()
    
        management.db.init('manufacture/databases/test.sqlite3')
        management.db.connect()
        
        self.models_db = [auth.db, management.db]
        
        self.add_finished_callback(self.finish)

    def finish(self, request):
        for db in self.models_db:
            db.commit()
            
            if not db.is_closed():
                db.close()


def main(global_config, **settings):
    my_session_factory = SignedCookieSessionFactory('secret_key_here')
    config = Configurator(
        settings = settings,
        session_factory = my_session_factory
    )
    config.set_request_factory(MyRequest)
    config.include('pyramid_mako')
    
    config.add_route('home', '/')
    config.add_route('user_login', '/login/')
    config.add_route('user_logout', '/logout/')
    
    config.add_route('item_list', '/items/')
    config.add_route('item_show', '/item/{id}/')
    config.add_route('item_new', '/new/item/')
    config.add_route('item_edit', '/edit/item/{id}/')
    config.add_route('item_delete', '/delete/item/{id}/')
    
    config.add_route('recipe_show', '/recipe/{id}/')
    config.add_route('recipe_new', '/new/recipe/')
    config.add_route('recipe_edit', '/edit/recipe/{id}/')
    config.add_route('recipe_delete', '/delete/recipe/{id}/')
    
    config.add_route('stock_list', '/inventory/')
    config.add_route('stock_new', '/new/stock/')
    config.add_route('stock_edit', '/edit/stock/{id}/')
    config.add_route('stock_delete', '/delete/stock/{id}/')
    
    config.add_route('machine_list', '/machines/')
    config.add_route('machine_show', '/machine/{id}/')
    config.add_route('machine_new', '/new/machine/')
    config.add_route('machine_edit', '/edit/machine/{id}/')
    config.add_route('machine_delete', '/delete/machine/{id}/')
    
    config.add_route('task_list', '/tasks/')
    config.add_route('task_new', '/new/task/')
    config.add_route('task_edit', '/edit/task/{id}/')
    config.add_route('task_delete', '/delete/task/{id}/')
    config.add_route('machine_task_delete', '/delete/task_machine/{id}/')
    
    config.add_route('notification_delete', '/delete/notification/{id}/')
    
    config.add_route('analyzer_input', '/analyzer/input/')
    config.add_route('analyzer_test', '/analyzer/test/')
    config.add_route('analyzer_result', '/analyzer/result/')
    
    config.add_route('download_file', '/download/{filename}')
    
    config.add_static_view(name='static', path='static')
    
    config.scan('.views.default')
    config.scan('.views.auth')
    config.scan('.views.management')
    config.scan('.views.analyzer')

    return config.make_wsgi_app()
