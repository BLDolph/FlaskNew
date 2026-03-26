from flask import Blueprint, jsonify
from flask import request
from data import db_session
from data.jobs import Jobs

api = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@api.route('/api/jobs', methods=['GET'])
def jobs():
    if request.method == 'GET':
        session = db_session.create_session()
        jobs_item = session.query(Jobs).all()
        return jsonify({
            'jobs': [
                job.to_dict(
                    only=('id', 'team_leader', 'job',
                          'work_size', 'collaborators',
                          'start_date', 'end_date',
                          'is_finished')
                ) for job in jobs_item
            ]
        })
    return jsonify({'error': 'Method Not Allowed '}), 405