import flask
from flask import jsonify, render_template
from flask_login import login_required, current_user

from forms.jobs import JobsForm
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/all_jobs')
def get_all_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'team_leader', 'work_size'))
                 for item in jobs]
        }
    )

@blueprint.route('/api/jobs/<int:id>')
def get_job_id(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id)
    if not list(jobs):
        return 'Работа не найдена'
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'team_leader', 'work_size'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.team_leader = form.team_id.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        db_sess.add(jobs)
        db_sess.commit()
        return flask.redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)
