import os
from sqla_wrapper import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)
    session_token = db.Column(db.String, unique=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
