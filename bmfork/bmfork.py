from flask import Flask
from models import db

app = Flask(__name__)
app.config.from_object('configs.settings')
try:
    app.config.from_envvar('BMFORK_SETTINGS')
except Exception as e:
    print e

db.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello world!'


if __name__ == '__main__':
    app.run()
