from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,current_user
from cseduprojecthub import APPLOGIN

class User(UserMixin,object):

    def __init__(self,ob):
        self.id = ob

@APPLOGIN.user_loader
def load_user(username):
    print(username)
    return User(username)





