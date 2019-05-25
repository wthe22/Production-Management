
class BaseView:
    def __init__(self, request):
        self.request = request

    @property
    def user(self):
        session = self.request.session
        if 'user' in session:
            return session['user']
        return "Anonymous"

    @property
    def is_authenticated(self):
        return True
        if 'user' in self.request.session:
            return True
        return False