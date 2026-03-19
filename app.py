from flask import Flask, render_template
from flask import redirect

from data.db_session import create_session
from forms.login_form import LoginForm
from data.user import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session

app = Flask(__name__)

app.config["SECRET_KEY"] = 'pudge'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    session = db_session.create_session()
    return session.get(User, user_id)


@app.route('/')
@app.route('/index')
def get_index():
    session = create_session()
    result = session.query(Jobs, User).join(User, Jobs.team_leader == User.id)
    return render_template('index.html', title='Главная страница', result=result)


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
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == login_form.email.data,
            User.hashed_password == login_form.password.data
        ).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, login_form.remember_me)
            return redirect('/')
        return render_template('login.html', form=login_form,
                                message='Пользователь не найден')

    return render_template('login.html', form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.run('127.0.0.1', 8080)