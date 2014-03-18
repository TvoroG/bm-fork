from flask import Flask

app = Flask(__name__)
app.config.from_object('settings')


@app.route('/')
def hello_world():
    return 'Hello world!'


if __name__ == '__main__':
    app.run()
