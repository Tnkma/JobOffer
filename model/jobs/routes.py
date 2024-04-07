#!/usr/bin/python3
from flask_login import current_user, login_required
from flask import render_template, flash, redirect, Blueprint
from model.base import Job
from .utils import new, save
from .form import PostJobForm

job_route = Blueprint('job_route', __name__)

@job_route.route("/jobs/new", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def post_new_job():
    """ Posts new job"""
    form = PostJobForm()
    if form.validate_on_submit():
        job  = Job(job_title=form.job_title.data, content=form.content.data, location=form.state.data, job_description=form.job_description.data, client_id=current_user.id)
        new(job)
        save()
        flash(f'Job posted successfully!', 'success')
        return redirect(job_route.url_for('home'))
    return render_template('post_job.html', title='Post Job', form=form)


@job_route.route("/jobs/<int:job_id>", strict_slashes=False)
def job(job_id):
    """ Renders the job details """
    job = Job.query.get_or_404(job_id)
    return render_template('job.html', title=job.job_title, job=job)