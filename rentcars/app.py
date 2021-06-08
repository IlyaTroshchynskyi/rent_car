from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)


# @app.route('/', methods=["GET"])
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)