from application import app
from flask import current_app as app
from application.database import db

with app.app_context():
    db.create_all()
app.run(host = "0.0.0.0", port=5005)