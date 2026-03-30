from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.jobs import Jobs


parser = reqparse.RequestParser()
parser.add_argument('team_leader', requaried=True, type=int)
parser.add_argument('job', requaried=True)
parser.add_argument('work_size', requaried=True, type=int)
parser.add_argument('collaborators', requaried=True)
parser.add_argument('start_date', requaried=True)
parser.add_argument('end_date', requaried=True)
parser.add_argument('is_finished', requaried=True, type=bool)


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"News {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify(jobs.to_dict(
            only=('id', 'team_leader', 'job',
                  'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished')
        ))

    def delete(self, jobs_id):
        abort_if_jobs_not_found(Jobs)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'ok'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({
            'jobs': [
                job.to_dict(
                    only=('id', 'team_leader', 'job',
                          'work_size', 'collaborators',
                          'start_date', 'end_date',
                          'is_finished')
                ) for job in jobs
            ]
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            is_finished=args['is_finished']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'id': jobs.id})