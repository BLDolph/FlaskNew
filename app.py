from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def get_index():
    return render_template('base.html', title='Заготовка')


@app.route('/promotion')
def get_promotion():
    return ('Человечество вырастает из детства.'
            '<br>Человечеству мала одна планета.'
            '<br>Мы сделаем обитаемыми безжизненные пока планеты.'
            '<br>И начнем с Марса!'
            '<br>Присоединяйся!')


#@app.route('/training/<prof>')
#def training(prof):
    return render_template('training.html', title='Тренировки в полёте', prof=prof)


@app.route('/image_mars')
def image_mars():
    return render_template('image_mars.html')


@app.route('/promotion_image')
def promotion_image():
    return render_template('promotion_image.html')


@app.route('/astronaut_selection')
def astronaut_selection():
    return render_template('astronaut_selection.html', title='Отбор астронавтов')


@app.route('/list_prof/<list>')
def list_of_professions():
    professions = ['Инженер', 'Биолог', 'Строитель', 'Врач', 'Водитель марсохода']
    return render_template('list_prof.html')

@app.route('/answer')
@app.route('/auto_answer')
def answer():
    context = {
        'title': 'Анкета',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': True
    }
    return render_template('auto_answer.html', **context)


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)