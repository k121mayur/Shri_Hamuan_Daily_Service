import os
from flask import Flask
from application.database import db
from flask_login import LoginManager
from application.models import Users


basedir = os.path.abspath(os.path.dirname(__file__))
tp = os.path.join(basedir, "../templates")
st = os.path.join(basedir, "../static")
app = Flask(__name__, template_folder=tp, static_folder=st)
SQLITE_DB_DIR = os.path.join(basedir, "../database")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testing.sqlite3")

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

db.init_app(app)
login_manager.init_app(app)
app.app_context().push()



# Import all the controllers so they are loaded
from application.controllers import *


app.debug = True
if __name__ == '__main__':
    app.run(host="0.0.0.0")
