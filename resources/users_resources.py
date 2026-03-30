from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.user import User


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"News {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(user.to_dict(
            only=('id', 'surname', 'name',
                  'age', 'position',
                  'speciality', 'address', 'email', 'hashed_password')
        ))

    def delete(self, user_id):
        abort_if_users_not_found(User)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'ok'})

class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users': [
                user.to_dict(
                    only=('id', 'surname', 'name',
                          'age', 'position',
                          'speciality', 'address',
                          'email', 'hashed_password')
                ) for user in users
            ]
        })