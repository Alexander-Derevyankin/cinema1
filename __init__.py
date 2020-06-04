
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

login = LoginManager(app)
login.login_view = 'login'
from app import routes, models
from app.posts.blueprint import posts

app.register_blueprint(posts, url_prefix="/blog")

### ADMIN ###
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import *

admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))

#Flask security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)