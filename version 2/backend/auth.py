from flask_login import LoginManager
# from models import User, db
# from .models import User, db
try:
    from models import User, db
except ImportError:
    from .models import User, db


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None