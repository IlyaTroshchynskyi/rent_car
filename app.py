from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import *
