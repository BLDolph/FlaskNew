from data import db_session
from data.jobs import Jobs
from datetime import datetime

db_session.global_init("../db/mars_explorer.db")
session = db_session.create_session()

resident = Jobs(
    team_leader=1,
    job='deployment of residential modules 1 and 2',
    work_size=15,
    collaborators='2, 3',
    start_date=datetime.now(),
    is_finished=False
)