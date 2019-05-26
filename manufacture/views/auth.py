from pyramid.view import view_config

from ..models.auth import User
from .base import BaseView
from .forms import PostForm


class AuthView(BaseView):
    @view_config(route_name='user_login', renderer='../templates/auth/user_login.mako')
    def login(self):
        login_form = PostForm(
            name = 'edit',
            action = 'submit',
            components = [
                {'name': 'username', 'label': "Username", 'type': "text",},
                {'name': 'password', 'label': "Password", 'type': "password",},
            ]
        )
        
        if 'submit' in self.request.params:
            form_values = login_form.extract_values(self.request.params)
            username = form_values['username']
            password = form_values['password']
            user = list(User.select().where(User.username == username, User.password == password))
            if len(user) == 1:
                self.request.session['user'] = user[0]
                url = self.request.route_url('home')
                return HTTPFound(url)
            return {
                'login_msg': "Invalid username and password combination",
                'login_form_schema': login_form.schema(),
            }

        return {
            'login_msg': "",
            'login_form_schema': login_form.schema(),
        }

    @view_config(route_name='user_logout', renderer='../templates/base.mako')
    def logout(self):
        del self.request.session['user']
        url = self.request.route_url('default')
        return HTTPFound(url)
