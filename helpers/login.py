from flask_login import LoginManager, UserMixin
from helpers import users


login_manager = LoginManager()


class AppUser(UserMixin):
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username


@login_manager.user_loader
def get_user(user_id: int):
    user = users.get_user_by_id(user_id)
    return AppUser(user.id, user.username)
