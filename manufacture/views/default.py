from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..lib.task import TaskManager
from ..models import management
from ..models.management import Notification
from .base import BaseView


class DefaultView(BaseView):
    #@view_config(route_name='default', renderer='../templates/base.mako')
    def index(request):
        return {
            'text': "Hello world!",
        }


class HomeView(BaseView):
    @view_config(route_name='home', renderer='../templates/default/home.mako')
    def index(self):
        if not self.is_authenticated:
            url = self.request.route_url('user_login')
            return HTTPFound(url)

        if 'delete_notification' in self.request.params:
            delete_notification()
        
        if True:
            taskman = TaskManager()
            machine_sequences = taskman.update_db_tasks()
            
            for notif in taskman.sequence2log(machine_sequences):
                notif.save()
        
        return {
            'notification_list': Notification.select().order_by(Notification.time)
        }
    
    @view_config(route_name='notification_delete', renderer='../templates/default/home.mako')
    def delete_notification(self):
        id = self.request.matchdict['id']
        try:
            selected = Notification.get_by_id(id)
            selected.delete_instance()
        except Notification.DoesNotExist:
            print("warning: notification does not exist")
        
        url = self.request.route_url('home')
        return HTTPFound(url)

