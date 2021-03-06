import os
from random import sample
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.db import init_db
from flask import current_app

from . import dataprocess
from . import fileconverter
from flask import send_from_directory

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, num_samples, sample_size, info'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/reset')
@login_required
def reset():
    init_db()
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, num_samples, sample_size, info'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        num_samples = request.form['num_samples']
        sample_size = request.form['sample_size']
        error = None
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not title or not num_samples or not sample_size:
            error = 'All fields are required.'
        if error is not None:
            flash(error)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            info = dataprocess.Data_Processor.statistics_info(fileconverter.convert_xl(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/') + filename))
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, num_samples, sample_size, info)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (title, body, g.user['id'], int(num_samples), int(sample_size), info)
            )
            db.commit()
            post = get_db().execute('SELECT * FROM post ORDER BY ID DESC LIMIT 1').fetchone()

            dp = dataprocess.Data_Processor(post['id'], fileconverter.convert_xl(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/') + filename), num_samples, sample_size)
            dp.distribution(post['id'], fileconverter.convert_xl(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/') + filename))
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
@login_required
def download_all(filename):
    post = get_db().execute('SELECT * FROM post ORDER BY ID DESC LIMIT 1').fetchone()
    all = "all" + str(post['id']) + ".csv"
    print(f"tried to send {all}")
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
@login_required
def download_summary(filename):
    post = get_db().execute('SELECT * FROM post ORDER BY ID DESC LIMIT 1').fetchone()
    summary = "summary" + str(post['id']) + ".csv"
    print(f"tried to send {summary}")
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, num_samples, sample_size, info'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
