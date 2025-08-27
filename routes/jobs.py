# routes/jobs.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os

from forms import JobPostForm, ApplicationForm
from models import db, Job, Application

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/')
def index():
    query = request.args.get('q', '')
    location = request.args.get('location', '')
    
    jobs = Job.query
    
    if query:
        jobs = jobs.filter(Job.title.ilike(f'%{query}%') | Job.description.ilike(f'%{query}%'))
    
    if location:
        jobs = jobs.filter(Job.location.ilike(f'%{location}%'))

    jobs = jobs.order_by(Job.timestamp.desc()).all()
    
    return render_template('jobs/search.html', jobs=jobs)

@jobs_bp.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if not current_user.is_employer:
        flash('Only employers can post jobs.', 'danger')
        return redirect(url_for('jobs.index'))

    form = JobPostForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            location=form.location.data,
            description=form.description.data,
            salary=form.salary.data,
            posted_by=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('jobs.index'))
        
    return render_template('jobs/create_job.html', form=form)

@jobs_bp.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('jobs/job_details.html', job=job)

@jobs_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply_to_job(job_id):
    form = ApplicationForm()
    job = Job.query.get_or_404(job_id)

    if form.validate_on_submit():
        if not current_user.is_employer:
            # Handle resume upload
            f = form.resume.data
            filename = secure_filename(f.filename)
            upload_path = os.path.join(current_app.root_path, 'static', 'resumes', filename)

            # Create the 'resumes' directory if it doesn't exist
            if not os.path.exists(os.path.join(current_app.root_path, 'static', 'resumes')):
                os.makedirs(os.path.join(current_app.root_path, 'static', 'resumes'))
            
            f.save(upload_path)

            application = Application(
                job_id=job.id,
                jobseeker_id=current_user.id,
                resume=filename,
                cover_letter=form.cover_letter.data
            )
            db.session.add(application)
            db.session.commit()
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('jobs.index'))
        else:
            flash('Employers cannot apply for jobs.', 'danger')
            return redirect(url_for('jobs.job_details', job_id=job.id))
            
    return render_template('jobs/apply_to_job.html', form=form, job=job)