from .base import BaseView
from pyramid.view import view_config
from ..models.management import Notification


class DefaultView(BaseView):
    @view_config(route_name='default', renderer='../templates/base.mako')
    def default_view(request):
        return {
            'text': "Hello world!",
        }


class HomeView(BaseView):
    def delete_notification(self):
        id = self.request.matchdict['id']
        try:
            selected = Notification.get_by_id(id)
            selected.delete_instance()
        except Notification.DoesNotExist:
            print("warning: notification does not exist")
        return

    @view_config(route_name='home', renderer='../templates/home.mako')
    def list(self):
        if 'delete_notification' in self.request.params:
            delete_notification()
        
        return {
            'notification_list': Notification.select().order_by(Notification.time)
        }
