from datetime import datetime
from flask import make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource

from flask import Flask, render_template
from flask import redirect

from data.db_session import create_session
from forms.jobs_form import JobsForm
from forms.login_form import LoginForm
from data.user import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from forms.register_form import RegisterForm
from resources.jobs_resources import JobsResource, JobsListResource
from resources.users_resources import UsersResource, UsersListResource

# from API import api

app = Flask(__name__)
# app.register_blueprint(api)
api = Api(app)
api.add_resource(JobsResource, '/api/v2/jobs/<int:jobs_id>')
api.add_resource(JobsListResource, '/api/v2/jobs')
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(UsersListResource, '/api/v2/users')

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


@app.route('/choice/<planet_name>')
def offer(planet_name):
    return render_template('offer.html', planet_name=planet_name)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == login_form.email.data
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


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    jobs_form = JobsForm()
    if jobs_form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(
            team_leader=jobs_form.team_leader.data,
            job=jobs_form.job.data,
            work_size=jobs_form.work_size.data,
            collaborators=jobs_form.collaborators.data,
            start_date=datetime.now(),
            is_finished=jobs_form.is_finished.data
        )
        session.add(job)
        session.commit()
        return redirect('/')
    else:
        return render_template('addjob.html', form=jobs_form, title='Adding a Job')


# @app.route('/register')
# def registration():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        session = db_session.create_session()
        new_user = User()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)



if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.run('127.0.0.1', 8080)