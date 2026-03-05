from flask import Flask, render_template
from flask import redirect

from login_form import LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = 'pudge'


@app.route('/')
@app.route('/index')
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


@app.route('/choice/<planet_name>')
def choice_planet(planet_name):
    return render_template('choose_planet.html')


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)