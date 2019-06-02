from ..models import (
    auth,
    management,
)


class BaseView:
    def __init__(self, request):
        self.request = request
    
    def __del__(self):
        pass
    
    @property
    def user(self):
        session = self.request.session
        if 'user' in session:
            return session['user']
        return "Anonymous"

    @property
    def is_authenticated(self):
        if 'user' in self.request.session:
            return True
        return False
