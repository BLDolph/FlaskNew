from flask import Flask

app = Flask(__name__)

@app.route('/')
def get():
    return 'Миссия Колонизация Марса'


@app.route('/index')
def get_index():
    return 'И на Марсе будут яблони цвести!'


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)