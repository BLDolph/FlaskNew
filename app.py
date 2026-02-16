from flask import Flask

app = Flask(__name__)

@app.route('/')
def get():
    return 'Миссия Колонизация Марса'


@app.route('/index')
def get_index():
    return 'И на Марсе будут яблони цвести!'


@app.route('/promote')
def get_promotion():
    return ('Человечество вырастает из детства.'
            '<br>Человечеству мала одна планета.'
            '<br>Мы сделаем обитаемыми безжизненные пока планеты.'
            '<br>И начнем с Марса!'
            '<br>Присоединяйся!')


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)