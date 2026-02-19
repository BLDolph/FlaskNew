from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')#
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


@app.route('/image_mars')
def image_mars():
    return render_template('image_mars.html')


@app.route('/promotion_image')
def promotion_image():
    return render_template('promotion_image.html')


@app.route('/astronaut_selection')
def astronaut_selection():
    return render_template('astronaut_selection.html')

if __name__ == '__main__':
    app.run('127.0.0.1', 8080)