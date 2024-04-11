#!/usr/bin/python3
from flask_login import current_user, login_required
from flask import render_template, flash, redirect, Blueprint, url_for, request, abort
from model.base import Job, JobPlumber
from .utils import new, save, delete
from .form import PostJobForm

job_route = Blueprint('job_route', __name__, url_prefix="/jobs", template_folder='templates', static_folder='static')

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
        return redirect(url_for('main.home'))
    return render_template('post_job.html', title='Post Job', form=form)


@job_route.route("/jobs/<int:job_id>", strict_slashes=False)
def job(job_id):
    """ Renders the job details """
    job = Job.query.get_or_404(job_id)
    return render_template('job.html', title=job.job_title, job=job)

@job_route.route("/apply_job/<int:job_id>", strict_slashes=False)
def apply_job(job_id):
    """ Apply for a job """
    job = Job.query.get_or_404(job_id)
    job_plumber = JobPlumber(job_id=job.id, plumber_id=current_user.id)
    new(job_plumber)
    save()
    flash(f'You have applied for the job!', 'success')
    return redirect(url_for('main.home'))

@job_route.route("/jobs/<int:job_id>/update", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_job(job_id):
    """ Update the job """
    job = Job.query.get_or_404(job_id)
    if job.client != current_user:
        abort(403)
    form = PostJobForm()
    if form.validate_on_submit():
        job.job_title = form.job_title.data
        job.content = form.content.data
        job.location = form.state.data
        job.job_description = form.job_description.data
        save()
        flash(f'Job updated successfully!', 'success')
        return redirect(url_for('job_route.job', job_id=job.id))
    elif request.method == 'GET':
        form.job_title.data = job.job_title
        form.content.data = job.content
        form.state.data = job.location
        form.job_description.data = job.job_description
    return render_template('post_job.html', title='Update Job', form=form, legend='Update Job')

@job_route.route("/jobs/<int:job_id>/delete", methods=['POST'], strict_slashes=False)
@login_required
def delete_job(job_id):
    """ Delete the job """
    job = Job.query.get_or_404(job_id)
    if job.client != current_user:
        abort(403)
    delete(job)
    flash(f'Job deleted successfully!', 'success')
    return redirect(url_for('main.home'))