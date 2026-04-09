from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.user import User

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)

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

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            id=args['id'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            address=args['address'],
            email=args['email'],
            speciality=args['speciality'],
            hashed_password=args['hashed_password'],
        )
        session.add(user)
        session.commit()
        return jsonify({'id':user.id})