from pyramid.config import Configurator
from pyramid.request import Request
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
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_route('home', '/')
    config.add_route('list_items', '/items/')
    config.add_route('list_stocks', '/stocks/')
    config.add_route('list_machines', '/machines/')
    config.add_route('list_tasks', '/tasks/')
    config.add_route('list_notifications', '/notifications/')
    config.add_route('list_db', '/database/')
    config.add_route('show_item', '/item/{id}/')
    config.add_route('show_recipe', '/recipe/{id}/')
    config.add_route('new_object', '/new/{model}/{id}/')
    config.add_route('edit_object', '/edit/{model}/{id}/')
    #config.add_view(yourview, route_name='new_object')
    #config.add_route('populate_items', '/populate/items/{sample}/')
    #config.add_route('populate_stocks', '/populate/stocks/')
    config.add_static_view(name='static', path='static')
    config.set_request_factory(MyRequest)
    config.scan('.views')
    return config.make_wsgi_app()